// .NET 11 runtime · Live stack trace WITH Runtime Async (the runtime handles await)
// Run: dotnet run 02-stack-trace-runtime-async.cs
#:property Features=runtime-async=on
using System.Diagnostics;

await OuterAsync();

static async Task OuterAsync()  { await Task.CompletedTask; await MiddleAsync(); }
static async Task MiddleAsync() { await Task.CompletedTask; await InnerAsync(); }
static async Task InnerAsync()
{
    await Task.CompletedTask;
    Console.WriteLine(new StackTrace());
}
