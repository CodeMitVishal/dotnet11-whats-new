# Speaker notes: .NET 11, What's new

A short script for each slide: what to say, and the one thing the audience should remember.
Slide numbers match `slides/dotnet11-whats-new.pdf`.

---

### 1 · Cover
".NET 11 shipped on 10 November 2026. In this talk I'll show what's new with small examples. Every output you'll see is real: I ran each example with the .NET 11 SDK, and the code is in the repo."

### 2 · Agenda
Six parts: the release, C# 15, libraries, runtime, SDK, then the ecosystem and how to upgrade.

### 3 · Supported versions
- **LTS** (even numbers) = 3 years of support; **STS** (odd numbers) = 2 years.
- .NET 10 (LTS) and .NET 11 (STS) are **both supported until November 2028**.
- .NET 8 and 9 stopped getting security fixes on 10 November 2026: move now.
- *Remember:* choose 10 if you upgrade rarely; 11 if you want the newest features.

---

### 4 · Part 1: C# 15
C# 15 is the default for `net11.0`: no `LangVersion` change. Only memory safety needs preview.

### 5 · Union types
- `union Pet(Cat, Dog, Bird)` means a Pet is **exactly one** of those three types.
- You assign a Dog directly: the conversion is implicit.
- The `switch` has no `default` arm, and the compiler knows it's complete. Add a fourth case later and every switch that misses it warns you.

### 6 · Why unions matter (before/after)
- Before: a base class. Anyone could add a subclass, so the compiler forced a `_ =>` fallback.
- Now: the set is fixed, and `Ok` and `Error` don't even need a common base.
- Typical use: a method returns a **result OR an error**. See `02-union-result.cs`.

### 7 · Closed hierarchies
- `closed` on a base class: only **this assembly** can derive from it.
- So the compiler knows all children and the switch is complete. A closed class is automatically abstract.

### 8 · Union or closed?
- Union: combine types that already exist (even `int` and `string`).
- Closed: a family you design, with a shared base.
- For public JSON APIs prefer closed + a discriminator, because a union is serialized as just its value.

### 9 · Collection expression arguments
`with(...)` as the first element passes arguments to the constructor: capacity for `List`, comparer for `HashSet`. Output: capacity 10, and the set has 1 item because "Hi", "HI", "hi" are equal when case is ignored.

### 10 · Extension indexers
C# 14 brought `extension` blocks. C# 15 adds indexers, so `numbers[2]` works on an `IEnumerable<int>`. The receiver needs a name (`sequence`). Note: `ElementAt` walks the sequence, so it's slow on big data.

### 11 · Labeled break and continue
Before: a `found` flag checked in every loop. Now: name the loop (`outer:`), then `break outer` or `continue outer`. Output `1 2 5 6 7 8 9`: row 1 stops at -1 and goes to the next row; row 3 stops everything at 99.

### 12 · Memory safety (preview)
Taking an address with `&` is no longer `unsafe`, because nothing is read yet. Reading through the pointer still is. The goal: `unsafe` marks exactly the risky lines, so reviewers find them. Preview only.

---

### 13 · Part 2: Libraries
New APIs that remove boilerplate.

### 14 · Process
Before: 10 lines, and if you forgot `WaitForExitAsync` (or redirected both streams and read one), it could deadlock. Now: `RunAndCaptureTextAsync` returns the output and the exit code in one call. Also new: `Process.Run`, `StartAndForget`, `KillOnParentExit`, `Signal`.

### 15 · LINQ joins
`FullJoin` returns everything from both sides, with null where there's no match: see "Cable | -" and "- | Desks". `Join` without a result selector gives tuples you can deconstruct. EF Core 11 translates FullJoin to SQL.

### 16 · Small helpers
`EqualityComparer<T>.Create(p => p.Name)`: a comparer from a lambda, so the second Alice isn't added (count 2). `NextInteger<T>` / `NextBinaryFloat<T>` give random numbers of any numeric type (different every run).

