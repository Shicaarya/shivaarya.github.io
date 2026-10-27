import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("housing.data")

X = data[:, :-1]
y = data[:, -1]

X_train = X[:100]
y_train = y[:100]

X_test = X[100:]
y_test = y[100:]

mean = np.mean(X_train, axis=0)
std = np.std(X_train, axis=0)

std[std == 0] = 1

X_train_n = (X_train - mean) / std
X_test_n = (X_test - mean) / std


def polynomial_features(X, degree):
    features = []

    for d in range(1, degree + 1):
        features.append(X ** d)

    return np.hstack(features)


# Part 1(a)

train_errors = []
test_errors = []

for degree in range(1, 8):
    Phi_train = polynomial_features(X_train_n, degree)
    Phi_test = polynomial_features(X_test_n, degree)

    Phi_train = np.column_stack(
        (np.ones(len(Phi_train)), Phi_train)
    )

    Phi_test = np.column_stack(
        (np.ones(len(Phi_test)), Phi_test)
    )

    w = np.linalg.pinv(Phi_train) @ y_train

    y_train_pred = Phi_train @ w
    y_test_pred = Phi_test @ w

    train_rms = np.sqrt(
        np.mean((y_train_pred - y_train) ** 2)
    )

    test_rms = np.sqrt(
        np.mean((y_test_pred - y_test) ** 2)
    )

    train_errors.append(train_rms)
    test_errors.append(test_rms)

    print(
        "Degree:",
        degree,
        "Train RMS:",
        train_rms,
        "Test RMS:",
        test_rms
    )


degrees = range(1, 8)

plt.plot(
    degrees,
    train_errors,
    marker='o',
    label='Training RMS'
)

plt.plot(
    degrees,
    test_errors,
    marker='o',
    label='Test RMS'
)

plt.xlabel('Polynomial Degree')
plt.ylabel('RMS Error (log scale)')
plt.title('Training and Test RMS Error vs Polynomial Degree')
plt.yscale('log')
plt.legend()
plt.grid()
plt.show()


# Part 1(b)

Phi_train = polynomial_features(X_train_n, 1)

Phi_train = np.column_stack(
    (np.ones(len(Phi_train)), Phi_train)
)

w = np.linalg.pinv(Phi_train) @ y_train

print("\nDegree 1 Weights:")

for i, weight in enumerate(w):
    print("w", i, "=", weight)


# Part 1(c)

x_train_1d = X_train_n[:, 1]
x_test_1d = X_test_n[:, 1]

degrees_to_plot = [1, 3, 7]

for degree in degrees_to_plot:

    Phi_train = np.column_stack(
        [
            x_train_1d ** d
            for d in range(1, degree + 1)
        ]
    )

    Phi_train = np.column_stack(
        (np.ones(len(Phi_train)), Phi_train)
    )

    w = np.linalg.pinv(Phi_train) @ y_train

    x_line = np.linspace(
        min(x_train_1d.min(), x_test_1d.min()),
        max(x_train_1d.max(), x_test_1d.max()),
        300
    )

    Phi_line = np.column_stack(
        [
            x_line ** d
            for d in range(1, degree + 1)
        ]
    )

    Phi_line = np.column_stack(
        (np.ones(len(Phi_line)), Phi_line)
    )

    y_line = Phi_line @ w

    plt.figure()

    plt.scatter(
        x_train_1d,
        y_train,
        label='Training Data'
    )

    plt.scatter(
        x_test_1d,
        y_test,
        label='Test Data'
    )

    plt.plot(
        x_line,
        y_line,
        label='Polynomial'
    )

    plt.xlabel('Normalized Feature 2')
    plt.ylabel('Median House Value')
    plt.title(
        f'Polynomial Regression - Degree {degree}'
    )

    plt.legend()
    plt.grid()
    plt.show()


# Part 1(d)

lambdas = [0, 0.01, 0.1, 1, 10, 100, 1000]
degree = 8

validation_errors = []

for lam in lambdas:

    fold_errors = []

    for fold in range(10):

        start = fold * 10
        end = start + 10

        X_val_raw = X_train[start:end]
        y_val = y_train[start:end]

        X_train_fold_raw = np.concatenate(
            (X_train[:start], X_train[end:])
        )

        y_train_fold = np.concatenate(
            (y_train[:start], y_train[end:])
        )

        mean_fold = np.mean(
            X_train_fold_raw,
            axis=0
        )

        std_fold = np.std(
            X_train_fold_raw,
            axis=0
        )

        std_fold[std_fold == 0] = 1

        X_train_fold_n = (
            X_train_fold_raw - mean_fold
        ) / std_fold

        X_val_n = (
            X_val_raw - mean_fold
        ) / std_fold

        x_train_fold = X_train_fold_n[:, 1]
        x_val = X_val_n[:, 1]

        Phi_train = np.column_stack(
            [
                x_train_fold ** d
                for d in range(1, degree + 1)
            ]
        )

        Phi_train = np.column_stack(
            (np.ones(len(Phi_train)), Phi_train)
        )

        Phi_val = np.column_stack(
            [
                x_val ** d
                for d in range(1, degree + 1)
            ]
        )

        Phi_val = np.column_stack(
            (np.ones(len(Phi_val)), Phi_val)
        )

        I = np.eye(
            Phi_train.shape[1]
        )

        I[0, 0] = 0

        w = np.linalg.pinv(
            Phi_train.T @ Phi_train
            + lam * I
        ) @ Phi_train.T @ y_train_fold

        y_val_pred = Phi_val @ w

        rms = np.sqrt(
            np.mean(
                (y_val_pred - y_val) ** 2
            )
        )

        fold_errors.append(rms)

    validation_errors.append(
        np.mean(fold_errors)
    )


