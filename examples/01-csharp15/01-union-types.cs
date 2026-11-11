// C# 15 · Union types
// Run: dotnet run 01-union-types.cs

// Implicit conversion: a Dog is a Pet
Pet pet = new Dog("Rex");
Console.WriteLine(Describe(pet));

pet = new Cat("Misty");
Console.WriteLine(Describe(pet));

// Every case is handled, so no "default" arm
static string Describe(Pet pet) => pet switch
{
    Dog d  => $"{d.Name} barks",
    Cat c  => $"{c.Name} meows",
    Bird b => $"{b.Name} sings",
};

public record Cat(string Name);
public record Dog(string Name);
public record Bird(string Name);

// A Pet is exactly one of: Cat, Dog or Bird
public union Pet(Cat, Dog, Bird);
