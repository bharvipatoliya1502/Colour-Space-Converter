"""Core matrix algorithms implemented without numpy.linalg."""

from typing import List

Matrix = List[List[float]]


def _validate_matrix(a: Matrix) -> None:
    if not isinstance(a, list) or not a or not all(isinstance(row, list) for row in a):
        raise ValueError("Matrix must be a non-empty list of rows.")
    width = len(a[0])
    if width == 0 or any(len(row) != width for row in a):
        raise ValueError("Matrix rows must have the same non-zero length.")
    for row in a:
        for value in row:
            if not isinstance(value, (int, float)):
                raise ValueError("Matrix entries must be numeric.")


def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """Multiply A (m×n) by B (n×p), using explicit loops."""
    _validate_matrix(a)
    _validate_matrix(b)
    if len(a[0]) != len(b):
        raise ValueError("Incompatible matrix dimensions for multiplication.")
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            total = 0.0
            for k in range(len(b)):
                total += float(a[i][k]) * float(b[k][j])
            row.append(total)
        result.append(row)
    return result


def determinant(matrix: Matrix, tolerance: float = 1e-12) -> float:
    """Compute determinant by Gaussian elimination with row swaps."""
    _validate_matrix(matrix)
    n = len(matrix)
    if len(matrix[0]) != n:
        raise ValueError("Determinant is defined only for square matrices.")
    a = [[float(x) for x in row] for row in matrix]
    det = 1.0
    sign = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < tolerance:
            return 0.0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1.0
        pivot_value = a[col][col]
        det *= pivot_value
        for r in range(col + 1, n):
            factor = a[r][col] / pivot_value
            for c in range(col + 1, n):
                a[r][c] -= factor * a[col][c]
            a[r][col] = 0.0
    return sign * det


def matrix_inverse(matrix: Matrix, tolerance: float = 1e-12) -> Matrix:
    """Compute inverse using Gauss-Jordan elimination with partial pivoting."""
    _validate_matrix(matrix)
    n = len(matrix)
    if len(matrix[0]) != n:
        raise ValueError("Only square matrices can be inverted.")
    left = [[float(x) for x in row] for row in matrix]
    right = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(left[r][col]))
        if abs(left[pivot][col]) < tolerance:
            raise ValueError("Matrix is singular and has no inverse.")
        if pivot != col:
            left[col], left[pivot] = left[pivot], left[col]
            right[col], right[pivot] = right[pivot], right[col]
        pivot_value = left[col][col]
        left[col] = [x / pivot_value for x in left[col]]
        right[col] = [x / pivot_value for x in right[col]]
        for r in range(n):
            if r == col:
                continue
            factor = left[r][col]
            left[r] = [left[r][c] - factor * left[col][c] for c in range(n)]
            right[r] = [right[r][c] - factor * right[col][c] for c in range(n)]
    return right


def matrix_rank(matrix: Matrix, tolerance: float = 1e-10) -> int:
    """Compute matrix rank by row reduction."""
    _validate_matrix(matrix)
    a = [[float(x) for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows:
            break
        pivot = max(range(pivot_row, rows), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < tolerance:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        pivot_value = a[pivot_row][col]
        a[pivot_row] = [x / pivot_value for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row:
                factor = a[r][col]
                a[r] = [a[r][c] - factor * a[pivot_row][c] for c in range(cols)]
        rank += 1
        pivot_row += 1
    return rank


def matrix_null_space(matrix: Matrix, tolerance: float = 1e-10):
    """Return a basis for the null space using RREF and free variables."""
    _validate_matrix(matrix)
    a = [[float(x) for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows:
            break
        pivot = max(range(pivot_row, rows), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) <= tolerance:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        value = a[pivot_row][col]
        a[pivot_row] = [x / value for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row:
                factor = a[r][col]
                a[r] = [a[r][c] - factor * a[pivot_row][c] for c in range(cols)]
        pivot_cols.append(col)
        pivot_row += 1
    free_cols = [c for c in range(cols) if c not in pivot_cols]
    basis = []
    for free in free_cols:
        vector = [0.0] * cols
        vector[free] = 1.0
        for r, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = -a[r][free]
        basis.append(vector)
    return basis