for lam, err in zip(
    lambdas,
    validation_errors
):

    print(
        "lambda =",
        lam,
        "average validation RMS =",
        err
    )


plt.semilogx(
    lambdas[1:],
    validation_errors[1:],
    marker='o'
)

plt.xlabel('Lambda')
plt.ylabel('Average Validation RMS Error')
plt.title(
    '10-Fold Cross-Validation for Degree-8 Polynomial'
)

plt.grid()
plt.show()

print(
    "Validation error for lambda = 0:",
    validation_errors[0]
)

best_index = np.argmin(
    validation_errors
)

print(
    "Best lambda:",
    lambdas[best_index]
)

print(
    "Best validation RMS:",
    validation_errors[best_index]
)


# Part 2(e)

def gaussian_features(
    X,
    centers,
    sigma=1.0
):
    Phi = []

    for center in centers:

        dist2 = np.sum(
            (X - center) ** 2,
            axis=1
        )

        Phi.append(
            np.exp(
                -dist2 / (2 * sigma ** 2)
            )
        )

    return np.column_stack(Phi)


np.random.seed(0)

basis_counts = list(
    range(5, 100, 10)
)

gaussian_train_errors = []
gaussian_test_errors = []

perm = np.random.permutation(
    len(X_train_n)
)

for K in basis_counts:

    center_indices = perm[:K]
    centers = X_train_n[center_indices]

    Phi_train = gaussian_features(
        X_train_n,
        centers
    )

    Phi_test = gaussian_features(
        X_test_n,
        centers
    )

    Phi_train = np.column_stack(
        (np.ones(len(Phi_train)), Phi_train)
    )

    Phi_test = np.column_stack(
        (np.ones(len(Phi_test)), Phi_test)
    )

    w = np.linalg.pinv(
        Phi_train
    ) @ y_train

    train_pred = Phi_train @ w
    test_pred = Phi_test @ w

    train_rms = np.sqrt(
        np.mean(
            (train_pred - y_train) ** 2
        )
    )

    test_rms = np.sqrt(
        np.mean(
            (test_pred - y_test) ** 2
        )
    )

    gaussian_train_errors.append(
        train_rms
    )

    gaussian_test_errors.append(
        test_rms
    )

    print(
        K,
        train_rms,
        test_rms
    )


plt.plot(
    basis_counts,
    gaussian_train_errors,
    marker='o',
    label='Training RMS'
)

plt.plot(
    basis_counts,
    gaussian_test_errors,
    marker='o',
    label='Test RMS'
)

plt.xlabel(
    'Number of Gaussian Basis Functions'
)

plt.ylabel('RMS Error')
plt.title('Gaussian Basis Regression')

plt.legend()
plt.grid()
plt.show()


# Part 2(f)

lambdas = [
    0,
    0.01,
    0.1,
    1,
    10,
    100,
    1000
]

validation_errors_gaussian = []

for lam in lambdas:

    fold_errors = []

    for fold in range(10):

        start = fold * 10
        end = start + 10

        X_val_raw = X_train[start:end]
        y_val = y_train[start:end]

        X_train_fold_raw = np.concatenate(
            (X_train[:start], X_train[end:])
        )

        y_train_fold = np.concatenate(
            (y_train[:start], y_train[end:])
        )

        mean_fold = np.mean(
            X_train_fold_raw,
            axis=0
        )

        std_fold = np.std(
            X_train_fold_raw,
            axis=0
        )

        std_fold[std_fold == 0] = 1

        X_train_fold_n = (
            X_train_fold_raw - mean_fold
        ) / std_fold

        X_val_n = (
            X_val_raw - mean_fold
        ) / std_fold

        centers = X_train_fold_n

        Phi_train = gaussian_features(
            X_train_fold_n,
            centers
        )

        Phi_val = gaussian_features(
            X_val_n,
            centers
        )

        Phi_train = np.column_stack(
            (
                np.ones(len(Phi_train)),
                Phi_train
            )
        )

        Phi_val = np.column_stack(
            (
                np.ones(len(Phi_val)),
                Phi_val
            )
        )

        I = np.eye(
            Phi_train.shape[1]
        )

        I[0, 0] = 0

        w = np.linalg.pinv(
            Phi_train.T @ Phi_train
            + lam * I
        ) @ Phi_train.T @ y_train_fold

        y_val_pred = Phi_val @ w

        rms = np.sqrt(
            np.mean(
                (y_val_pred - y_val) ** 2
            )
        )

        fold_errors.append(rms)

    validation_errors_gaussian.append(
        np.mean(fold_errors)
    )


for lam, err in zip(
    lambdas,
    validation_errors_gaussian
):

    print(
        "lambda =",
        lam,
        "average validation RMS =",
        err
    )


plt.semilogx(
    lambdas[1:],
    validation_errors_gaussian[1:],
    marker='o'
)

plt.xlabel('Lambda')
plt.ylabel('Average Validation RMS Error')
plt.title(
    'Gaussian Regression 10-Fold Cross-Validation'
)

plt.grid()
plt.show()

print(
    "Validation error for lambda = 0:",
    validation_errors_gaussian[0]
)

best_index = np.argmin(
    validation_errors_gaussian
)

print(
    "Best lambda:",
    lambdas[best_index]
)

print(
    "Best validation RMS:",
    validation_errors_gaussian[best_index]
)