### 17 · JSON
A union is written as its active value: `"hello"`, then `42`, with no wrapper. `topLevelValues: true` writes JSON Lines, one value per line. Mention the `PublishAot=false` line: file-based apps default to Native AOT, which disables reflection-based JSON.

### 18 · Streams and Zstandard
`StringStream` turns a string into a Stream without copying. `ZstandardStream` is built in now. 7,000 bytes of repeated text become 24 bytes (repetitive text compresses extremely well; real data compresses less).

### 19 · Async validation
Validation rules can now `await`: derive from `AsyncValidationAttribute`, implement `IsValidAsync`, call `Validator.TryValidateObjectAsync`. The sync `IsValid` must still exist but is never called. Output: "VAT number not registered."

### 20 · Decimal types
`double` gives 0.30000000000000004 for 0.1 + 0.2; `Decimal64` gives 0.3. They implement the IEEE 754 decimal standard: useful to exchange data with other systems. Keep `decimal` for money in normal .NET code.

### 21 · Also new
Read the table quickly. Highlight ZIP CRC32: corrupt ZIP files now **throw**, which can surface as a "new" error after upgrading.

---

### 22 · Part 3: Runtime
Most of this is free: retarget and get faster.

### 23 · Runtime Async
The same program, printing a live stack trace three calls deep. Compiler state machines: 13 frames full of `AsyncMethodBuilderCore.Start`. Runtime Async: 5 frames, the real call chain. Better for debugging and profilers, and less overhead. Turn it on with `<Features>runtime-async=on</Features>`; the .NET libraries are already compiled this way.

### 24 · JIT
Fewer bounds checks, constant folding, devirtualization, cheaper `await`, faster `Math.BigMul`, up to 20× faster default comparers in ReadyToRun. No code change. Always measure your own app.

### 25 · SIMD
`CreateGeometricSequence(1, 2)` gives 1, 2, 4, 8. `Zip` interleaves two vectors: `<1,10,2,20>` and `<3,30,4,40>`. Building blocks for image/audio processing.

### 26 · Minimum CPU
x64 now needs x86-64-v2 (SSE4.2, POPCNT): any CPU still supported by Intel/AMD. Windows on Arm64 needs LSE. Very old servers or VMs with a limited CPU model will refuse to start .NET 11.

---

### 27 · Part 4: SDK & tooling

### 28 · File-based apps
`dotnet run app.cs` runs a single file (since .NET 10). New: `#:include` pulls in other files or a DLL; `dotnet run -e GREETING=Hallo` passes environment variables. Output "Hallo, Vishal from Augsburg!".

### 29 · Faster CLI
The `dotnet` CLI starts as Native AOT; tools like `dotnet ef` skip 600–700 ms. MSBuild server on by default. The Linux SDK is 18–26% smaller. Project evaluation is 10–13% faster.

### 30 · Commands
`dotnet test --timeout` and `--maximum-failed-tests` stop runaway CI runs. Solution filters from the CLI. xUnit v3 template. `--min-publish-age-hours` avoids freshly published (possibly malicious) packages: a supply-chain safety net.

---

### 31 · Ecosystem
ASP.NET Core 11: OpenAPI 3.2, async validation, unions in APIs. EF Core 11 requires .NET 11; watch the SQL Server compatibility level 160 change. MAUI moves from Mono to CoreCLR. AI: MCP C# SDK 2.0 and `dotnet new mcpserver`.

### 32 · Upgrade in four steps
Install SDK 11.0.100 and pin it in `global.json` → `net11.0` → update packages → build and test. Check the four breaking changes on the right first.

### 33 · Try it yourself
Clone, `cd` into a folder, `dotnet run` a file. `python run_examples.py` re-runs everything.

### 34 · Thanks
Point to the repo and the Microsoft Learn page for the full list.
