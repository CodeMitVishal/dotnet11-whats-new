""".NET 11: What's new. Builds slides/dotnet11-whats-new.pdf from the examples.

Uses the CodeMitVishal slide template (slide_kit.py). Every output box shows the real output of
the example, captured by run_examples.py into slides/outputs.json.

    python run_examples.py          # run all examples with the .NET 11 SDK
    python slides/build_deck.py     # build the HTML + PDF
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

TEMPLATE = Path(os.environ.get("SLIDES_TEMPLATE", r"C:\Users\acer\.claude\slides-template"))
sys.path.insert(0, str(TEMPLATE))
import slide_kit  # noqa: E402
from slide_kit import Deck  # noqa: E402

HERE = Path(__file__).parent
ROOT = HERE.parent
EX = ROOT / "examples"
OUTPUTS = json.loads((HERE / "outputs.json").read_text(encoding="utf-8")) if (HERE / "outputs.json").exists() else {}
REPO = "github.com/CodeMitVishal/dotnet11-whats-new"

# ------------------------------------------------------------------ C# syntax highlighting
CS_KW = ("public|private|protected|internal|static|class|record|struct|interface|union|closed|extension|"
         "var|new|return|if|else|for|foreach|in|while|await|async|using|string|int|long|byte|bool|double|"
         "float|object|void|true|false|null|switch|break|continue|this|override|sealed|abstract|throw|yield|"
         "unsafe|fixed|with|is|not|and|or|out|get|set|const|static|readonly|default|typeof|try|catch|finally")
CS_TOKENS = re.compile(rf"""(?P<s>\$?@?"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)')|(?P<c>//[^\n]*|\#:[^\n]*|<!--.*?-->)|(?P<k>\b(?:{CS_KW})\b)|(?P<o>.|\n)""")


def hl(code: str) -> str:
    """C# highlighter. Code that starts with '#!txt' is shown as plain text (terminal output, XML)."""
    code = code.strip("\n")
    if code.startswith("#!txt"):
        return html.escape(code[5:].lstrip("\n"))
    if code.startswith("#!sh"):                                   # shell: highlight comments only
        lines = code[4:].lstrip("\n").splitlines()
        return "\n".join(f'<span class="c">{html.escape(l)}</span>' if l.lstrip().startswith("#")
                         else f'<span class="g">$</span> {html.escape(l)}' if l.strip() else "" for l in lines)
    out = []
    for m in CS_TOKENS.finditer(code):
        text = html.escape(m.group())
        out.append(text if m.lastgroup == "o" else f'<span class="{m.lastgroup}">{text}</span>')
    return "".join(out)


slide_kit.hl = hl    # the template's layouts call slide_kit.hl

EXTRA_CSS = """
.term { background: #0B0F18; border: 2px solid #2A3550; border-radius: 16px; padding: 18px 28px 20px;
  font-family: 'Roboto Mono', monospace; color: #E6E9F0; white-space: pre; line-height: 1.45; }
.term .cmd { color: #7EE2A8; } .term .lbl { display: block; font-family: 'Space Grotesk', Arial, sans-serif;
  font-size: 18px; letter-spacing: 3px; color: #8A93A6; margin-bottom: 6px; font-weight: 700; }
.ba-h { font-size: 24px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 6px 16px;
  border-radius: 999px; align-self: flex-start; }
.ba-old { background: #E8E3D6; color: #6B7385; } .ba-new { background: #121826; color: #7EE2A8; }
.agenda { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
.agenda .card { min-height: 250px; }
.agenda .n { font-size: 64px; font-weight: 700; color: #F2C14E; line-height: 1; }
.agenda .card { background: #121826; border: none; } .agenda h3 { color: #fff; font-size: 34px; }
.agenda p { color: #C9D2E3; }
.kpi { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.kpi div { background: #FFFDF8; border: 1px solid #E3DFD3; border-radius: 18px; padding: 24px 26px; }
.kpi b { display: block; font-size: 52px; color: #2F5E9E; line-height: 1.1; }
.kpi > div > span { font-size: 24px; line-height: 1.35; display: block; margin-top: 8px; }
td.ok { color: #1F7A4A; font-weight: 700; } td.old { color: #B4462F; font-weight: 700; }
"""


