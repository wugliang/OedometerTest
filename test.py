import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("測試.xlsx", sheet_name="e")
np.set_printoptions(suppress=True)
data['壓力P(kg/cm2)'] = data['壓力P(kg/cm2)']
# data['壓力P(kg/cm2)'] = data['壓力P(kg/cm2)'] * 98.1

plt.ticklabel_format(style='plain', axis='both')
plt.plot(data['壓力P(kg/cm2)'], data['孔隙比e'], color='#000000', label='Regression line', marker='o')

# Cs = (data['孔隙比e'][9] - data['孔隙比e'][6]) / (np.log10(data['壓力P(kg/cm2)'][9]) - np.log10(data['壓力P(kg/cm2)'][6]))
# Cc = (data['孔隙比e'][5] - data['孔隙比e'][2]) / (np.log10(data['壓力P(kg/cm2)'][5]) - np.log10(data['壓力P(kg/cm2)'][2]))
#
# # 根據實際數據點調整位置
# text_x = data['壓力P(kg/cm2)'][6]  # 你可能需要根據你的數據進行調整
# text_y = data['孔隙比e'][0]  # 你可能需要根據你的數據進行調整
#
#
# text_content = f'Cc = {Cc:.3f}\nCs = {Cs:.3f}'
# plt.text(text_x, text_y, text_content, fontsize=12, color='red', ha='center', va='center',
#          bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
# plt.grid(1)
# plt.xscale("log")
# plt.title('$e-\sigma$ (log scale)',fontsize=16)
# plt.xlabel('$\sigma$ (kPa), log scale',fontsize=16)
# plt.ylabel('$e$',fontsize=16)

plt.grid(1)
plt.title('$e-\sigma$ ',fontsize=16)
plt.xlabel('$\sigma$ (kgf/cm$^2$)',fontsize=16)
plt.ylabel('$e$',fontsize=16)

plt.show()
