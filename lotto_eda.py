import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# data를 로드
eda_data = pd.read_csv('final_data.csv')

# data를 1회차부터 정렬
eda_data = eda_data.sort_values(by='turn_nm', ascending=True)
eda_data.index = eda_data.index.sort_values(ascending=True)

# barplot 사용자 정의 함수
def bar_plot(col, data, hue=None):
    f, ax = plt.subplots(figsize=(10,5))
    sns.countplot(x=col, hue=hue, data=data, alpha=0.5)
    plt.show

bar_plot(eda_data.num_1, eda_data, hue=None)
bar_plot(eda_data.num_2, eda_data, hue=None)
bar_plot(eda_data.num_3, eda_data, hue=None)
bar_plot(eda_data.num_4, eda_data, hue=None)
bar_plot(eda_data.num_5, eda_data, hue=None)
bar_plot(eda_data.num_6, eda_data, hue=None)
bar_plot(eda_data.num_bonus, eda_data, hue=None)