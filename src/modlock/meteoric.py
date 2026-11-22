"""Read the Meteoric JSON shape studied in issue #2, without inferring identity."""

import json
import math
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]
type ErrorCode = Literal[
    "io", "file_type", "size", "encoding", "json", "structure", "unsupported"
]
type WarningCode = Literal["unknown_field", "incomplete_metadata", "metadata_count"]

DEFAULT_MAX_BYTES = 16 * 1024 * 1024
_FIELDS = {
    "id",
    "type",
    "separatorName",
    "modName",
    "displayName",
    "plugins",
    "general",
    "installed",
    "order",
    "tags",
    "active",
}
_GENERAL = {"modid", "version", "newestVersion", "category", "installationFile"}


class ReaderError(ValueError):
    """An input error with a stable category and JSON location, without file content."""

    def __init__(self, code: ErrorCode, location: str, message: str) -> None:
        self.code = code
        self.location = location
        super().__init__(f"{location}: {message}")


@dataclass(frozen=True)
class ReadWarning:
    code: WarningCode
    location: str
    message: str


@dataclass(frozen=True)
class InstalledMetadata:
    size: int | None
    files: tuple[dict[str, str], ...] | None
    raw: JsonObject


@dataclass(frozen=True)
class MeteoricRecord:
    index: int
    kind: Literal["mod", "separator"]
    source_id: int | str | None
    separator_name: str
    mod_name: str
    display_name: str
    plugins: tuple[str, ...]
    general: dict[str, str]
    installed: InstalledMetadata
    order: int
    tags: tuple[str, ...]
    active: bool
    raw: JsonObject


@dataclass(frozen=True)
class MeteoricExport:
    source: Path
    records: tuple[MeteoricRecord, ...]
    warnings: tuple[ReadWarning, ...]


