"""Fixed-corpus experiment, not a modlock parser or product CLI.

Usage: python run.py METEORIC_CHECKOUT NEW_OUTPUT_DIRECTORY
Only standard library and the separately checked out upstream code are used.
"""
from __future__ import annotations

import copy
import configparser
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import subprocess
import sys
from types import ModuleType, SimpleNamespace
from collections import Counter

COMMIT = "1e34b9918a81239b71789a5472f6bc16ffdab70b"
HERE = Path(__file__).resolve().parent


def mod(name: str, page: int = 101, file: str = "1001") -> dict:
    return dict(id=page, type="mod", separatorName="Core", modName=name,
                displayName=name, plugins=[], general=dict(modid=str(page),
                version="1.0.0.0", newestVersion="1.0.0.0", category="",
                installationFile=""), installed=dict(size=1, files=[
                    dict(modid=str(page), fileid=file)]), order=0, tags=[], active=True)


def local(display: str, name: str) -> dict:
    item = mod(name)
    item.update(id=name, displayName=display, general={}, installed={})
    item["tags"] = [display[1:display.index("]")]] if display.startswith("[") else []
    return item


def export(items: list[dict], sections: tuple[str, ...] = ("Core",)) -> list[dict]:
    data = []
    for section in sections:
        data.append(dict(id=None, type="separator", separatorName=section,
                         modName=section, displayName=section + "_separator",
                         plugins=[], general={}, installed={}, order=0, tags=[], active=True))
        data.extend(copy.deepcopy([m for m in items if m["separatorName"] == section]))
    for i, item in enumerate(data):
        item["order"] = i
    return data


def corpus() -> dict[str, tuple[list, list]]:
    a, b = mod("Synthetic Alpha"), mod("Synthetic Birch", 202, "2002")
    cases = {"01-identical": (export([a]), export([a]))}
    changed = copy.deepcopy(a)
    changed["general"].update(version="2.0.0.0", newestVersion="2.0.0.0")
    changed["installed"]["files"][0]["fileid"] = "1002"
    cases["02-version"] = export([a]), export([changed])
    cases["03-order"] = export([a, b]), export([b, a])
    moved = copy.deepcopy(a)
    moved["separatorName"] = "Extras"
    cases["04-section"] = export([a, b], ("Core", "Extras")), export([b, moved], ("Core", "Extras"))
    cases["05-fuzzy"] = (export([local("Synthetic Texture Kit", "Synthetic Texture Kit")]),
                         export([local("Synthetic Texture Kits", "Synthetic Texture Kits")]))
    variant = mod("Synthetic Alpha Optional", 101, "1003")
    cases["06-shared-page"] = export([a, variant]), export([variant, a])
    one, two = local("[A] Local Patch", "Local Patch"), local("[B] Local Patch", "Local Patch")
    cases["07-ambiguous"] = export([one, two]), export([two, one])
    empty = local("Local Output", "Local Output")
    cases["08-missing-meta"] = export([empty]), export([empty])
    changed = copy.deepcopy(a)
    changed["installed"]["files"][0]["fileid"] = "1009"
    cases["09-file-change"] = export([a]), export([changed])
    disabled = copy.deepcopy(a)
    disabled["active"] = False
    cases["10-active"] = export([a]), export([disabled])
    return cases


def dump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def check_exporter(data: list[dict], directory: Path, exporter: ModuleType) -> None:
    """Run the real exporter against a synthetic MO2 API and synthetic meta.ini.

    This checks export reachability, not integration with a running MO2 instance.
    """
    by_name, states = {}, {}
    for i, item in enumerate(data):
        path = directory / str(i)
        path.mkdir(parents=True)
        config = configparser.ConfigParser()
        if item["general"]:
            config["General"] = item["general"]
        if item["installed"]:
            config["installedFiles"] = {"size": str(item["installed"]["size"])}
            for j, file in enumerate(item["installed"]["files"], 1):
                for key, value in file.items():
                    config["installedFiles"][f"{j}\\{key}"] = value
        if config.sections():
            with (path / "meta.ini").open("w", encoding="utf-8") as stream:
                config.write(stream)
        by_name[item["displayName"]] = SimpleNamespace(
            isSeparator=lambda item=item: item["type"] == "separator",
            absolutePath=lambda path=path: str(path),
            nexusId=lambda item=item: item["id"] if type(item["id"]) is int else 0)
        states[item["displayName"]] = int(item["active"])
    assert len(by_name) == len(data), "MO2 display names must be unique"
    modlist = SimpleNamespace(allModsByProfilePriority=lambda: list(by_name), state=states.__getitem__)
    organizer = SimpleNamespace(modList=lambda: modlist, getMod=by_name.__getitem__)
    sys.modules["mobase"] = SimpleNamespace(ModState=SimpleNamespace(ACTIVE=1))
    assert exporter.export_modlist(organizer) == data, "Real exporter did not reproduce fixture"


