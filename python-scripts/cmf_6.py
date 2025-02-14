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
        x_interp = float(data['x_interp'])
        
        if len(x) != len(y):
            raise ValueError("Количество x и y должно совпадать")
            
        h = x[1] - x[0]
        if not np.allclose(np.diff(x), h, atol=1e-6):
            raise ValueError("Интервалы между x должны быть равными")
        
        # Расчет таблицы разностей
        diff_table = forward_diff_table(y)
        df = pd.DataFrame(diff_table)
        response['table'] = df.round(4).to_dict()
        
        # Интерполяция
        u = (x_interp - x[0]) / h
        interp_value = y[0]
        u_term = fact = 1
        
        for j in range(1, len(x)):
            u_term *= (u - (j - 1))
            fact *= j
            interp_value += (u_term / fact) * diff_table[0, j]
            
        response['value'] = round(interp_value, 4)
        
        # Генерация графика
        plt.figure(figsize=(10, 6))
        x_dense = np.linspace(x[0], x[-1], 200)
        y_dense = [interp_value]
        plt.plot(x_dense, [newton_poly((xi - x[0])/h, diff_table, h) for xi in x_dense], 'b-')
        plt.plot(x, y, 'ro', label="Узлы")
        plt.plot(x_interp, interp_value, 'gs')
        plt.grid(True)
        plot_path = f'public/images/task6_{abs(hash(str(data)))}.png'
        plt.savefig(plot_path)
        plt.close()
        response['plot'] = plot_path.replace('public/', '')
        
    except Exception as e:
        response['error'] = str(e)
        
    print(json.dumps(response))

def newton_poly(u, diff_table, h):
    value = diff_table[0, 0]
    u_term = fact = 1
    for j in range(1, len(diff_table)):
        u_term *= (u - (j - 1))
        fact *= j
        value += (u_term / fact) * diff_table[0, j]
    return value

if __name__ == "__main__":
    main()