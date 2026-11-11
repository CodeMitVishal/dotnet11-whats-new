// .NET 11 libraries · Async validation with DataAnnotations
// Run: dotnet run 06-async-validation.cs
using System.ComponentModel.DataAnnotations;

var invoice = new Invoice("DE000");
var errors = new List<ValidationResult>();
bool ok = await Validator.TryValidateObjectAsync(
    invoice, new ValidationContext(invoice), errors, true);
Console.WriteLine(ok ? "Valid" : errors[0].ErrorMessage);

record Invoice([property: VatRegistered] string VatNumber);
class VatRegisteredAttribute : AsyncValidationAttribute
{
    protected override async Task<ValidationResult?> IsValidAsync(
        object? value, ValidationContext ctx, CancellationToken ct)
    {
        await Task.Delay(100, ct);   // e.g. ask the tax office
        return value is "DE123" ? ValidationResult.Success
            : new ValidationResult("VAT number not registered.");
    }
    protected override ValidationResult? IsValid(object? value,
        ValidationContext ctx) => throw new NotSupportedException();
}
