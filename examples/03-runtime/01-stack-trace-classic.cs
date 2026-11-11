// .NET 11 runtime · Live stack trace WITHOUT Runtime Async (compiler state machines)
// Run: dotnet run 01-stack-trace-classic.cs
#:property UseRuntimeAsync=false
using System.Diagnostics;

await OuterAsync();

static async Task OuterAsync()  { await Task.CompletedTask; await MiddleAsync(); }
static async Task MiddleAsync() { await Task.CompletedTask; await InnerAsync(); }
static async Task InnerAsync()
{
    await Task.CompletedTask;
    Console.WriteLine(new StackTrace());
}