class TalkDeck(Deck):
    def save(self, out_html):
        out = super().save(out_html)
        page = out.read_text(encoding="utf-8").replace("</style>", EXTRA_CSS + "</style>", 1)
        out.write_text(page, encoding="utf-8")
        return out

    # -------------------------------------------------------------- extra layouts
    def part(self, num: str, name: str, tagline: str, toc: list[tuple[str, str]]):
        rows = "".join(f"<div><span>{a}</span><span>{b}</span></div>" for a, b in toc)
        return self.raw(f"""<section class="dark" style="flex-direction:row;align-items:center;gap:100px">
  <div style="width:640px;display:flex;flex-direction:column;gap:20px">
    <p class="num">PART</p><p class="big">{num}</p>
    <h1 style="font-size:80px">{name}</h1>
    <p style="font-size:30px;line-height:1.4">{tagline}</p></div>
  <div style="flex:1" class="toc"><p class="num" style="font-size:22px;margin-bottom:10px">IN THIS PART</p>{rows}</div>
  {self._foot(f"{self.title} · Part {num}")}
</section>""")

    def feature(self, label: str, eyebrow: str, h2: str, file: str, notes=(), tip: str | None = None,
                run: str | None = None, width: int = 1000, size: int = 25, strip_header: bool = True):
        """Code from an example file on the left, its real output below it, notes on the right."""
        src = (EX / file).read_text(encoding="utf-8")
        if strip_header:   # drop the shebang, the "// title" line and the "// Run:" lines; the slide says it
            lines = src.splitlines()
            if lines and lines[0].startswith("#!"):
                lines.pop(0)
            if lines and lines[0].startswith("//"):
                lines.pop(0)
            while lines and (lines[0].startswith(("// Run:", "//      dotnet")) or not lines[0].strip()):
                lines.pop(0)
            src = "\n".join(lines)
        key = run or file
        output = OUTPUTS.get(key, {}).get("output", "(run: python run_examples.py)")
        cmd = "dotnet run " + (" ".join(key.split(" ")[1:]) + " " if " " in key else "") + Path(file).name
        n_lines = len(src.strip("\n").splitlines())
        size = min(size, int(640 / (n_lines * 1.5)))   # fit the height too (about 640px for the code box)
        side_w = 1664 - 48 - width          # the right column: notes, then the real output
        out_size = max(17, min(24, int((side_w - 60) / (max(len(l) for l in (output + "\n$ " + cmd).splitlines()) * 0.61))))
        notes_html = "".join(f'<p class="note">{n}</p>' for n in notes) + (f'<p class="tip">{tip}</p>' if tip else "")
        term = (f'<div class="term" style="font-size:{out_size}px"><span class="lbl">OUTPUT</span>'
                f'<span class="cmd">$ {html.escape(cmd)}</span>\n{html.escape(output)}</div>')
        return self.raw(f"""<section style="gap:34px">
  <div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>
  <div class="row"><div class="code" style="width:{width}px;font-size:{slide_kit.fit(src, width, size)}px;padding:24px 32px">{hl(src)}</div>
  <div class="col" style="width:{side_w}px;gap:20px">{notes_html}{term}</div></div>
  {self._foot(label)}
</section>""")

    def before_after(self, label: str, eyebrow: str, h2: str, before: str, after: str,
                     before_title: str = "Before", after_title: str = ".NET 11",
                     notes=(), size: int = 24, height: int | None = None):
        def box(src):
            return (f'<div class="code" style="font-size:{slide_kit.fit(src, 790, size)}px;padding:24px 30px;'
                    f'{"min-height:" + str(height) + "px" if height else ""}">{hl(src)}</div>')
        side = "".join(f'<p class="note">{n}</p>' for n in notes)
        return self.raw(f"""<section style="gap:30px">
  <div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>
  <div class="row" style="gap:36px">
    <div class="col" style="width:790px;gap:14px"><span class="ba-h ba-old">{before_title}</span>{box(before)}</div>
    <div class="col" style="width:790px;gap:14px"><span class="ba-h ba-new">{after_title}</span>{box(after)}</div>
  </div>
  {f'<div class="row" style="gap:36px">{side}</div>' if side else ''}
  {self._foot(label)}
</section>""")


