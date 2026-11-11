// C# 15 · Memory safety (PREVIEW)
// Run: dotnet run 07-memory-safety.cs
#:property LangVersion=preview
#:property AllowUnsafeBlocks=true

int number = 42;

// Taking an address: no "unsafe" needed any more
int* pointer = &number;

// Reading the memory: still needs "unsafe"
int value = unsafe(*pointer);
Console.WriteLine(value);
