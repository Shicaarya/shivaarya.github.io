m = float(input("Enter m: "))
b = float(input("Enter b: "))

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

    partialdrive_m = 0

    for i in range(total_points):
        prediction = m * xstore[i] + b
        error = prediction - ystore[i]
        partialdrive_m += xstore[i] * error

    partialdrive_m = (2 / total_points) * partialdrive_m

    second_m = 0

    for i in range(total_points):
        second_m += xstore[i] ** 2

    second_m = (2 / total_points) * second_m

    m_new = m - partialdrive_m / second_m

    partialdrive_b = 0

    for i in range(total_points):
        prediction = m_new * xstore[i] + b
        error = prediction - ystore[i]
        partialdrive_b += error

    partialdrive_b = (2 / total_points) * partialdrive_b

    second_b = 2

    b_new = b - partialdrive_b / second_b

    print("Iteration", iteration)
    print("m =", m_new)
    print("b =", b_new)

    if abs(m_new - m) < 0.0001 and abs(b_new - b) < 0.0001:
        m = m_new
        b = b_new
        break

    m = m_new
    b = b_new

squared_errors = []

for i in range(total_points):
    prediction = m * xstore[i] + b
    error = prediction - ystore[i]
    squared_errors.append(error ** 2)

final_MSE = sum(squared_errors) / total_points

print("Final m =", m)
print("Final b =", b)
print("Final MSE =", final_MSE)