def out(key: str) -> str:
    return OUTPUTS.get(key, {}).get("output", "(run: python run_examples.py)")


# ======================================================================= the deck
d = TalkDeck(".NET 11: What's new", repo=REPO)
L1, L2, L3, L4, L5 = (".NET 11 · The release", ".NET 11 · C# 15", ".NET 11 · Libraries",
                      ".NET 11 · Runtime", ".NET 11 · SDK & tooling")

d.cover(".NET 11: What's new",
        'C# 15, a faster runtime, handier libraries and a quicker SDK, '
        'explained with <b style="color:#7EE2A8">code you can run</b>.',
        kicker=".NET 11 · RELEASED 10 NOVEMBER 2026",
        stats=[("C# 15", "new language version"), ("2 years", "of support (STS)"), ("18", "runnable examples")])

d.raw(f"""<section>
  <div><p class="eyebrow">Agenda</p><h2>What we'll cover</h2></div>
  <div class="agenda">
    <div class="card"><span class="n">1</span><h3>The release</h3><p>Support dates, and who should upgrade.</p></div>
    <div class="card"><span class="n">2</span><h3>C# 15</h3><p>Unions, closed hierarchies, <span style="font-family:'Roboto Mono'">with(...)</span>, extension indexers, labeled loops.</p></div>
    <div class="card"><span class="n">3</span><h3>Libraries</h3><p>Process, LINQ joins, JSON unions, Zstandard, async validation, decimals.</p></div>
    <div class="card"><span class="n">4</span><h3>Runtime</h3><p>Runtime Async, JIT wins you get for free, new CPU baseline.</p></div>
    <div class="card"><span class="n">5</span><h3>SDK &amp; tooling</h3><p>File-based apps, a faster CLI, better <span style="font-family:'Roboto Mono'">dotnet test</span>.</p></div>
    <div class="card"><span class="n">6</span><h3>Upgrade</h3><p>Ecosystem changes and a 4-step upgrade checklist.</p></div>
  </div>
  {d._foot(".NET 11 · Agenda")}
</section>""")

# ----------------------------------------------------------------------- 1. release
d.table(L1, "The release", "Supported versions after 10 November 2026",
        ["Version", "Type", "Released", "Support ends"],
        [["<b>.NET 11</b>", "STS", "10 Nov 2026", '<span style="color:#1F7A4A;font-weight:700">14 Nov 2028</span>'],
         ["<b>.NET 10</b>", "LTS", "11 Nov 2025", '<span style="color:#1F7A4A;font-weight:700">14 Nov 2028</span>'],
         ["<b>.NET 9</b>", "STS", "12 Nov 2024", '<span style="color:#B4462F;font-weight:700">ended 10 Nov 2026</span>'],
         ["<b>.NET 8</b>", "LTS", "14 Nov 2023", '<span style="color:#B4462F;font-weight:700">ended 10 Nov 2026</span>']],
        notes=["<b>LTS</b> = Long-Term Support: 3 years.",
               "<b>STS</b> = Standard-Term Support: 2 years.",
               "So .NET 10 and .NET 11 are both supported until <b>November 2028</b>."],
        tip="Still on .NET 8 or 9? You no longer get security fixes. Move to 10 (LTS) or 11 (STS).")

# ----------------------------------------------------------------------- 2. C# 15
d.part("1", "C# 15", "The default language version for net11.0. No preview flag needed (except memory safety).",
       [("Union types", "01, 02"), ("Closed hierarchies", "03"), ("Collection expression arguments", "04"),
        ("Extension indexers", "05"), ("Labeled break and continue", "06"), ("Memory safety (preview)", "07")])

d.feature(L2, "C# 15 · Union types", "One value, one of a fixed set of types", "01-csharp15/01-union-types.cs",
          notes=["<span class=\"m\">union Pet(Cat, Dog, Bird)</span>: a Pet is <b>exactly one</b> of these three.",
                 "Each case converts automatically: <span class=\"m\">Pet pet = new Dog(\"Rex\")</span>.",
                 "The compiler checks that your <span class=\"m\">switch</span> handles <b>every</b> case: no <span class=\"m\">default</span> arm needed."],
          tip="Add a fourth case later? Every switch that misses it gets a compiler warning.")

