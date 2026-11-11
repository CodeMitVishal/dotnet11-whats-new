// .NET 11 libraries · EqualityComparer<T>.Create and generic Random
// Run: dotnet run 03-comparer-and-random.cs

// Compare people by name only: no custom comparer class
var byName = EqualityComparer<Person>.Create(p => p.Name);

var people = new HashSet<Person>(byName)
{
    new("Alice", 30),
    new("Bob", 25),
    new("Alice", 40),   // same name: not added
};
Console.WriteLine($"People: {people.Count}");

// Random numbers of any numeric type
long l = Random.Shared.NextInteger<long>(0, 100);
Half h = Random.Shared.NextBinaryFloat<Half>();
Console.WriteLine($"long={l}, Half={h}");

record Person(string Name, int Age);
