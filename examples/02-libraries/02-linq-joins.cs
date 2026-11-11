// .NET 11 libraries · LINQ: FullJoin and tuple-returning Join
// Run: dotnet run 02-linq-joins.cs

(int Id, string Name, string? Category)[] products =
    [(1, "Laptop", "Electronics"), (2, "Cable", null)];
(string Name, string Text)[] categories =
    [("Electronics", "Devices"), ("Furniture", "Desks")];

// FullJoin: both sides, paired where they match
var full = products.FullJoin(categories,
    p => p.Category, c => c.Name);
foreach (var (p, c) in full)
    Console.WriteLine($"{p.Name ?? "-"} | {c.Text ?? "-"}");

// Join without a result selector returns tuples
(int ProductId, int Qty)[] orders = [(1, 3), (1, 1)];
var joined = products.Join(orders, p => p.Id, o => o.ProductId);
foreach (var (p, o) in joined)
    Console.WriteLine($"{p.Name}: qty {o.Qty}");