d.before_after(L2, "C# 15 · Union types", "Why it matters: success OR error, checked by the compiler", '''
abstract record Result;
record Ok(int Value) : Result;
record Error(string Message) : Result;

string Show(Result r) => r switch
{
    Ok ok     => $"OK: {ok.Value}",
    Error err => $"Error: {err.Message}",
    _ => throw new UnreachableException(),
};''', '''
record Ok(int Value);
record Error(string Message);
union Result(Ok, Error);

string Show(Result r) => r switch
{
    Ok ok     => $"OK: {ok.Value}",
    Error err => $"Error: {err.Message}",
};''', before_title="Before: base class", after_title="C# 15: union",
               notes=["<b>Before:</b> anyone can add another subclass, so the compiler insists on a <span class=\"m\">_ =&gt;</span> fallback.",
                      "<b>Now:</b> the set of cases is fixed. Ok and Error don't even need a common base class."])

d.feature(L2, "C# 15 · Closed hierarchies", "A class family nobody else can extend", "01-csharp15/03-closed-hierarchies.cs",
          notes=["<span class=\"m\">closed</span>: only <b>this assembly</b> can derive from GateState.",
                 "So the compiler knows <b>all</b> children and the switch needs no <span class=\"m\">default</span>.",
                 "A closed class is automatically <span class=\"m\">abstract</span>."],
          tip="Unions combine types that already exist. Closed hierarchies are a family you design with a shared base.")

d.table(L2, "C# 15 · Union or closed?", "Which one should I use?",
        ["Situation", "Use"],
        [["The cases already exist and are unrelated (<span class=\"m\">int</span>, <span class=\"m\">string</span>, a library type)", "<b>union</b>"],
         ["You design the types and they share a base (properties, methods)", "<b>closed</b> hierarchy"],
         ["A function returns success <i>or</i> an error", "<b>union</b>"],
         ["A public JSON API contract", "<b>closed</b> + a type discriminator"],
         ["You need exhaustive <span class=\"m\">switch</span> checks", "both ✔"]],
        notes=["System.Text.Json writes a union as its <b>active case only</b>: <span class=\"m\">\"hello\"</span>, no <span class=\"m\">$type</span>.",
               "That's why Microsoft suggests a closed hierarchy with a discriminator for new API contracts."],
        width=560)

d.feature(L2, "C# 15 · Collection expression arguments", "Pass constructor arguments inside [ ]",
          "01-csharp15/04-collection-expression-args.cs",
          notes=["<span class=\"m\">with(...)</span> must be the <b>first</b> element.",
                 "Its arguments go to the collection's constructor: capacity, comparer, …",
                 "Before, you had to drop the <span class=\"m\">[ ]</span> syntax and write <span class=\"m\">new HashSet&lt;string&gt;(comparer) { … }</span>."])

d.feature(L2, "C# 15 · Extension indexers", "Add an indexer to a type you don't own", "01-csharp15/05-extension-indexers.cs",
          notes=["C# 14 introduced <span class=\"m\">extension</span> blocks (extension properties).",
                 "C# 15 lets them declare <b>indexers</b>: <span class=\"m\">this[int index]</span>.",
                 "The receiver needs a name (here <span class=\"m\">sequence</span>), because indexers are instance members."],
          tip="ElementAt walks the sequence: fine for demos, slow for big lists.")

d.before_after(L2, "C# 15 · Labeled break and continue", "Leave nested loops without flags or goto", '''
bool found = false;
for (int row = 0; row < grid.Length; row++)
{
    for (int col = 0; col < grid[row].Length; col++)
    {
        if (grid[row][col] == 99)
        {
            found = true;
            break;          // only the inner loop
        }
    }
    if (found) break;       // and again here
}''', '''
outer: for (int row = 0; row < grid.Length; row++)
{
    for (int col = 0; col < grid[row].Length; col++)
    {
        if (grid[row][col] == -1)
            continue outer; // next row

        if (grid[row][col] == 99)
            break outer;    // leave both loops
    }
}''', before_title="Before: a flag", after_title="C# 15: labels",
               notes=["Put a label on the loop, then <span class=\"m\">break outer</span> or <span class=\"m\">continue outer</span>.",
                      f"Example 06 output: <span class=\"m\">{html.escape(out('01-csharp15/06-labeled-break-continue.cs'))}</span>"])

