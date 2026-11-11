// C# 15 · Collection expression arguments: with(...)
// Run: dotnet run 04-collection-expression-args.cs

string[] values = ["one", "two", "three"];

// with(...) passes a capacity to List<T>'s constructor
List<string> names = [with(capacity: 10), .. values];
Console.WriteLine($"Capacity: {names.Capacity}");

// with(...) passes a comparer to HashSet<T>'s constructor
HashSet<string> set =
    [with(StringComparer.OrdinalIgnoreCase), "Hi", "HI", "hi"];

// All three are equal when case is ignored
Console.WriteLine($"{set.Count} item");
