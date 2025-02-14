import sys
import json
import numpy as np

def jacobi_method(A, b, x0, tol=1e-6, max_iter=100):
    n = len(A)
    x = np.array(x0, dtype=float)
    x_new = np.zeros_like(x)
    
    for it in range(max_iter):
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        
        if np.linalg.norm(x_new - x, np.inf) < tol:
            return x_new.tolist(), it+1
        x = x_new.copy()
    
    return x.tolist(), max_iter

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    
    try:
        A = data['matrix']
        b = data['vector']
        x0 = data['initial']
        tol = float(data.get('tolerance', 1e-6))
        max_iter = int(data.get('max_iterations', 100))
        
        solution, iterations = jacobi_method(A, b, x0, tol, max_iter)
        print(json.dumps({
            "solution": solution,
            "iterations": iterations,
            "matrix": A,
            "vector": b,
            "error": None
        }))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Ошибка: {str(e)}",
            "solution": None,
            "iterations": 0
        }))