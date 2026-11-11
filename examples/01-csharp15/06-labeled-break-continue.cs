// C# 15 · Labeled break and continue
// Run: dotnet run 06-labeled-break-continue.cs

int[][] grid =
[
    [1, 2, -1, 4],   // -1 = blocked: skip the rest of this row
    [5, 6, 7, 8],
    [9, 99, 10, 11], // 99 = goal: stop everything
];

outer: for (int row = 0; row < grid.Length; row++)
{
    for (int col = 0; col < grid[row].Length; col++)
    {
        int cell = grid[row][col];
        if (cell == -1) continue outer;   // next row
        if (cell == 99) break outer;      // leave both loops
        Console.Write($"{cell} ");
    }
}
Console.WriteLine();
