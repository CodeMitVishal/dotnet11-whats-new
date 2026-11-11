# .NET 11: What's new

A 34-slide talk about **.NET 11** (released 10 November 2026) with **18 small, runnable examples**.
Every output shown on the slides is the real output of these examples, run with the .NET 11 SDK (11.0.100).

📄 **Slides:** [`slides/dotnet11-whats-new.pdf`](slides/dotnet11-whats-new.pdf) · 🗣️ **Speaker script:** [`SPEAKER_NOTES.md`](SPEAKER_NOTES.md)

## What's covered

| Part | Topics |
|---|---|
| The release | STS, 2 years of support (until 14 Nov 2028); .NET 8 and 9 are out of support |
| 1 · C# 15 | union types, closed hierarchies, collection expression arguments `with(...)`, extension indexers, labeled `break`/`continue`, memory safety (preview) |
| 2 · Libraries | `Process.RunAndCaptureTextAsync`, LINQ `FullJoin`, `EqualityComparer<T>.Create`, generic `Random`, JSON unions + JSON Lines, `StringStream`, Zstandard, async validation, `Decimal32/64/128` |
| 3 · Runtime | Runtime Async (13 → 5 stack frames), JIT improvements, SIMD lane APIs, new minimum CPU (x86-64-v2) |
| 4 · SDK & tooling | file-based apps with `#:include`, `dotnet run -e`, Native AOT CLI, `dotnet test` options, solution filters |
| Ecosystem & upgrade | ASP.NET Core 11, EF Core 11, MAUI, AI; a 4-step upgrade checklist |

## Run the examples

You need the [.NET 11 SDK](https://dotnet.microsoft.com/download/dotnet/11.0). Every example is a **file-based app**: one `.cs` file, no project file.

```bash
git clone https://github.com/CodeMitVishal/dotnet11-whats-new
cd dotnet11-whats-new/examples/01-csharp15
dotnet run 01-union-types.cs
```

| Folder | Examples |
|---|---|
| [`examples/01-csharp15`](examples/01-csharp15) | `01-union-types` · `02-union-result` · `03-closed-hierarchies` · `04-collection-expression-args` · `05-extension-indexers` · `06-labeled-break-continue` · `07-memory-safety` |
| [`examples/02-libraries`](examples/02-libraries) | `01-process-run` · `02-linq-joins` · `03-comparer-and-random` · `04-json-unions-and-jsonl` · `05-streams-and-zstandard` · `06-async-validation` · `07-decimal-types` |
| [`examples/03-runtime`](examples/03-runtime) | `01-stack-trace-classic` · `02-stack-trace-runtime-async` · `03-simd-lanes` |
| [`examples/04-sdk`](examples/04-sdk) | `app.cs` (+ `helpers.cs`, `models/customer.cs` via `#:include`); try `dotnet run -e GREETING=Hallo app.cs` |

Notes:
- The first run of each file builds it, so it takes a few seconds; later runs are fast.
- File-based apps use Native AOT settings by default, so you may see trimming/AOT warnings on the first build. The JSON example sets `#:property PublishAot=false` because Native AOT turns off reflection-based JSON.
- `07-memory-safety.cs` uses a **preview** feature (`LangVersion=preview`).

## Rebuild the slides

```bash
python run_examples.py         # runs all 18 examples, saves their output to slides/outputs.json
python slides/build_deck.py    # builds slides/dotnet11-whats-new.html and .pdf
```

The deck uses the CodeMitVishal slide template (`slide_kit.py`). Set `SLIDES_TEMPLATE` to its folder if it isn't in the default location. Rendering the PDF uses Microsoft Edge (Windows).

## Sources

- [What's new in .NET 11](https://learn.microsoft.com/dotnet/core/whats-new/dotnet-11/overview) (runtime, libraries, SDK)
- [What's new in C# 15](https://learn.microsoft.com/dotnet/csharp/whats-new/csharp-15)
- [.NET support policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core)
- [.NET 11 guide on dotnetdevs.io](https://www.dotnetdevs.io/guides/dotnet-11/) (ecosystem summary)

Made by [CodeMitVishal](https://www.youtube.com/@CodeMitVishal).
