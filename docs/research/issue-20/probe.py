"""Research assertions only: no MO2 parser, conversion or product implementation."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    folder = Path(__file__).resolve().parent
    root = folder.parents[2]
    scenarios = json.loads((folder / "scenarios.json").read_text(encoding="utf-8"))
    a, b = scenarios["a"], scenarios["b"]
    assert (folder / "fixtures" / a["fixture"]).read_bytes() == (
        folder / "fixtures" / b["fixture"]
    ).read_bytes()
    assert a["file_id"] != b["file_id"] and a["version"] != b["version"]
    results = []
    for path in sorted((folder / "fixtures").glob("*.txt")):
        before = path.read_bytes()
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "modlock",
                "compare",
                str(path),
                str(path),
                "--audit",
            ],
            cwd=root,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 1 and b"Error [json]" in result.stderr
        assert b"Traceback" not in result.stderr
        assert path.read_bytes() == before
        results.append(
            {
                "fixture": path.name,
                "sha256": hashlib.sha256(before).hexdigest(),
                "current_cli_exit": result.returncode,
                "unchanged": True,
            }
        )
    assert len(results) == 6
    print(
        json.dumps(
            {
                "decision": "RECHAZAR_FORMATO_AISLADO_AHORA",
                "identical_text_distinct_synthetic_variants": True,
                "producer_executed": False,
                "parser_implemented": False,
                "cases": results,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
