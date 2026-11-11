// C# 15 · Union types for results: success OR error, never both
// Run: dotnet run 02-union-result.cs

Console.WriteLine(Show(Divide(10, 2)));
Console.WriteLine(Show(Divide(10, 0)));

static Result Divide(int a, int b) =>
    b == 0 ? new Error("cannot divide by zero")
           : new Ok(a / b);

static string Show(Result r) => r switch
{
    Ok ok     => $"OK: {ok.Value}",
    Error err => $"Error: {err.Message}",
};

public record Ok(int Value);
public record Error(string Message);
public union Result(Ok, Error);
