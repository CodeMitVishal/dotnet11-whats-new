// C# 15 · Closed hierarchies
// Run: dotnet run 03-closed-hierarchies.cs

Console.WriteLine(Describe(new Closed()));
Console.WriteLine(Describe(new Open(40)));

// Every direct child of GateState is handled, so no default arm.
static string Describe(GateState state) => state switch
{
    Closed => "closed",
    Open(var percent) => $"{percent}% open",
};

// "closed": only this assembly may derive from GateState.
public closed record class GateState;
public record class Closed : GateState;
public record class Open(float Percent) : GateState;
