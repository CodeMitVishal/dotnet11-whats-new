// .NET 11 libraries · Process: run a command and capture its output in one call
// Run: dotnet run 01-process-run.cs
using System.Diagnostics;

// Before: ProcessStartInfo + RedirectStandardOutput + ReadToEnd + WaitForExit
// Now: one call, no deadlock risk, output and exit code together.
ProcessTextOutput result = await Process.RunAndCaptureTextAsync(
    "dotnet", ["--version"]);

Console.WriteLine($"Output:    {result.StandardOutput.Trim()}");
Console.WriteLine($"Exit code: {result.ExitStatus.ExitCode}");
