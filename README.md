# Gauss Seidel Elimination Numerical Method Implementation in Python

This repository contains a Python implementation of the Gauss-Seidel Elimination method for solving systems of linear equations. The code reads coefficients from an Excel file (`data.xls`), performs Gauss-Seidel iteration with relaxation, and saves the results in a new Excel file. The method also includes error checking and verifies the results.

## Table of Contents
- [Gauss-Seidel Elimination Theory](#gauss-seidel-elimination-theory)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Example](#example)
- [Files in the Repository](#files-in-the-repository)
- [Input Parameters](#input-parameters)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

## Gauss-Seidel Elimination Theory
The Gauss-Seidel method is an iterative technique for solving systems of linear equations. It improves upon the Jacobi method by using the latest updates to the values of the unknowns immediately within the iteration.

**Steps:**
1. Initialize initial guesses for all unknowns.
2. Iterate over each equation and solve for the current unknown using the latest available values of other unknowns.
3. Apply a relaxation factor to accelerate convergence.
4. Check for convergence by comparing the relative errors to a desired threshold.

## Dependencies
To run this code, you need the following libraries:
- `numpy`
- `xlrd`
- `xlwt`

## Installation
To install the required libraries, you can use `pip`:
```sh
pip install numpy xlrd xlwt
```

## Usage
1. Clone the repository.
2. Ensure the script and the Excel file (`data.xls`) are in the same directory.
3. Run the script using Python:
    ```sh
    python gauss_seidel_elimination.py
    ```
4. Provide the required inputs when prompted:
    - Enter the desired percentage relative error.
    - Enter the number of iterations.
    - Enter the relaxation factor.
5. The script will read the coefficients from the Excel file, perform Gauss-Seidel Elimination, and write the results into a new Excel file named `xlwt_example.xls`.

## Code Explanation
The code begins by importing the necessary libraries and defining a helper function `brcond_Seidel` to check the convergence condition. It then reads the coefficients and constants from the Excel file into numpy arrays. The main iteration loop performs Gauss-Seidel updates and checks for convergence. The results are written into a new sheet in an Excel file.

Below is a snippet from the code illustrating the main logic:

```python
import numpy as np
import xlrd
from xlwt import Workbook

def brcond_Seidel(E, err, n):
    a = 0
    for i in range(n):
        if E[i] < err:
            a += 1
    return a / n

err = float(input('Enter desired percentage relative error: '))
ite = int(input('Enter number of iterations: '))
relaxation = float(input('Enter relaxation factor: '))

loc = ('data.xls')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(3)

n = sheet.nrows
a = np.zeros([n, n+1])
E = np.zeros([n])
rel_err = np.zeros([ite, n])
X = np.zeros([n])
x = np.zeros([ite, n])
x_new = np.zeros([ite, n])
itern = np.zeros([ite])
p = np.zeros([n])

for i in range(sheet.ncols):
    for j in range(sheet.nrows):
        a[j, i] = sheet.cell_value(j, i)

# Iteration for Gauss-Seidel begins here
for j in range(ite):
    itern[j] = j + 1
    for i in range(n):
        summation = 0
        for k in range(n):
            if k != i:
                summation += a[i, k] * x[j, k]
        x_new[j, i] = (a[i, n] - summation) / a[i, i]
        if j > 0:
            x[j, i] = x_new[j, i] * relaxation + (1 - relaxation) * x[j-1, i]
        else:
            x[j, i] = x_new[j, i]
        if j > 0:
            rel_err[j, i] = abs((x[j, i] - x[j-1, i]) / x[j, i]) * 100
            E[i] = rel_err[j, i]

    if j > 0 and brcond_Seidel(E, err, n) == 1:
        break
    elif j == ite - 1:
        break

    x[j+1, :] = x[j, :]

num_of_iter = j
X = x[j, :]

print('The values of the unknown variables are respectively:')
print(X)

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

sheet1.write(0, n, 'Gauss')
sheet1.write(0, n+1, 'Seidel')
sheet1.write(1, 0, 'Number of iteration')

for i in range(1, n+1):
    sheet1.write(1, i, 'x_' + str(i))
for i in range(n+1, 2*n+1):
    sheet1.write(1, i, 'Relative error of x_' + str(i-n))

for i in range(num_of_iter+1):
    sheet1.write(i+2, 0, itern[i])
    for j in range(n):
        sheet1.write(i+2, 1+j, x[i, j])
        sheet1.write(i+2, n+1+j, rel_err[i, j])

sheet1.write(i+4, 0, 'The')
sheet1.write(i+4, 1, 'unknown')
sheet1.write(i+4, 2, 'values')
sheet1.write(i+4, 3, 'are:')
for k in range(n):
    sheet1.write(i+4, k+4, X[k])

wb.save('xlwt_example.xls')

# Result Verification
for i in range(n):
    summation = 0
    for j in range(n):
        summation += a[i, j] * X[j]
    p[i] = summation - a[i, j+1]

print('The verification results are:')
print(p)
print('The implementation is correct if verification results are all zero')
```

The code completes by saving the final results into the Excel file `xlwt_example.xls` and prints verification results.

## Example
Below is an example of how to use the script:

1. Prepare the `data.xls` file with the system of equations in matrix form.
2. **Run the script**:
    ```sh
    python gauss_seidel_elimination.py
    ```

3. **Enter the input values**:
    ```
    Enter desired percentage relative error: 0.001
    Enter number of iterations: 50
    Enter relaxation factor: 1.0
    ```

4. **Output**:
    - The script will compute the results using the Gauss-Seidel Elimination method and write the intermediate and final results into the Excel file (`xlwt_example.xls`).
    - The console will display the values of the unknowns and the verification results.

## Files in the Repository
- `gauss_seidel_elimination.py`: The main script for performing the Gauss-Seidel Elimination method.
- `data.xls`: Excel file from which the matrix data is read and into which the results are written.

## Input Parameters
The initial input data is expected to be in the form of a matrix within the `data.xls` file. Each row represents coefficients of the variables in the equations along with the constants.

## Troubleshooting
1. **Excel File**: Ensure that the input matrix is correct and placed in the `data.xls` file.
2. **Matrix Format**: Confirm that the matrix is complete and correctly formatted.
3. **Excel File Creation**: Ensure you have write permissions in the directory where the script is run to save the Excel file.
4. **Python Version**: This script is compatible with Python 3. Ensure you have Python 3 installed.

## Author
Script created by sudipto3331.

---

This documentation should guide you through understanding, installing, and using the Gauss-Seidel Elimination method script. For further issues or feature requests, please open an issue in the repository on GitHub. Feel free to contribute by creating issues and submitting pull requests. Happy coding!