def _object(value: JsonValue, location: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ReaderError("structure", location, "Expected an object.")
    return value


def _expect[T](value: JsonValue, expected: type[T], location: str) -> T:
    # Exact types prevent bool from being accepted as an integer.
    if type(value) is not expected:
        raise ReaderError("structure", location, f"Expected {expected.__name__}.")
    return cast(T, value)


def _strings(value: JsonValue, location: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ReaderError("structure", location, "Expected an array of strings.")
    return tuple(_expect(v, str, f"{location}[{i}]") for i, v in enumerate(value))


def _unknown(
    data: JsonObject, known: set[str], location: str, warnings: list[ReadWarning]
) -> None:
    for _ in sorted(data.keys() - known):
        # Unknown keys may themselves contain private text; retain them in raw only.
        warnings.append(
            ReadWarning("unknown_field", location, "Unknown field preserved.")
        )


def _text_metadata(
    data: JsonObject, known: set[str], location: str, warnings: list[ReadWarning]
) -> dict[str, str]:
    _unknown(data, known, location, warnings)
    empty_required = {"version"} if known == _GENERAL else {"modid", "fileid"}
    if known - data.keys() or any(data.get(key) == "" for key in empty_required):
        warnings.append(
            ReadWarning(
                "incomplete_metadata", location, "Metadata fields are absent or empty."
            )
        )
    return {
        key: _expect(data[key], str, f"{location}.{key}")
        for key in sorted(known & data.keys())
    }


def _installed(
    data: JsonObject, location: str, warnings: list[ReadWarning]
) -> InstalledMetadata:
    _unknown(data, {"size", "files"}, location, warnings)
    size = _expect(data["size"], int, location + ".size") if "size" in data else None
    files = None
    if "files" in data:
        values = data["files"]
        if not isinstance(values, list):
            raise ReaderError("structure", location + ".files", "Expected an array.")
        files = tuple(
            _text_metadata(
                _object(value, f"{location}.files[{i}]"),
                {"modid", "fileid"},
                f"{location}.files[{i}]",
                warnings,
            )
            for i, value in enumerate(values)
        )
    if size is None or files is None:
        warnings.append(
            ReadWarning("incomplete_metadata", location, "Metadata fields are absent.")
        )
    if size is not None and (size < 0 or (files is not None and size != len(files))):
        warnings.append(
            ReadWarning(
                "metadata_count", location, "Declared file count is inconsistent."
            )
        )
    return InstalledMetadata(size, files, data)


def _record(
    value: JsonValue, index: int, section: str, warnings: list[ReadWarning]
) -> MeteoricRecord:
    location = f"$[{index}]"
    data = _object(value, location)
    missing = _FIELDS - data.keys()
    if missing:
        field = sorted(missing)[0]
        raise ReaderError(
            "structure", location + "." + field, "Required field is absent."
        )
    _unknown(data, _FIELDS, location, warnings)
    kind = data["type"]
    if kind not in ("mod", "separator"):
        raise ReaderError("unsupported", location + ".type", "Unsupported record type.")
    order = _expect(data["order"], int, location + ".order")
    if order != index:
        raise ReaderError(
            "structure", location + ".order", "Order must match the array position."
        )
    section_name = _expect(data["separatorName"], str, location + ".separatorName")
    mod_name = _expect(data["modName"], str, location + ".modName")
    display_name = _expect(data["displayName"], str, location + ".displayName")
    active = _expect(data["active"], bool, location + ".active")
    plugins = _strings(data["plugins"], location + ".plugins")
    tags = _strings(data["tags"], location + ".tags")
    general = _object(data["general"], location + ".general")
    installed = _object(data["installed"], location + ".installed")
    source_id = data["id"]
    if kind == "separator":
        if source_id is not None or plugins or general or installed or not active:
            raise ReaderError("structure", location, "Invalid separator fields.")
        if section_name != mod_name:
            raise ReaderError(
                "structure", location + ".separatorName", "Separator names disagree."
            )
        general_values: dict[str, str] = {}
        installed_values = InstalledMetadata(None, None, installed)
    else:
        if not (type(source_id) is str or (type(source_id) is int and source_id > 0)):
            raise ReaderError(
                "structure", location + ".id", "Expected a positive integer or name."
            )
        if section_name != section:
            raise ReaderError(
                "structure", location + ".separatorName", "Section context disagrees."
            )
        general_values = _text_metadata(
            general, _GENERAL, location + ".general", warnings
        )
        installed_values = _installed(installed, location + ".installed", warnings)
    return MeteoricRecord(
        index=index,
        kind=cast(Literal["mod", "separator"], kind),
        source_id=cast(int | str | None, source_id),
        separator_name=section_name,
        mod_name=mod_name,
        display_name=display_name,
        plugins=plugins,
        general=general_values,
        installed=installed_values,
        order=order,
        tags=tags,
        active=active,
        raw=data,
    )


def _pairs(pairs: list[tuple[str, JsonValue]]) -> JsonObject:
    data: JsonObject = {}
    for key, value in pairs:
        if key in data:
            raise ReaderError(
                "json", "$", "Duplicate JSON object keys are unsupported."
            )
        data[key] = value
    return data


def _float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ReaderError("json", "$", "Non-finite numbers are unsupported.")
    return number


def _constant(_: str) -> None:
    raise ReaderError("json", "$", "Non-standard JSON constants are unsupported.")


def read_meteoric(
    path: str | Path, *, max_bytes: int = DEFAULT_MAX_BYTES
) -> MeteoricExport:
    """Read one regular file. Never follow paths named inside its JSON fields.

    UTF-8 with/without BOM is accepted. The limit bounds the bytes read, including
    BOM. Warnings retain partial metadata; errors do not repair or rewrite input.
    The shape is supported; the file's producer/version cannot be authenticated.
    """
    if type(max_bytes) is not int or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer")
    source = Path(path)
    try:
        info = source.stat()
        if not stat.S_ISREG(info.st_mode):
            raise ReaderError("file_type", "$", "Expected a regular file.")
        if info.st_size > max_bytes:
            raise ReaderError("size", "$", "Export exceeds the configured byte limit.")
        with source.open("rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise ReaderError("file_type", "$", "Expected a regular file.")
            raw = stream.read(max_bytes + 1)
    except FileNotFoundError:
        raise ReaderError("io", "$", "Export file not found.") from None
    except PermissionError:
        raise ReaderError("io", "$", "Export file is not readable.") from None
    except OSError:
        raise ReaderError("io", "$", "Unable to read export file.") from None
    except ValueError as exc:
        if isinstance(exc, ReaderError):
            raise
        raise ReaderError("io", "$", "Invalid export path.") from None
    if len(raw) > max_bytes:
        raise ReaderError("size", "$", "Export exceeds the configured byte limit.")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ReaderError(
            "encoding", "$", "Expected UTF-8, optionally with BOM."
        ) from None
    try:
        data = json.loads(
            text, object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_float
        )
    except json.JSONDecodeError as exc:
        raise ReaderError(
            "json", "$", f"Invalid JSON at line {exc.lineno}, column {exc.colno}."
        ) from None
    except (RecursionError, ValueError) as exc:
        if isinstance(exc, ReaderError):
            raise
        raise ReaderError(
            "json", "$", "JSON exceeds supported decoder limits."
        ) from None
    if not isinstance(data, list):
        raise ReaderError("structure", "$", "Expected an array of records.")
    warnings: list[ReadWarning] = []
    records = []
    section = "Unsectioned"
    for index, value in enumerate(data):
        record = _record(value, index, section, warnings)
        records.append(record)
        if record.kind == "separator":
            section = record.separator_name
    return MeteoricExport(source, tuple(records), tuple(warnings))
