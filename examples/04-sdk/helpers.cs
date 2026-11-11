// Shared helper, pulled into app.cs with #:include
public static class Helpers
{
    public static string Format(string greeting, Customer c) =>
        $"{greeting}, {c.Name} from {c.City}!";
}
