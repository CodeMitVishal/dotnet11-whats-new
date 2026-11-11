// .NET 11 libraries · New in-memory streams and Zstandard
// Run: dotnet run 05-streams-and-zstandard.cs
using System.IO.Compression;
using System.Text;

string text = string.Concat(Enumerable.Repeat("dotnet ", 1000));

// StringStream: a string as a Stream, no byte[] copy
using var source = new StringStream(text, Encoding.UTF8);

// Zstandard: built in, next to GZip and Brotli
using var packed = new MemoryStream();
using (var zstd = new ZstandardStream(packed,
           CompressionMode.Compress, leaveOpen: true))
{
    source.CopyTo(zstd);
}
Console.WriteLine($"Before: {text.Length:N0} bytes");
Console.WriteLine($"After:  {packed.Length:N0} bytes");
