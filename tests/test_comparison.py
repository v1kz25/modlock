"""Synthetic comparisons with explicit context and conservation assertions."""

import json
from copy import deepcopy
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from modlock.comparison import compare_exports
from modlock.identity import normalize_export
from modlock.meteoric import read_meteoric


def mod(page: int, name: str) -> dict:
    return dict(
        id=page,
        type="mod",
        separatorName="Unsectioned",
        modName=name,
        displayName=name,
        plugins=[],
        general=dict(
            modid=str(page),
            version="1",
            newestVersion="",
            category="",
            installationFile="",
        ),
        installed=dict(size=1, files=[dict(modid=str(page), fileid=str(page * 10))]),
        order=0,
        tags=[],
        active=True,
    )


def load(tmp_path: Path, name: str, data: list[dict]):
    for i, item in enumerate(data):
        item["order"] = i
    path = tmp_path / name
    path.write_text(json.dumps(data), encoding="utf-8")
    return normalize_export(read_meteoric(path))


def compare(tmp_path: Path, a: list[dict], b: list[dict], context="synthetic:lineage"):
    return compare_exports(
        load(tmp_path, "old.json", a), load(tmp_path, "new.json", b), context=context
    )


def test_context_is_never_inferred(tmp_path: Path) -> None:
    result = compare(tmp_path, [mod(1, "A")], [mod(1, "A")], None)
    assert [c.category for c in result.changes] == ["ambiguous", "ambiguous"]
    assert all(c.reason == "unconfirmed_context" for c in result.changes)
    assert all(c.base is None or c.head is None for c in result.changes)


def test_version_rename_metadata_and_activation_with_same_references(
    tmp_path: Path,
) -> None:
    old = mod(1, "A")
    new = deepcopy(old)
    new.update(modName="Renamed", displayName="Renamed", active=False)
    new["general"]["version"] = "2"
    new["future"] = {"kept": True}
    result = compare(tmp_path, [old], [new])
    assert len(result.changes) == 1
    assert result.changes[0].category == "modified"
    assert result.changes[0].fields == ("active", "metadata", "name", "version")


def test_changed_file_id_is_not_assumed_to_be_an_update(tmp_path: Path) -> None:
    old, new = mod(1, "A"), mod(1, "A")
    new["installed"]["files"][0]["fileid"] = "99"
    new["general"]["version"] = "2"
    result = compare(tmp_path, [old], [new])
    assert [c.category for c in result.changes] == ["ambiguous", "ambiguous"]


def test_add_remove_and_inverse(tmp_path: Path) -> None:
    a = load(tmp_path, "a.json", [mod(1, "A")])
    b = load(tmp_path, "b.json", [mod(2, "B")])
    forward = compare_exports(a, b, context="synthetic")
    reverse = compare_exports(b, a, context="synthetic")
    assert [c.category for c in forward.changes] == ["removed", "added"]
    assert [
        c.base.original.source_id if c.base else c.head.original.source_id
        for c in reverse.changes
    ] == [2, 1]


def test_order_is_relative_to_shared_proven_references(tmp_path: Path) -> None:
    result = compare(tmp_path, [mod(1, "A"), mod(2, "B")], [mod(2, "B"), mod(1, "A")])
    assert [c.category for c in result.changes] == ["reordered", "reordered"]
    shifted = compare(tmp_path, [mod(1, "A")], [mod(2, "B"), mod(1, "A")])
    assert [c.category for c in shifted.changes] == ["unchanged", "added"]


def test_incomplete_counterpart_prevents_false_removal(tmp_path: Path) -> None:
    unknown = mod(2, "Unknown")
    unknown.update(id="Unknown", general={}, installed={})
    result = compare(tmp_path, [mod(1, "A")], [unknown])
    assert all(c.category == "ambiguous" for c in result.changes)


def test_unknown_version_is_metadata_not_a_proven_version_update(
    tmp_path: Path,
) -> None:
    a, b = mod(1, "A"), mod(1, "A")
    a["general"]["version"] = ""
    result = compare(tmp_path, [a], [b])
    assert result.changes[0].fields == ("version_metadata",)


def test_duplicates_are_not_paired_and_counts_are_conserved(tmp_path: Path) -> None:
    data = [mod(1, "A"), mod(1, "B")]
    a = load(tmp_path, "a.json", data)
    b = load(tmp_path, "b.json", deepcopy(data))
    before = asdict(a), asdict(b)
    result = compare_exports(a, b, context="synthetic")
    assert len(result.changes) == 4
    assert all(c.category == "ambiguous" for c in result.changes)
    assert sum(c.base is not None for c in result.changes) == len(a.records)
    assert sum(c.head is not None for c in result.changes) == len(b.records)
    assert before == (asdict(a), asdict(b))
    assert result == compare_exports(a, b, context="synthetic")


def test_invalid_models_and_context_fail_explanatorily(tmp_path: Path) -> None:
    a = load(tmp_path, "a.json", [mod(1, "A")])
    for context in ("", "  ", 1):
        with pytest.raises(ValueError, match="Context"):
            compare_exports(a, a, context=context)
    with pytest.raises(ValueError, match="normalized"):
        compare_exports(None, a)
    forged = replace(
        a,
        records=(
            replace(
                a.records[0],
                identity=replace(a.records[0].identity, state="incomplete"),
            ),
        ),
    )
    with pytest.raises(ValueError, match="inconsistent"):
        compare_exports(forged, a)


def test_independent_golden_and_pure_detached_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    old = [mod(1, "A"), mod(2, "B")]
    new = [mod(2, "B"), mod(1, "A"), mod(3, "C")]
    new[1]["general"]["version"] = "2"
    a, b = load(tmp_path, "a.json", old), load(tmp_path, "b.json", new)
    expected = json.loads(
        (Path(__file__).parent / "fixtures/comparison.expected.json").read_text(
            encoding="utf-8"
        )
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("Comparison must not access files")

    with monkeypatch.context() as ctx:
        ctx.setattr(Path, "open", forbidden)
        ctx.setattr(Path, "stat", forbidden)
        result = compare_exports(a, b, context="synthetic")
    view = [
        dict(
            category=c.category,
            base=c.base.original.index if c.base else None,
            head=c.head.original.index if c.head else None,
            fields=list(c.fields),
        )
        for c in result.changes
    ]
    assert view == expected
    a.records[0].original.general["version"] = "mutated"
    assert result.changes[0].base.original.general["version"] == "1"