d.feature(L2, "C# 15 · Memory safety (preview)", "unsafe marks where memory is actually read",
          "01-csharp15/07-memory-safety.cs",
          notes=["<b>Preview:</b> needs <span class=\"m\">LangVersion=preview</span>.",
                 "Taking an address (<span class=\"m\">&amp;number</span>) is safe now: nothing is read yet.",
                 "Reading through the pointer is still <span class=\"m\">unsafe</span>. New: <span class=\"m\">unsafe(expr)</span> for one expression."],
          tip="Goal: reviewers find every risky memory access by searching for <b>unsafe</b>.")

# ----------------------------------------------------------------------- 3. libraries
d.part("2", "Libraries", "New APIs that remove boilerplate you write every week.",
       [("Process: run and capture", "01"), ("LINQ FullJoin and tuple Join", "02"),
        ("EqualityComparer.Create, generic Random", "03"), ("JSON unions and JSON Lines", "04"),
        ("StringStream and Zstandard", "05"), ("Async validation", "06"), ("Decimal32 / 64 / 128", "07")])

d.before_after(L3, "Libraries · Process", "Run a command and read its output", '''
var psi = new ProcessStartInfo("dotnet", "--version")
{
    RedirectStandardOutput = true,
    RedirectStandardError  = true,
};
using var p = Process.Start(psi)!;
string output = await p.StandardOutput.ReadToEndAsync();
await p.WaitForExitAsync();   // forget this: wrong code
Console.WriteLine(output);
Console.WriteLine(p.ExitCode);''', '''
ProcessTextOutput result =
    await Process.RunAndCaptureTextAsync(
        "dotnet", ["--version"]);

Console.WriteLine(result.StandardOutput);
Console.WriteLine(result.ExitStatus.ExitCode);''', before_title="Before: 10 lines", after_title=".NET 11: 1 call",
               notes=[f"Output of example 01: <span class=\"m\">{html.escape(out('02-libraries/01-process-run.cs')).replace(chr(10), ' · ')}</span>",
                      "Also new: <span class=\"m\">Process.Run</span>, <span class=\"m\">StartAndForget</span>, <span class=\"m\">KillOnParentExit</span> (Windows), <span class=\"m\">Signal(PosixSignal)</span>."])

d.feature(L3, "Libraries · LINQ", "FullJoin, and Join that returns tuples", "02-libraries/02-linq-joins.cs", size=22,
          notes=["<b>FullJoin</b>: every item from <b>both</b> sides, <span class=\"m\">null</span> where there's no match.",
                 "<b>Join</b> without a result selector gives you <span class=\"m\">(outer, inner)</span> tuples to deconstruct.",
                 "LeftJoin/RightJoin came in .NET 10. EF Core 11 turns FullJoin into SQL <b>FULL OUTER JOIN</b>."])

d.feature(L3, "Libraries · Small helpers", "Comparers from a lambda, random numbers of any type",
          "02-libraries/03-comparer-and-random.cs", size=23,
          notes=["<span class=\"m\">EqualityComparer&lt;T&gt;.Create(p =&gt; p.Name)</span>: compare by a key, no custom class.",
                 "<span class=\"m\">NextInteger&lt;T&gt;</span>: any integer type. <span class=\"m\">NextBinaryFloat&lt;T&gt;</span>: float, double, Half.",
                 "The random numbers differ on every run."])

d.feature(L3, "Libraries · System.Text.Json", "Unions and JSON Lines", "02-libraries/04-json-unions-and-jsonl.cs", size=22,
          notes=["A union is serialized as its <b>active case</b>: no wrapper object, no <span class=\"m\">$type</span>.",
                 "<span class=\"m\">topLevelValues: true</span> writes <b>JSON Lines</b>: one value per line.",
                 "JSON Lines suits logs and streams: read and write one line at a time."])

