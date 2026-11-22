"""Read existing issue #2 fixtures and adversarial synthetic inputs without writes."""

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from modlock.meteoric import ReaderError, read_meteoric

CORPUS = Path(__file__).resolve().parents[1] / "docs/research/issue-2"
CASES = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))["fixtures"]


def _base() -> list[dict]:
    return json.loads(
        (CORPUS / "fixtures/valid/04-empty-sections.json").read_text(encoding="utf-8")
    )


def _write(tmp_path: Path, data: object) -> Path:
    path = tmp_path / "Café export.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


@pytest.mark.parametrize("case", CASES, ids=[case["path"] for case in CASES])
def test_issue_two_corpus_is_repeatable_and_unchanged(case: dict) -> None:
    path = CORPUS / "fixtures" / case["path"]
    before = path.read_bytes()
    assert hashlib.sha256(before).hexdigest() == case["sha256"]
    try:
        if case["kind"] == "invalid":
            with pytest.raises(ReaderError) as first:
                read_meteoric(path)
            with pytest.raises(ReaderError) as second:
                read_meteoric(path)
            expected = {
                "utf8": "encoding",
                "json-syntax": "json",
                "unsupported-type": "unsupported",
            }
            assert first.value.code == expected.get(case["rule"], "structure")
            assert str(first.value) == str(second.value)
            assert first.value.location.startswith("$")
        else:
            result = read_meteoric(path)
            assert result == read_meteoric(path)
            assert [record.raw for record in result.records] == json.loads(before)
            assert [record.index for record in result.records] == list(
                range(len(result.records))
            )
            if case["kind"] == "anomalous":
                assert any(w.code == "metadata_count" for w in result.warnings)
    finally:
        assert path.read_bytes() == before


def test_unknown_fields_survive_at_every_object_level(tmp_path: Path) -> None:
    data = _base()
    data[0]["future"] = {"nested": [False, 3.5]}
    data[0]["general"]["future"] = ["uninterpreted"]
    data[0]["installed"].update(
        size=1, files=[{"modid": "", "future": {"x": True}}], future=42
    )
    path = _write(tmp_path, data)

    result = read_meteoric(path)

    assert result.records[0].raw == data[0]
    assert result.records[0].installed.raw == data[0]["installed"]
    assert result.records[0].installed.files == ({"modid": ""},)
    assert [w.location for w in result.warnings if w.code == "unknown_field"] == [
        "$[0]",
        "$[0].general",
        "$[0].installed",
        "$[0].installed.files[0]",
    ]
    assert any(w.code == "incomplete_metadata" for w in result.warnings)


def test_missing_empty_and_partial_metadata_are_not_invented(tmp_path: Path) -> None:
    data = _base()
    original = read_meteoric(_write(tmp_path, data)).records[0]
    assert original.general["version"] == ""
    assert original.installed.size == 0
    assert original.installed.files == ()

    data[0].update(general={}, installed={"files": [{}]})
    partial = read_meteoric(_write(tmp_path, data))
    assert partial.records[0].general.get("version") is None
    assert partial.records[0].installed.size is None
    assert partial.records[0].installed.files == ({},)
    assert partial.records[0].installed.files[0].get("fileid") is None
    assert all(w.code == "incomplete_metadata" for w in partial.warnings)


def test_collisions_and_activation_are_preserved_without_identity_decisions() -> None:
    collision = read_meteoric(CORPUS / "fixtures/valid/05-name-collision.json")
    assert len(collision.records) == 2
    assert collision.records[0].mod_name == collision.records[1].mod_name
    assert [r.display_name for r in collision.records] == [
        "[A] Local Patch",
        "[B] Local Patch",
    ]
    metadata = read_meteoric(CORPUS / "fixtures/valid/03-metadata.json")
    mod = metadata.records[1]
    assert mod.active is False
    assert mod.source_id == 91001
    assert mod.general["version"] == "d2026.11.22.0"
    assert len(mod.installed.files) == 2


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", True),
        ("id", 1.5),
        ("id", 0),
        ("order", False),
        ("plugins", [7]),
        ("tags", None),
        ("general", {"version": 3}),
        ("installed", {"size": True}),
        ("installed", {"files": {}}),
        ("installed", {"files": [None]}),
        ("installed", {"files": [{"fileid": 4}]}),
    ],
)
def test_wrong_known_types_are_not_coerced(
    tmp_path: Path, field: str, value: object
) -> None:
    data = _base()
    data[0][field] = value
    path = _write(tmp_path, data)
    before = path.read_bytes()
    with pytest.raises(ReaderError, match=r"\$\[0\]") as error:
        read_meteoric(path)
    assert error.value.code == "structure"
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", 1),
        ("active", False),
        ("plugins", ["a.esp"]),
        ("general", {"version": "1"}),
    ],
)
def test_separator_invariants(tmp_path: Path, field: str, value: object) -> None:
    data = json.loads(
        (CORPUS / "fixtures/valid/06-separator-only.json").read_text(encoding="utf-8")
    )
    data[0][field] = value
    with pytest.raises(ReaderError) as error:
        read_meteoric(_write(tmp_path, data))
    assert error.value.code == "structure"


