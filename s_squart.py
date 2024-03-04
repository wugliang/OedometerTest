import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

def find_line_equation(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    x_values = np.linspace(0, 2, 10)
    return slope, intercept, x_values

def find_intersection(slope1, intercept1, slope2, intercept2):
    x_intersection = (intercept2 - intercept1) / (slope1 - slope2)
    y_intersection = slope1 * x_intersection + intercept1
    return x_intersection, y_intersection

def plot_graph(sheet_name):
    # 讀取數據
    data = pd.read_excel("測試.xlsx", sheet_name=sheet_name)
    np.set_printoptions(suppress=True)

    # 對歷時進行開根號
    data["歷時(min)"] = np.sqrt(data["歷時(min)"].astype(float))
    data = data.drop(data.index[0]).reset_index(drop=True)

    # 設定圖表
    Xmin = data["歷時(min)"][0] - 0.5
    Ymin = data["沉陷S(mm)"][0] - 0.05
    Xmax = data["歷時(min)"].iloc[-1] + 0.5
    Ymax = data["沉陷S(mm)"].iloc[-1] + 0.05

    # 繪製曲線
    plt.plot(data["歷時(min)"], data["沉陷S(mm)"], color='#000000', marker="o", label='Curve')

    # 計算第一條切線的方程式
    slope1, intercept1, x_values1 = find_line_equation(data["歷時(min)"][1], data["沉陷S(mm)"][1], data["歷時(min)"][2],
                                                        data["沉陷S(mm)"][2])
    y_values1 = slope1 * x_values1 + intercept1

    # 標記交點截距A、B
    Ax=(Ymax-intercept1)/slope1
    Bx=1.5*Ax
    Ay=By=Ymax
    dsx=Xmin
    dsy=slope1 * Xmin + intercept1
    plt.scatter(Ax, Ay, color='red', label='Intersection Point', marker="x")
    plt.scatter(Bx,By, color='red', label='Intersection Point', marker="x")

    # 繪製切線
    plt.plot([dsx,Ax], [dsy,Ay], color='g', label='Tangent Line 1')
    plt.plot([dsx,Bx], [dsy,By], color='g', label='Tangent Line 1')
    # 設定水平線的點

    # 顯示圖形
    plt.ticklabel_format(style='plain', axis='both')
    plt.ylim(Ymin, Ymax)
    plt.xlim(Xmin, Xmax)
    plt.grid(1)
    plt.gca().invert_yaxis()
    plt.title(f'S-$\sqrt{{t}}$,part{sheet_name}',fontsize=16)
    plt.xlabel('$\sqrt{{t}}$',fontsize=16)
    plt.ylabel('$S(mm)$',fontsize=16)

    # 交互式選點
    clicked_points = plt.ginput(1)
    selected_point = clicked_points[0]
    plt.vlines(selected_point[0], ymin=selected_point[1], ymax=1, colors='#7B7B7B', )
    text_content = f'A=({dsx:.3f},{dsy:.3f})\nB=({Ax:.3f},{Ay:.3f})\nC=({Bx:.3f},{By:.3f})\n($\sqrt{{t90}}$, d90) = ({selected_point[0]:.3f}, {selected_point[1]:.3f})'
    plt.text(Xmax - 0.5, Ymin, text_content, fontsize=14, color='red', ha='center', va='center',
              bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    plt.show()

# 调用函数，传入用户输入的 sheet_name
user_input = input("請輸入 sheet_name：")
plot_graph(user_input)