d.feature(L3, "Libraries · Streams & compression", "No-copy streams and built-in Zstandard",
          "02-libraries/05-streams-and-zstandard.cs", size=23,
          notes=["<b>StringStream</b>, <b>ReadOnlyMemoryStream</b>, <b>WritableMemoryStream</b>, <b>ReadOnlySequenceStream</b>: wrap data without copying it into a MemoryStream.",
                 "<b>ZstandardStream</b> is now in System.IO.Compression, next to GZip and Brotli.",
                 "Zstandard: fast, with good compression; widely used for logs and backups."])

d.feature(L3, "Libraries · Async validation", "Validation that can await a database or API",
          "02-libraries/06-async-validation.cs", width=1000,
          notes=["Before: <span class=\"m\">IsValid</span> was synchronous, so a database check blocked with <span class=\"m\">.Result</span>.",
                 "Now: derive from <b>AsyncValidationAttribute</b> and put the work in <b>IsValidAsync</b>.",
                 "Run it with <span class=\"m\">Validator.TryValidateObjectAsync</span>. ASP.NET Core 11 uses it too.",
                 "The sync <span class=\"m\">IsValid</span> must still be overridden, but it's never called."])

d.feature(L3, "Libraries · Numerics", "Exact decimal math: Decimal32, Decimal64, Decimal128",
          "02-libraries/07-decimal-types.cs",
          notes=["<span class=\"m\">double</span> is binary: 0.1 + 0.2 is <b>not</b> exactly 0.3.",
                 "The new types follow the <b>IEEE 754 decimal</b> standard, so 0.1 + 0.2 = 0.3.",
                 "Use them to exchange data with other IEEE systems; <span class=\"m\">decimal</span> is still fine for money."])

d.table(L3, "Libraries · Also new", "More additions worth knowing",
        ["Area", "What's new"],
        [["Compression", "ZIP entries are <b>CRC32-checked</b>: corrupt files now throw <span class=\"m\">InvalidDataException</span>"],
         ["Base64", "<span class=\"m\">EncodeToString</span>, <span class=\"m\">DecodeFromChars</span>, UTF-8 and span versions"],
         ["Security", "<span class=\"m\">X25519DiffieHellman</span> key exchange, AES Key Wrap, experimental ML-KEM / HPKE"],
         ["Networking", "Typed DNS lookups (<span class=\"m\">DnsResolver</span>: SRV, MX, TXT), HTTP request compression"],
         ["Observability", "Built-in OpenTelemetry metrics for <span class=\"m\">MemoryCache</span>"],
         ["Console", "<span class=\"m\">FORCE_COLOR=1</span> keeps colours when output is redirected"]])

# ----------------------------------------------------------------------- 4. runtime
d.part("3", "Runtime", "Most of this you get for free: just retarget to net11.0.",
       [("Runtime Async", "01, 02"), ("JIT: faster with no code changes", "-"), ("SIMD lane APIs", "03"),
        ("New minimum CPU requirements", "-")])

def short_frames(trace: str) -> str:
    """Make the real stack traces readable on a slide: same frames, shorter names."""
    trace = trace.replace("System.Runtime.CompilerServices.AsyncMethodBuilderCore.Start[TStateMachine]"
                          "(TStateMachine& stateMachine)", "AsyncMethodBuilderCore.Start(...)")
    trace = re.sub(r"Program\.<<Main>\$>g__(\w+)\|\d+_\d+\(\)", r"\1()", trace)
    trace = trace.replace("Program.<Main>$(String[] args)", "<Main>$(args)")
    return trace.replace("Program.<Main>(String[] args)", "Main(args)")


classic = short_frames(out("03-runtime/01-stack-trace-classic.cs"))
native = short_frames(out("03-runtime/02-stack-trace-runtime-async.cs"))
d.before_after(L4, "Runtime · Runtime Async", "The runtime runs async methods itself",
               "#!txt\n" + classic, "#!txt\n" + native,
               before_title=f"Compiler state machines: {len(classic.splitlines())} frames",
               after_title=f"Runtime Async: {len(native.splitlines())} frames", size=22, height=520,
               notes=["Same program (examples 01 and 02): Outer → Middle → Inner, then print <span class=\"m\">new StackTrace()</span>.",
                      "Turn it on: <span class=\"m\">&lt;Features&gt;runtime-async=on&lt;/Features&gt;</span>. Fewer frames: clearer debugging and profiling, less overhead."])

