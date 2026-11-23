"""Synthetic identity evidence; no cross-export matching or product serialization."""

import json
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

import pytest

from modlock.identity import FileReference, NormalizedExport, normalize_export
from modlock.meteoric import read_meteoric

FIXTURES = Path(__file__).parent / "fixtures/identity"


def _mod() -> dict:
    data = json.loads((FIXTURES / "export.json").read_text(encoding="utf-8"))[1]
    data["order"] = 0
    data["separatorName"] = "Unsectioned"
    return data


def _read(tmp_path: Path, records: list[dict], name: str = "export.json"):
    path = tmp_path / name
    for index, record in enumerate(records):
        record["order"] = index
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return read_meteoric(path)


def _view(result: NormalizedExport) -> list[dict]:
    # A test-only golden view, not a public schema, report, or export standard.
    return [
        dict(
            index=record.original.index,
            state=record.identity.state,
            references=[[r.page_id, r.file_id] for r in record.identity.references],
            reasons=list(record.identity.reasons),
            conflicting_indices=list(record.identity.conflicting_indices),
        )
        for record in result.records
    ]


def test_independent_golden_repeatability_and_no_data_loss() -> None:
    path = FIXTURES / "export.json"
    before = path.read_bytes()
    source = read_meteoric(path)
    original = asdict(source)

    result = normalize_export(source)
    repeated = normalize_export(read_meteoric(path))

    expected = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
    assert _view(result) == expected
    assert result == repeated
    assert json.dumps(_view(result), sort_keys=True) == json.dumps(
        _view(repeated), sort_keys=True
    )
    assert [asdict(r.original) for r in result.records] == [
        asdict(r) for r in source.records
    ]
    assert result.source == source.source
    assert result.read_warnings == source.warnings
    assert asdict(source) == original
    assert path.read_bytes() == before
    assert result.records[1].original.active is False
    assert result.records[1].original.general["version"] == "d2026.11.22.0"
    assert result.records[1].original.raw["future"] == {"note": "synthetic only"}


def test_provenance_remains_separate_from_equivalent_identity_data(
    tmp_path: Path,
) -> None:
    first = normalize_export(_read(tmp_path, [_mod()], "one.json"))
    second = normalize_export(_read(tmp_path, [_mod()], "two.json"))
    assert first.records == second.records
    assert _view(first) == _view(second)
    assert first.source != second.source


def test_empty_export_stays_empty(tmp_path: Path) -> None:
    source = _read(tmp_path, [])
    result = normalize_export(source)
    assert result.source == source.source
    assert result.records == ()
    assert result.read_warnings == ()


@pytest.mark.parametrize("token", ["42", "00042"])
def test_ascii_numeric_references_normalize_without_rewriting_originals(
    tmp_path: Path, token: str
) -> None:
    record = _mod()
    record["installed"]["files"][0]["fileid"] = token
    result = normalize_export(_read(tmp_path, [record])).records[0]
    assert result.identity.state == "referenced"
    assert result.identity.references == (FileReference(101, 42),)
    assert result.original.installed.files[0]["fileid"] == token


@pytest.mark.parametrize(
    "token", ["", "0", "-1", "+42", " 42", "42 ", "٤٢", "4.2", "abc"]
)
def test_invalid_file_reference_is_incomplete_without_guessing(
    tmp_path: Path, token: str
) -> None:
    record = _mod()
    record["installed"]["files"][0]["fileid"] = token
    result = normalize_export(_read(tmp_path, [record])).records[0]
    assert result.identity.state == "incomplete"
    assert result.identity.references == ()
    assert "missing_file_reference" in result.identity.reasons
    assert result.original.installed.files[0]["fileid"] == token


def test_textual_top_level_id_never_becomes_a_nexus_id(tmp_path: Path) -> None:
    record = _mod()
    record["id"] = "101"
    result = normalize_export(_read(tmp_path, [record])).records[0]
    assert result.identity.state == "incomplete"
    assert result.identity.reasons == ("missing_page_id",)
    assert result.identity.references == (FileReference(101, 1001),)
    assert result.original.source_id == "101"


@pytest.mark.parametrize("declared", ["999", "not-numeric"])
def test_conflicting_or_invalid_page_metadata_stays_ambiguous(
    tmp_path: Path, declared: str
) -> None:
    record = _mod()
    record["general"]["modid"] = declared
    result = normalize_export(_read(tmp_path, [record])).records[0]
    assert result.identity.state == "ambiguous"
    assert result.identity.reasons == ("conflicting_page_id",)
    assert result.original.general["modid"] == declared


def test_conflicting_file_page_is_not_replaced_by_top_level_id(tmp_path: Path) -> None:
    record = _mod()
    record["installed"]["files"][0]["modid"] = "999"
    result = normalize_export(_read(tmp_path, [record])).records[0]
    assert result.identity.state == "ambiguous"
    assert result.identity.references == (FileReference(999, 1001),)
    assert result.original.source_id == 101


