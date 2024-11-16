import pickle
from fractions import Fraction

def save_matrix(matrix, filename):
    """
    Сохраняет матрицу в файл с помощью pickle.
    """
    with open(filename, 'wb') as f:
        pickle.dump(matrix, f)

def load_matrix(filename):
    """
    Загружает матрицу из файла с помощью pickle.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)

def normalize_matrix(matrix):
    """
    Нормализует матрицу переходов, чтобы сумма каждой строки была равна 1.
    """
    normalized = []
    for row in matrix:
        row_sum = sum(row)
        if row_sum == 0:
            normalized.append(row)
        else:
            normalized.append([elem / row_sum for elem in row])
    return normalized
