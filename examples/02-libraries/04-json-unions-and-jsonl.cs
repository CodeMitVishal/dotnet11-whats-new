// .NET 11 libraries · System.Text.Json: unions and JSON Lines
// Run: dotnet run 04-json-unions-and-jsonl.cs
// File-based apps use Native AOT, which turns off reflection JSON:
#:property PublishAot=false
using System.IO.Pipelines;
using System.Text.Json;

// 1) A union is written as its active case: no wrapper
Reading reading = "hello";
Console.WriteLine(JsonSerializer.Serialize(reading));
reading = 42;
Console.WriteLine(JsonSerializer.Serialize(reading));

// 2) JSON Lines: one value per line
var pipe = PipeWriter.Create(Console.OpenStandardOutput());
await JsonSerializer.SerializeAsyncEnumerable(
    pipe, AsyncEnumerable.Range(1, 3), topLevelValues: true);
await pipe.CompleteAsync();

public union Reading(int, string);