def test_unknown_version_does_not_change_or_fabricate_file_references(
    tmp_path: Path,
) -> None:
    record = _mod()
    record["general"]["version"] = ""
    record["general"]["modid"] = ""
    result = normalize_export(_read(tmp_path, [record]))
    assert result.records[0].identity.state == "referenced"
    assert result.records[0].original.general["version"] == ""
    assert result.read_warnings


@pytest.mark.parametrize(
    "installed",
    [{}, {"size": 0, "files": []}, {"files": [{}]}, {"size": -1, "files": []}],
)
def test_missing_and_partial_file_lists_remain_incomplete(
    tmp_path: Path, installed: dict
) -> None:
    record = _mod()
    record["installed"] = installed
    source = _read(tmp_path, [record])
    result = normalize_export(source)
    assert result.records[0].identity.state == "incomplete"
    assert result.records[0].original.installed == source.records[0].installed
    assert result.records[0].identity.references == ()


def test_repeated_reference_within_one_record_is_not_deduplicated(
    tmp_path: Path,
) -> None:
    record = _mod()
    file = record["installed"]["files"][0]
    record["installed"] = {"size": 2, "files": [file, deepcopy(file)]}
    result = normalize_export(_read(tmp_path, [record])).records[0]
    assert result.identity.state == "ambiguous"
    assert result.identity.reasons == ("duplicate_reference",)
    assert result.identity.references == (
        FileReference(101, 1001),
        FileReference(101, 1001),
    )
    assert result.identity.conflicting_indices == ()
    assert len(result.original.installed.files) == 2


def test_partial_reference_overlap_marks_all_records_without_merging(
    tmp_path: Path,
) -> None:
    first, second = _mod(), _mod()
    first["installed"] = {
        "size": 2,
        "files": [{"modid": "101", "fileid": "2"}, {"modid": "101", "fileid": "1"}],
    }
    second.update(modName="Other", displayName="Other")
    second["installed"] = {
        "size": 2,
        "files": [{"modid": "00101", "fileid": "02"}, {"modid": "101", "fileid": "3"}],
    }
    result = normalize_export(_read(tmp_path, [first, second]))
    assert len(result.records) == 2
    assert [r.identity.state for r in result.records] == ["ambiguous", "ambiguous"]
    assert [r.identity.conflicting_indices for r in result.records] == [(1,), (0,)]
    assert result.records[0].identity.references == (
        FileReference(101, 1),
        FileReference(101, 2),
    )
    assert [f["fileid"] for f in result.records[0].original.installed.files] == [
        "2",
        "1",
    ]


def test_same_file_number_on_different_pages_is_not_a_duplicate(tmp_path: Path) -> None:
    first, second = _mod(), _mod()
    second.update(id=202, modName="Other", displayName="Other")
    second["general"]["modid"] = "202"
    second["installed"]["files"][0]["modid"] = "202"
    result = normalize_export(_read(tmp_path, [first, second]))
    assert [r.identity.state for r in result.records] == ["referenced", "referenced"]


@pytest.mark.parametrize("names", [("Alpha", "ALPHA"), ("Straße", "STRASSE")])
def test_casefold_only_warns_about_collisions_without_rewriting_names(
    tmp_path: Path, names: tuple[str, str]
) -> None:
    records = [_mod(), _mod()]
    for i, (record, name) in enumerate(zip(records, names, strict=True)):
        record.update(modName=name, displayName=name)
        record["installed"]["files"][0]["fileid"] = str(i + 1)
    result = normalize_export(_read(tmp_path, records))
    assert [r.original.mod_name for r in result.records] == list(names)
    assert [r.identity.state for r in result.records] == ["ambiguous", "ambiguous"]
    assert all(r.identity.reasons == ("name_collision",) for r in result.records)


def test_unicode_composition_is_not_silently_normalized(tmp_path: Path) -> None:
    names = ["Café", "Cafe\u0301"]
    records = [_mod(), _mod()]
    for i, (record, name) in enumerate(zip(records, names, strict=True)):
        record.update(modName=name, displayName=name)
        record["installed"]["files"][0]["fileid"] = str(i + 1)
    result = normalize_export(_read(tmp_path, records))
    assert [r.original.mod_name for r in result.records] == names
    assert all(r.identity.state == "referenced" for r in result.records)


def test_normalization_is_detached_and_performs_no_file_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _read(tmp_path, [_mod()])
    before = asdict(source)

    def forbidden(*args, **kwargs):
        raise AssertionError("normalize_export must not touch the filesystem")

    with monkeypatch.context() as context:
        context.setattr(Path, "open", forbidden)
        context.setattr(Path, "stat", forbidden)
        result = normalize_export(source)
    assert asdict(source) == before
    source.records[0].raw["future"]["note"] = "changed in source"
    assert result.records[0].original.raw["future"]["note"] == "synthetic only"
    result.records[0].original.general["version"] = "changed in result"
    assert source.records[0].general["version"] == "d2026.11.22.0"