def reference_coverage(items: list[dict]) -> dict:
    """M1: explicit version plus locally unique, complete Nexus file references."""
    mods = [m for m in items if m["type"] == "mod"]
    keys = [[(m["id"], f["fileid"]) for f in m["installed"].get("files", [])
             if type(m["id"]) is int and f["modid"] == str(m["id"]) and f["fileid"].isdigit()
             and int(f["fileid"]) > 0] for m in mods]
    counts = Counter(k for group in keys for k in group)
    complete = sum(bool(group) and len(group) == m["installed"].get("size")
                   and all(counts[k] == 1 for k in group)
                   and m["general"].get("version", "").strip() not in ("", "Unknown")
                   for m, group in zip(mods, keys))
    return dict(complete=complete, total=len(mods))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python run.py METEORIC_CHECKOUT NEW_OUTPUT_DIRECTORY")
    upstream, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    sha = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if sha != COMMIT:
        raise ValueError(f"Expected Meteoric {COMMIT}, received {sha}")
    if subprocess.check_output(["git", "-C", str(upstream), "status", "--porcelain", "--untracked-files=no"], text=True).strip():
        raise ValueError("Meteoric tracked files must be unmodified")
    output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(upstream / "tools"))
    import modlist_utils as utils
    import generate_diff as diff
    import generate_coverage as coverage
    spec = importlib.util.spec_from_file_location("experiment_exporter", upstream / "mo2-plugins/modlist_compare/exporter_core.py")
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load the pinned Meteoric exporter")
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)

    results = []
    for case, (old, new) in corpus().items():
        fixture = HERE / "fixtures" / case
        # These are fixed synthetic exports, never user-supplied data.
        for label, data in (("old", old), ("new", new)):
            check_exporter(data, output / "synthetic-mo2" / case / label, exporter)
            text = dump(data)
            path = fixture / (label + ".json")
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")
            if path.read_text(encoding="utf-8") != text:
                raise ValueError(f"Fixture differs from documented experiment: {path}")
        oldmods, newmods = utils.extract_mods(old), utils.extract_mods(new)
        matched, added, removed = utils.match_mods(oldmods, newmods)
        pairs = lambda ms: sorted((a["displayName"], b["displayName"]) for a, b in ms)
        baseline = pairs(matched)
        variants = [pairs(utils.match_mods(list(o), list(n))[0])
                    for o in itertools.permutations(oldmods)
                    for n in itertools.permutations(newmods)]
        stable = sum(all(pair in variant for variant in variants) for pair in baseline)
        section_matches, _, _ = diff.match_sections(utils.get_separator_order(old), utils.get_separator_order(new), matched)
        changes = diff.classify_mod_changes(matched, {utils.name_key(a): utils.name_key(b) for a, b in section_matches})
        rows = coverage.classify_source_mods(new, old, 0.80, None)
        states = Counter(row.state.value for section in rows.values() for row in section)
        case_out = output / case
        case_out.mkdir()
        hashes = {}
        before = {label: hashlib.sha256((fixture / (label + ".json")).read_bytes()).hexdigest()
                  for label in ("old", "new")}
        for tool, filename, first, second in (
                ("generate_changelog.py", "changelog.md", "old", "new"),
                ("generate_diff.py", "diff.html", "old", "new"),
                ("generate_coverage.py", "coverage.html", "new", "old")):
            command = [sys.executable, str(upstream / "tools" / tool),
                       str(fixture / (first + ".json")), str(fixture / (second + ".json")),
                       "-o", str(case_out / filename)]
            subprocess.run(command, check=True, capture_output=True)
            first_bytes = (case_out / filename).read_bytes()
            subprocess.run(command, check=True, capture_output=True)
            assert first_bytes == (case_out / filename).read_bytes(), (case, tool, "nondeterministic")
            hashes[filename] = hashlib.sha256(first_bytes).hexdigest()
        assert before == {label: hashlib.sha256((fixture / (label + ".json")).read_bytes()).hexdigest()
                          for label in ("old", "new")}, "Input changed"
        results.append(dict(case=case, matched=baseline, added=pairs([(m, m) for m in added]),
                            removed=pairs([(m, m) for m in removed]), updated=utils.classify_updates(matched),
                            diff_changes=[dict(old=a["displayName"], new=b["displayName"], flags=c.value)
                                          for a, b, c, _, _ in changes], coverage=dict(states),
                            reference_coverage=dict(old=reference_coverage(old), new=reference_coverage(new)),
                            matching_stability=dict(stable=stable, total=len(baseline), permutations=len(variants),
                                                    distinct_pairings=len({dump(v) for v in variants})),
                            input_sha256=before, output_sha256=hashes))
    indexed = {r["case"]: r for r in results}
    assert len(indexed["02-version"]["updated"]) == 1
    assert [c["flags"] for c in indexed["03-order"]["diff_changes"]] == [0, 0]
    assert sum(c["flags"] == 4 for c in indexed["04-section"]["diff_changes"]) == 1
    assert indexed["07-ambiguous"]["matching_stability"]["stable"] == 0
    assert indexed["07-ambiguous"]["matching_stability"]["distinct_pairings"] == 2
    assert indexed["08-missing-meta"]["reference_coverage"]["new"]["complete"] == 0
    for case in ("09-file-change", "10-active"):
        assert indexed[case]["coverage"] == {"common": 1}
        assert indexed[case]["updated"] == []
    (output / "results.json").write_text(dump(dict(meteoric_commit=sha, python=platform.python_version(),
                                                  cases=results)), encoding="utf-8", newline="\n")
    print(f"PASS: {len(results)} pairs, 20 real exporter roundtrips with synthetic MO2 API, "
          "60 CLI executions, identical repeat outputs, intact inputs, expected findings")


if __name__ == "__main__":
    main()
