"""Run every example with the .NET 11 SDK and save its output to slides/outputs.json.
The slide builder (slides/build_deck.py) shows these real outputs on the slides.
Usage:  python run_examples.py            (all examples)
        python run_examples.py linq       (only files whose path contains "linq")"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "slides" / "outputs.json"
ENV = {**os.environ, "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"}
RUNS = {"04-sdk/app.cs": [[], ["-e", "GREETING=Hallo"]]}     # extra runs with options

results = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
only = sys.argv[1] if len(sys.argv) > 1 else ""
files = sorted(p for p in (ROOT / "examples").rglob("*.cs")
               if p.parent.name in {"01-csharp15", "02-libraries", "03-runtime", "04-sdk"} and p.name != "helpers.cs")
for f in files:
    key = f.relative_to(ROOT / "examples").as_posix()
    if only not in key:
        continue
    for extra in RUNS.get(key, [[]]):
        name = key + ("" if not extra else " " + " ".join(extra))
        cmd = ["dotnet", "run", *extra, f.name]
        p = subprocess.run(cmd, cwd=f.parent, capture_output=True, text=True, encoding="utf-8", env=ENV)
        text = p.stdout if p.returncode == 0 else p.stdout + p.stderr
        # first runs also print build warnings (trimming/AOT analyzers); keep only the program output
        out = "\n".join(l for l in text.splitlines() if ": warning " not in l).rstrip()
        results[name] = {"ok": p.returncode == 0, "output": out}
        print(f"{'OK  ' if p.returncode == 0 else 'FAIL'} {name}")
        if p.returncode != 0:
            print("     " + out.replace("\n", "\n     ")[:1500])
OUT.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
