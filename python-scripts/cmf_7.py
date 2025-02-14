import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def forward_diff_table(y_vals):
    n = len(y_vals)
    table = np.zeros((n, n))
    table[:, 0] = y_vals.copy()
    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = table[i+1, j-1] - table[i, j-1]
    return table

def main():
    data = json.loads(sys.stdin.read())
    response = {}
    
    try:
        x = np.array(data['x'], dtype=float)
        y = np.array(data['y'], dtype=float)
        x_deriv = float(data['x_deriv'])
        
        if len(x) != len(y):
            raise ValueError("Количество x и y должно совпадать")
            
        h = x[1] - x[0]
        if not np.allclose(np.diff(x), h, atol=1e-6):
            raise ValueError("Интервалы между x должны быть равными")
        
        # Расчет таблицы разностей
        diff_table = forward_diff_table(y)
        df = pd.DataFrame(diff_table)
        response['table'] = df.round(4).to_dict()
        
        # Расчет производной
        u = (x_deriv - x[0]) / h
        derivative = (1/h) * (diff_table[0, 1] + ((2*u - 1)/2) * diff_table[0, 2])
        response['derivative'] = round(derivative, 4)
        
        # Генерация графика
        plt.figure(figsize=(10, 6))
        x_dense = np.linspace(x[0], x[-1], 200)
        y_dense = [newton_poly(xi, x[0], h, diff_table) for xi in x_dense]
        y_point = newton_poly(x_deriv, x[0], h, diff_table)
        x_tangent = np.linspace(x_deriv - h, x_deriv + h, 50)
        y_tangent = y_point + derivative * (x_tangent - x_deriv)
        
        plt.plot(x_dense, y_dense, 'b-', label="Интерполяционный полином")
        plt.plot(x, y, 'ro', label="Узлы интерполяции")
        plt.plot(x_tangent, y_tangent, 'g--', label=f"Касательная (f'={derivative:.4f})")
        plt.grid(True)
        plt.legend()
        
        plot_path = f'public/images/task7_{abs(hash(str(data)))}.png'
        plt.savefig(plot_path)
        plt.close()
        response['plot'] = plot_path.replace('public/', '')
        
    except Exception as e:
        response['error'] = str(e)
        
    print(json.dumps(response))

def newton_poly(x_val, x0, h, diff_table):
    u = (x_val - x0) / h
    value = diff_table[0, 0]
    u_term = fact = 1
    for j in range(1, len(diff_table)):
        u_term *= (u - (j - 1))
        fact *= j
        value += (u_term / fact) * diff_table[0, j]
    return value

if __name__ == "__main__":
    main()