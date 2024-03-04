import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def find_line_equation(x1, y1, x2, y2):
    # 計算斜率和截距
    slope = (y2 - y1) / (np.log10(x2) - np.log10(x1))
    intercept = y1 - slope * np.log10(x1)
    return slope, intercept

def find_intersection(slope1, intercept1, slope2, intercept2):
    # 定義方程式
    def equations(p):
        x, y = p
        eq1 = slope1 * np.log10(x) + intercept1 - y
        eq2 = slope2 * np.log10(x) + intercept2 - y
        return [eq1, eq2]

    # 初始猜測值，這裡使用交點附近的點
    initial_guess = [1, 1]

    # 使用 fsolve 求解方程式
    intersection_point = fsolve(equations, initial_guess)

    return intersection_point[0], intersection_point[1]


def extend_line(slope, intercept, x_values):
    y_values = slope * np.log10(x_values) + intercept
    return y_values

def plot_graph(sheet_name):
    # 讀取數據
    data = pd.read_excel("測試.xlsx", sheet_name=sheet_name)
    np.set_printoptions(suppress=True)
    data = data.drop(data.index[0]).reset_index(drop=True)

    # 計算初始值
    delta_d = data["沉陷S(mm)"][3] - data["沉陷S(mm)"][1]
    d0 = data["沉陷S(mm)"][1] - delta_d
    t0 = data["歷時(min)"][1] / 4
    Xmin = data["歷時(min)"][0]-0.02
    Ymin = data["沉陷S(mm)"][0]-0.1
    Xmax = data["歷時(min)"].iloc[-1]+0.02
    Ymax = data["沉陷S(mm)"].iloc[-1] + 0.1

    # 繪製曲線
    plt.plot(data["歷時(min)"], data["沉陷S(mm)"], color='#000000', marker="o", label='Curve')

    # 計算第一條切線的方程式
    slope1, intercept1 = find_line_equation(data["歷時(min)"][4], data["沉陷S(mm)"][4], data["歷時(min)"][5],
                                            data["沉陷S(mm)"][5])
    x_values1 = np.logspace(np.log10(data["歷時(min)"][2]), np.log10(data["歷時(min)"][8]), 1000)
    y_values1 = extend_line(slope1, intercept1, x_values1)
    # 繪製第一條切線
    plt.plot(x_values1, y_values1, color='g', label='Tangent Line 1')

    # 計算第二條切線的方程式
    slope2, intercept2 = find_line_equation(data["歷時(min)"][7], data["沉陷S(mm)"][7], data["歷時(min)"][8],
                                            data["沉陷S(mm)"][8])
    x_values2 = np.logspace(np.log10(data["歷時(min)"][5]), np.log10(data["歷時(min)"].iloc[-1]), 1000)
    y_values2 = extend_line(slope2, intercept2, x_values2)
    # 繪製第二條切線
    plt.plot(x_values2, y_values2, color='g', label='Tangent Line 2')

    # 找出兩條切線的交點
    intersection_point = find_intersection(slope1, intercept1, slope2, intercept2)
    d50 = (d0 + intersection_point[1]) / 2

    # 標記交點
    plt.scatter(intersection_point[0], intersection_point[1], color='red', label='Intersection Point', marker="x")

    # 設定水平線的點
    plt.hlines(data["沉陷S(mm)"][1], xmin=Xmin, xmax=data["歷時(min)"][1], color='#7B7B7B', linestyle='--')
    plt.hlines(data["沉陷S(mm)"][3], xmin=Xmin, xmax=data["歷時(min)"][3], color='#7B7B7B', linestyle='--')
    plt.hlines(d0, xmin=Xmin, xmax=data["歷時(min)"][1], color='#7B7B7B', linestyle='--')
    plt.hlines(d50, xmin=Xmin, xmax=Xmax, color='#7B7B7B')
    plt.vlines(intersection_point[0], ymin=intersection_point[1], ymax=Ymax, colors='red', )
    plt.vlines(data["歷時(min)"][1], ymin=Ymin, ymax=data["沉陷S(mm)"][3], colors='red', )

    # 顯示圖形
    plt.ticklabel_format(style='plain', axis='both')
    plt.ylim(Ymin, Ymax)
    plt.xlim(Xmin, Xmax)
    plt.grid(1)
    plt.xscale("log")
    plt.gca().invert_yaxis()
    plt.title(f'$ S-t(log scale) ,part{sheet_name}$',fontsize=16)
    plt.xlabel('$t(log scale)$',fontsize=16)
    plt.ylabel('$S(mm)$',fontsize=16)

    # 交互式選點
    clicked_points = plt.ginput(1)
    selected_point = clicked_points[0]
    plt.vlines(selected_point[0], ymin=selected_point[1], ymax=1, colors='#7B7B7B', )
    text_content = f'd0 = {d0:.3f}\nd50 = {d50:.3f}\nd100 = {intersection_point[1]:.3f}\n(t50, d50) = ({selected_point[0]:.3f}, {selected_point[1]:.3f})'
    plt.text(Xmax - 0.5, Ymin, text_content, fontsize=14, color='red', ha='center', va='center',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    plt.show()

# 调用函数，传入用户输入的 sheet_name
user_input = input("請輸入 sheet_name：")
plot_graph(user_input)