d.table(L4, "Runtime · JIT", "Faster code, no changes needed",
        ["Improvement", "Code that gets faster"],
        [["Fewer bounds checks", "<span class=\"m\">values[^1]</span>, <span class=\"m\">if (!span.IsEmpty &amp;&amp; span[0] == x)</span>"],
         ["Constant folding", "<span class=\"m\">role == \"Admin\"</span> with a known role becomes true/false"],
         ["Devirtualization", "generic virtual methods, default interface methods"],
         ["Cheaper async", "no ExecutionContext copy when you don't use AsyncLocal"],
         ["Faster math", "<span class=\"m\">Math.BigMul</span> on x64 is one MUL instruction"],
         ["ReadyToRun", "default comparers precompiled: up to <b>20×</b> faster collection ops"],
         ["Linux", "<span class=\"m\">Guid.NewGuid()</span> about <b>12%</b> faster"]],
        tip="Measure your own app: run your benchmarks on .NET 10 and .NET 11.")

d.feature(L4, "Runtime · SIMD", "Build and shuffle vector lanes", "03-runtime/03-simd-lanes.cs", size=24,
          notes=["<span class=\"m\">CreateGeometricSequence(1, 2)</span>: 1, 2, 4, 8.",
                 "<span class=\"m\">Zip</span> interleaves two vectors lane by lane; <span class=\"m\">Unzip</span> splits them again.",
                 "Works on <span class=\"m\">Vector64/128/256/512</span> and <span class=\"m\">Vector&lt;T&gt;</span>. Also: hardware FP16 for <span class=\"m\">Half</span>."])

d.table(L4, "Runtime · Hardware", "New minimum CPU requirements",
        ["CPU", ".NET 10", ".NET 11"],
        [["x64 (Windows, Linux, macOS)", "x86-64-v1", "<b>x86-64-v2</b> (adds SSE4.2, POPCNT)"],
         ["Arm64 on Windows", "armv8.0-a", "<b>armv8.0-a + LSE</b>"],
         ["Arm64 on Linux / Apple", "unchanged", "unchanged (Raspberry Pi still works)"]],
        notes=["Every Intel and AMD CPU still supported by its vendor qualifies (older ones went out of support around 2013).",
               "Windows 11 already requires this level."],
        tip='On an older CPU, .NET 11 stops with: "The current CPU is missing one or more of the baseline instruction sets."',
        width=600)

# ----------------------------------------------------------------------- 5. SDK
d.part("4", "SDK & tooling", "A faster CLI, scripts that grow up, and better tests.",
       [("File-based apps: #:include", "app.cs"), ("dotnet run -e", "app.cs"), ("A faster dotnet CLI", "-"),
        ("dotnet test and other commands", "-")])

d.feature(L5, "SDK · File-based apps", "One-file apps can now span several files", "04-sdk/app.cs",
          run="04-sdk/app.cs -e GREETING=Hallo", size=24,
          notes=["<span class=\"m\">dotnet run app.cs</span>: no .csproj needed (since .NET 10).",
                 "New: <span class=\"m\">#:include helpers.cs</span> pulls in other files, even a <span class=\"m\">.dll</span>.",
                 "New: <span class=\"m\">dotnet run -e KEY=VALUE</span> passes environment variables.",
                 f"Without <span class=\"m\">-e</span>: <span class=\"m\">{html.escape(out('04-sdk/app.cs'))}</span>"])

d.raw(f"""<section>
  <div><p class="eyebrow">SDK · Speed</p><h2>A faster dotnet CLI, out of the box</h2></div>
  <div class="kpi">
    <div><b>Native AOT</b><span>The <span class="m">dotnet</span> CLI starts natively. Tools like <span class="m">dotnet ef</span> skip 600–700 ms of startup.</span></div>
    <div><b>On</b><span>The MSBuild server is on by default: a warm worker between builds.</span></div>
    <div><b>−18%</b><span>Linux SDK tarball: 230 → 189 MB (deb/rpm: −26%).</span></div>
    <div><b>10–13%</b><span>Faster project evaluation with many files (new wildcard matching).</span></div>
  </div>
  <div class="row"><p class="note" style="flex:1">Nothing to configure: install the SDK and you get all four.</p>
  <p class="tip" style="flex:1">Opt out if needed: <b>DOTNET_CLI_ENABLEAOT=false</b>, <b>DOTNET_CLI_USE_MSBUILD_SERVER=false</b>.</p></div>
  {d._foot(L5)}
</section>""")

