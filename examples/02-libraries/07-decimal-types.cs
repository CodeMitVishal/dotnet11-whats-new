// .NET 11 libraries · IEEE 754 decimal types
// Run: dotnet run 07-decimal-types.cs
using System.Numerics;

double d = 0.1 + 0.2;
Decimal64 x = Decimal64.Parse("0.1") + Decimal64.Parse("0.2");

Console.WriteLine($"double:    {d:R}");
Console.WriteLine($"Decimal64: {x}");
