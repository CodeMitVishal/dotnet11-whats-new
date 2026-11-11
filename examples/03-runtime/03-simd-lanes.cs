// .NET 11 runtime · New SIMD lane APIs
// Run: dotnet run 03-simd-lanes.cs
using System.Runtime.Intrinsics;

// Start at 1, multiply by 2 for each lane: 1, 2, 4, 8
var powers = Vector128.CreateGeometricSequence(1, 2);
Console.WriteLine(powers);

// Interleave two vectors, lane by lane
var a = Vector128.Create(1, 2, 3, 4);
var b = Vector128.Create(10, 20, 30, 40);
var (lower, upper) = Vector128.Zip(a, b);
Console.WriteLine($"{lower} {upper}");
