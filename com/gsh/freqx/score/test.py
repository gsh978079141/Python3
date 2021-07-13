import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import display

plt.style.use("fivethirtyeight")
sns.set_style({'font.sans-serif': ['simhei', 'Arial']})

# 导入csv原始数据
originl_df = pd.read_csv('data/WHQ_601fc44f1ea191508a3cec66_HZ_20210419_100000.csv')
display(originl_df.head(n=2))

originl_df.describe()

print("originl_df : %s" %originl_df)

# copy
df_f_fft = originl_df[['f', "fft"]]
# df = originl_df[['f', "fft"]]
# display(df_f_fft.head(n=2))
# 重新摆放列位置 f,fft,hht,raw,t
# columns = ['f', 'fft']
# df_f_fft = pd.DataFrame(df_f_fft, columns=columns)
# 重新审视数据集
display(df_f_fft.head(n=2))
print(df_f_fft)
# 在二维空间里画出身高和体重的分布图
plt.scatter(df_f_fft['f'], df_f_fft['fft'], color='black')
plt.xlabel('height (cm)')
plt.ylabel('weight (kg)')
plt.show()

# fig, ax = plt.subplots() # 创建一个子图
# sns.barplot(x='f', y='fft', data=df_f_fft, ax=ax)
# ax.set_title('频率幅值谱',fontsize=15)
# ax.set_xlabel('f')
# ax.set_ylabel('fft')
# plt.show() # 图1