@pytest.mark.parametrize(
    "raw",
    [
        b"",
        b"  \n",
        b"[NaN]",
        b"[Infinity]",
        b"[1e9999]",
        b'{"private-key":1,"private-key":2}',
    ],
)
def test_decoder_errors_do_not_expose_content(tmp_path: Path, raw: bytes) -> None:
    path = tmp_path / "private-file.json"
    path.write_bytes(raw)
    with pytest.raises(ReaderError) as error:
        read_meteoric(path)
    assert error.value.code == "json"
    assert "private" not in str(error.value)
    assert path.read_bytes() == raw


def test_deep_array_fails_without_an_unhandled_recursion_error(tmp_path: Path) -> None:
    path = tmp_path / "nested.json"
    raw = b"[" * 2000 + b"]" * 2000
    path.write_bytes(raw)
    with pytest.raises(ReaderError) as error:
        read_meteoric(path)
    # A decoder may hit its own depth bound before we can reject the non-object record.
    assert error.value.code in {"json", "structure"}
    assert path.read_bytes() == raw


def test_utf8_bom_and_unicode_are_supported(tmp_path: Path) -> None:
    raw = (CORPUS / "fixtures/valid/02-unsectioned-unicode.json").read_bytes()
    path = tmp_path / "á.json"
    path.write_bytes(b"\xef\xbb\xbf" + raw)
    result = read_meteoric(path)
    assert "Café" in result.records[0].display_name
    assert result.records[0].separator_name == "Unsectioned"
    assert result.records[0].plugins == ("A.ESM", "Parche.esp", "z.esl")
    assert path.read_bytes() == b"\xef\xbb\xbf" + raw


def test_utf16_is_rejected_without_reencoding(tmp_path: Path) -> None:
    path = tmp_path / "utf16.json"
    path.write_bytes("[]".encode("utf-16"))
    with pytest.raises(ReaderError) as error:
        read_meteoric(path)
    assert error.value.code == "encoding"


@pytest.mark.parametrize("limit", [0, -1, True, "16"])
def test_invalid_size_configuration(tmp_path: Path, limit: object) -> None:
    with pytest.raises(ValueError, match="max_bytes"):
        read_meteoric(tmp_path / "not-read.json", max_bytes=limit)


def test_size_limit_is_inclusive(tmp_path: Path) -> None:
    path = _write(tmp_path, [])
    assert read_meteoric(path, max_bytes=2).records == ()
    with pytest.raises(ReaderError) as error:
        read_meteoric(path, max_bytes=1)
    assert error.value.code == "size"
    assert path.read_bytes() == b"[]"


def test_read_bound_is_enforced_even_if_stat_underestimates(
    tmp_path: Path, monkeypatch
) -> None:
    path = _write(tmp_path, [1, 2, 3])
    mode = path.stat().st_mode
    monkeypatch.setattr(
        Path, "stat", lambda _: SimpleNamespace(st_mode=mode, st_size=0)
    )
    with pytest.raises(ReaderError) as error:
        read_meteoric(path, max_bytes=2)
    assert error.value.code == "size"


def test_missing_file_and_directory_have_useful_errors(tmp_path: Path) -> None:
    with pytest.raises(ReaderError, match="not found") as missing:
        read_meteoric(tmp_path / "absent.json")
    assert missing.value.code == "io"
    with pytest.raises(ReaderError) as directory:
        read_meteoric(tmp_path)
    assert directory.value.code == "file_type"


def test_invalid_path_has_a_controlled_error() -> None:
    with pytest.raises(ReaderError, match="Invalid export path") as error:
        read_meteoric("invalid\x00path.json")
    assert error.value.code == "io"


def test_permission_error_is_wrapped_without_private_paths(
    tmp_path: Path, monkeypatch
) -> None:
    path = _write(tmp_path, [])

    def denied(*args, **kwargs):
        raise PermissionError("private path")

    monkeypatch.setattr(Path, "open", denied)
    with pytest.raises(ReaderError, match="not readable") as error:
        read_meteoric(path)
    assert error.value.code == "io"
    assert "private" not in str(error.value)


def test_only_the_requested_file_is_opened_and_only_in_binary_read_mode(
    tmp_path: Path, monkeypatch
) -> None:
    data = _base()
    data[0]["general"]["installationFile"] = str(tmp_path / "do-not-read.zip")
    data[0]["plugins"] = [str(tmp_path / "do-not-read.esp")]
    path = _write(tmp_path, data)
    before = path.read_bytes()
    calls = []
    original = Path.open

    def tracked(self, *args, **kwargs):
        calls.append((self, args, kwargs))
        return original(self, *args, **kwargs)

    with monkeypatch.context() as context:
        context.setattr(Path, "open", tracked)
        read_meteoric(path)
    assert calls == [(path, ("rb",), {})]
    assert path.read_bytes() == before
