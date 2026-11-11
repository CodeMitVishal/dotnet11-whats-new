#!/usr/bin/env dotnet
// .NET 11 SDK · A file-based app split across files with #:include
// Run: dotnet run app.cs
//      dotnet run -e GREETING=Hallo app.cs
#:include helpers.cs
#:include models/customer.cs

var customer = new Customer("Vishal", "Augsburg");
var greeting = Environment.GetEnvironmentVariable("GREETING");

Console.WriteLine(Helpers.Format(greeting ?? "Hello", customer));
