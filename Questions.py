# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score


# np.random.seed(0)
# x = np.sort(np.random.rand(100, 1) * 10)  # Increases the size of the dataset
# y = 1 + 2 * (x ** 2) + 3 * (x ** 3) + np.random.randn(100, 1) * 10  # A cubic polynomial with noise


# plt.scatter(x, y, color='blue')
# plt.title('Complex Polynomial Data')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)


# degree = 5  # Change degree for more complexity
# poly = PolynomialFeatures(degree=degree)
# x_poly_train = poly.fit_transform(x_train)
# x_poly_test = poly.transform(x_test)


# model = LinearRegression()
# model.fit(x_poly_train, y_train)


# # Get coefficients and intercept
# coefficients = model.coef_
# intercept = model.intercept_

# # Print the coefficients and intercept
# print(f'Intercept: {intercept[0]}')
# print('Coefficients:', coefficients[0])

# polynomial_equation = f"y = {intercept[0]}"
# for i in range(1, len(coefficients[0])):
#     polynomial_equation += f" + {coefficients[0][i]} * x^{i}"

# print(polynomial_equation)


# y_pred = model.predict(x_poly_test)

# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# print(f'Mean Squared Error: {mse}')
# print(f'R^2 Score: {r2}')



# plt.scatter(x, y, color='blue')
# plt.scatter(x_test, y_test, color='red')  # Original test data
# plt.scatter(x_test, y_pred, color='green')  # Predicted values

# # Optional: For better visualization, plot the smooth curve for the polynomial fit
# x_plot = np.linspace(0, 10, 100).reshape(-1, 1)
# y_plot = model.predict(poly.transform(x_plot))
# plt.plot(x_plot, y_plot, color='orange', linewidth=2)  # Fitted polynomial line

# plt.title('Complex Polynomial Regression')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend(['Original Data', 'Test Data', 'Predictions', 'Fitted Polynomial'])
# plt.show()






import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

data = [
    (1892, 3),
    (1893, 1),
    (1894, 7),
    (1895, 18),
    (1896, 106),
    (1897, 37),
    (1898, 31),
    (1899, 24),
    (1900, 41),
    (1901, 19),
    (1902, 14),
    (1903, 26),
    (1904, 9),
    (1905, 14),
    (1906, 19),
    (1907, 29),
    (1908, 105),
    (1909, 188),
    (1910, 144),
    (1911, 153),
    (1912, 195),
    (1913, 192),
    (1914, 276),
    (1915, 344),
    (1916, 286),
    (1917, 325),
    (1918, 296),
    (1919, 110),
    (1920, 3),
    (1921, 2),
    (1922, 1),
    (1925, 2),
    (1936, 1),
    (1990, 1),
]

# Create separate lists for startYear and count
startYear = np.array([year for year, count in data])
count = np.array([count for year, count in data])

# Calculate the offset
offset = startYear.min()

# Adjust x values by subtracting the minimum value
startYear_offset = startYear - offset
x = startYear_offset.reshape(-1, 1)
y = count.reshape(-1, 1)

# # Split the data
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Define weights for each data point (same length as x and y)
weights = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

# Split the data
x_train, x_test, y_train, y_test, weights_train, weights_test = train_test_split(x, y, weights, test_size=0.2, random_state=0)


# Create a pipeline for polynomial regression
degree = 8
model_pipeline = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())

# Fit the model
model_pipeline.fit(x_train, y_train, linearregression__sample_weight=weights_train)

# Make predictions
y_pred = model_pipeline.predict(x_test)

# Get the coefficients and intercept
poly = model_pipeline.named_steps['polynomialfeatures']  # Get the PolynomialFeatures step
linear_reg = model_pipeline.named_steps['linearregression']  # Get the LinearRegression step

coefficients = linear_reg.coef_
intercept = linear_reg.intercept_

print(x_train, y_train)
print()
print(x_test, y_test)
print()
print(y_pred)

# Display the polynomial equation
polynomial_equation = f"y = {intercept[0]}"
for i in range(1, len(coefficients[0])):
    polynomial_equation += f" + {coefficients[0][i]} * x^{i}"

print(polynomial_equation)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

plt.figure()
# Optional: Plotting for visualization
plt.plot(startYear, count, color='blue', label='Data')
plt.scatter(startYear[x_test.flatten() + offset - offset], y_test, color='red', label='Test Data')
plt.scatter(startYear[x_test.flatten() + offset - offset], y_pred, color='green', label='Predictions')

# Plotting the fitted polynomial curve
x_plot = np.linspace(min(startYear_offset), max(startYear_offset), 100).reshape(-1, 1)
y_plot = model_pipeline.predict(x_plot)
plt.plot(x_plot + offset, y_plot, color='orange', linewidth=2, label=f'Fitted Polynomial, deg {degree}')

plt.title('Polynomial Regression with Pipeline')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.show()