d.code(L5, "SDK · Commands", "New options worth trying", '''#!sh
# Tests: stop after 90 s, or after 5 failures
dotnet test --timeout 90s
dotnet test --maximum-failed-tests 5

# Solution filters from the CLI
dotnet new slnf --parent-solution App.slnx --name Tests
dotnet sln Tests.slnf add tests/Tests/Tests.csproj

# xUnit v3 template on Microsoft.Testing.Platform
dotnet new xunit --xunit-version v3

# Only use NuGet packages published 24+ hours ago
dotnet nuget update source nuget.org --min-publish-age-hours 24''',
       notes=["<span class=\"m\">dotnet test</span> also shows tests that are <b>running right now</b>, and supports Android and iOS devices.",
              "<b>Solution filters</b> (.slnf): load only part of a big solution.",
              "<b>Minimum publish age</b> protects you from a freshly published malicious package."],
       width=1020, size=23)

# ----------------------------------------------------------------------- 6. ecosystem + upgrade
d.table(".NET 11 · Ecosystem", "Beyond the core", "What changes in the frameworks",
        ["Framework", "Highlights"],
        [["<b>ASP.NET Core 11</b>", "OpenAPI 3.2, async validation, unions in Minimal APIs, MVC, SignalR, Blazor"],
         ["<b>EF Core 11</b>", "Translates FullJoin, MaxBy, MinBy; fewer joins in includes. <b>Breaking:</b> SQL Server compatibility level 160 by default"],
         ["<b>.NET MAUI</b>", "CoreCLR replaces Mono on Android, iOS and Mac Catalyst (opt back: <span class=\"m\">UseMonoRuntime</span>)"],
         ["<b>AI</b>", "MCP C# SDK 2.0, <span class=\"m\">dotnet new mcpserver</span>, Blazor AI components (experimental)"]],
        notes=["EF Core 11 requires .NET 11.",
               "On SQL Server older than 2022, set <span class=\"m\">UseCompatibilityLevel</span> explicitly."],
        width=520)

d.code(".NET 11 · Upgrade", "Upgrade", "Four steps to .NET 11", '''
// 1. Install the SDK (11.0.100) and pin it in global.json
{ "sdk": { "version": "11.0.100" } }

// 2. Retarget every project (.csproj)
<TargetFramework>net11.0</TargetFramework>

// 3. Update packages: Microsoft.* and EF Core to 11.x
dotnet package update

// 4. Build, run the tests, read the warnings
dotnet build
dotnet test''',
       notes=["<b>Check the breaking changes</b> before step 4:",
              "• CPU baseline x86-64-v2 (old servers / VMs)",
              "• ZIP files now CRC32-checked",
              "• EF Core: SQL Server compatibility 160",
              "• MAUI: CoreCLR instead of Mono"],
       tip="C# 15 comes automatically with net11.0. No LangVersion change needed.", width=960, size=25)

d.code(".NET 11 · Try it", "Try it yourself", "Every example in this talk runs with one command", '''#!sh
git clone https://github.com/CodeMitVishal/dotnet11-whats-new
cd dotnet11-whats-new/examples/01-csharp15
dotnet run 01-union-types.cs

# Run every example and refresh the slide outputs
python run_examples.py''',
       notes=["Needs the <b>.NET 11 SDK</b> (11.0.100 or later).",
              "18 small apps: C# 15, libraries, runtime and SDK.",
              "No project files: each <span class=\"m\">.cs</span> file is a complete app."],
       width=1000)

d.closing("Thanks for watching!", "Questions? Open an issue in the repo or ask in the comments.",
          ["youtube.com/@CodeMitVishal", REPO, "learn.microsoft.com/dotnet/core/whats-new/dotnet-11/overview"])

if __name__ == "__main__":
    html_path = d.save(HERE / "dotnet11-whats-new.html")
    print(f"{len(d.slides)} slides -> {html_path}")
    if "--no-pdf" not in sys.argv:
        print("PDF:", d.render(HERE / "dotnet11-whats-new.pdf", html_path))
