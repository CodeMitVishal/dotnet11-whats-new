// C# 15 · Extension indexers
// Run: dotnet run 05-extension-indexers.cs

IEnumerable<int> numbers = Enumerable.Range(1, 10);

// Indexing an IEnumerable<int>, thanks to the extension
Console.WriteLine(numbers[2]);

public static class SequenceIndexer
{
    extension(IEnumerable<int> sequence)
    {
        public int this[int index] => sequence.ElementAt(index);
    }
}
