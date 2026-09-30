a = float(input("Enter a: "))
b = float(input("Enter b: "))
c = float(input("Enter c: "))

numberofpoints = int(input("How many points do you have? "))
total_points = numberofpoints

xstore = []
ystore = []

while numberofpoints > 0:
    x = float(input("Enter x-coordinate of point: "))
    y = float(input("Enter y-coordinate of point: "))

    xstore.append(x)
    ystore.append(y)

    numberofpoints = numberofpoints - 1

for iteration in range(100):

    partialdrive_a = 0

    for i in range(total_points):
        prediction = a*xstore[i]**2 + b*xstore[i] + c
        error = prediction - ystore[i]
        partialdrive_a += xstore[i]**2 * error

    partialdrive_a = (2 / total_points) * partialdrive_a

    second_a = 0

    for i in range(total_points):
        second_a += xstore[i]**4

    second_a = (2 / total_points) * second_a

    a_new = a - partialdrive_a / second_a

    partialdrive_b = 0

    for i in range(total_points):
        prediction = a_new*xstore[i]**2 + b*xstore[i] + c
        error = prediction - ystore[i]
        partialdrive_b += xstore[i] * error

    partialdrive_b = (2 / total_points) * partialdrive_b

    second_b = 0

    for i in range(total_points):
        second_b += xstore[i]**2

    second_b = (2 / total_points) * second_b

    b_new = b - partialdrive_b / second_b

    partialdrive_c = 0

    for i in range(total_points):
        prediction = a_new*xstore[i]**2 + b_new*xstore[i] + c
        error = prediction - ystore[i]
        partialdrive_c += error

    partialdrive_c = (2 / total_points) * partialdrive_c

    second_c = 2

    c_new = c - partialdrive_c / second_c

    print("Iteration", iteration)
    print("a =", a_new)
    print("b =", b_new)
    print("c =", c_new)

    if (abs(a_new - a) < 0.0001
        and abs(b_new - b) < 0.0001
        and abs(c_new - c) < 0.0001):

        a = a_new
        b = b_new
        c = c_new
        break

    a = a_new
    b = b_new
    c = c_new

squared_errors = []

for i in range(total_points):
    prediction = a*xstore[i]**2 + b*xstore[i] + c
    error = prediction - ystore[i]
    squared_errors.append(error**2)

final_MSE = sum(squared_errors) / total_points

print("Final a =", a)
print("Final b =", b)
print("Final c =", c)
print("Final MSE =", final_MSE)
