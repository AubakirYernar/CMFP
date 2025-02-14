import sys
import json
import numpy as np

def iterative_inverse(A, max_iter=100, tol=1e-6):
    """Итеративный метод Ньютона-Шульца"""
    n = A.shape[0]
    X = 0.1 * np.eye(n)  # Начальное приближение
    for _ in range(max_iter):
        X_new = 2*X - X @ A @ X
        if np.linalg.norm(X_new - X) < tol:
            break
        X = X_new
    return X_new

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    response = {}
    
    try:
        # Преобразование входных данных
        matrix = np.array(data['matrix'], dtype=float)
        n = len(matrix)
        
        # Проверка квадратности
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной!")
            
        # Проверка на вырожденность
        if np.linalg.det(matrix) < 1e-6:
            raise ValueError("Матрица вырождена!")
        
        # Вычисления
        approx_inv = iterative_inverse(matrix).tolist()
        exact_inv = np.linalg.inv(matrix).tolist()
        error = np.linalg.norm(np.array(approx_inv) - np.array(exact_inv))
        
        response = {
            "approximate": approx_inv,
            "exact": exact_inv,
            "error": round(error, 6)
        }
        
    except Exception as e:
        response["error"] = str(e)
    
    print(json.dumps(response))