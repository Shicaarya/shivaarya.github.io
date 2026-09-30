from math import sqrt, exp

print("Choose a function:")
print("1 = Parabola")
print("2 = Exponential")
choice = input("Enter 1 or 2: ")

if choice == "1":
    A = float(input("Enter A: "))
    B = float(input("Enter B: "))
    C = float(input("Enter C: "))

    def f(x):
        return A*x**2 + B*x + C

    def derivative1(x):
        return 2*A*x + B

    def derivative2(x):
        return 2*A

elif choice == "2":

    def f(x):
        return exp(x)

    def derivative1(x):
        return exp(x)

    def derivative2(x):
        return exp(x)

else:
    print("Invalid choice")
    exit()

t = float(input("Enter x-coordinate of point: "))
z = float(input("Enter y-coordinate of point: "))
x = float(input("Enter an initial guess for x: "))

for i in range(100):
    y = f(x)

    derivativeD = (
        2*(x - t)
        + 2*(y - z)*derivative1(x)
    )

    derivativeD2 = (
        2
        + 2*(derivative1(x)**2)
        + 2*(y - z)*derivative2(x)
    )

    xnew = x - derivativeD / derivativeD2

    print("iteration", i, "x =", xnew)

    if abs(xnew - x) < 0.0001:
        x = xnew
        break

    x = xnew

y = f(x)
distance = sqrt((x - t)**2 + (y - z)**2)

print("\nFinal result")
print("x =", x)
print("y =", y)
print("distance =", distance)
