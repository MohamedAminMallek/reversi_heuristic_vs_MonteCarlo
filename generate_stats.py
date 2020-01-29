import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

filename = "results_50_epochs"
df_stats = pd.read_csv(filename+".csv")

columns = df_stats.columns

win_first = df_stats.iloc[:,[0]].values
win_second = df_stats.iloc[:,[1]].values

lose_first = df_stats.iloc[:,[2]].values
lose_second = df_stats.iloc[:,[3]].values

resources = df_stats.iloc[:,[4]].values

mcts_timer = df_stats.iloc[:,[5]].values

other_timer = df_stats.iloc[:,[6]].values


wins = (win_first+win_second).astype(int)
loses = (lose_first+lose_second).astype(int)


fig, axs = plt.subplots(2,2,sharey='row',figsize=(10,8))
fig.suptitle('Monte Carlo Vs Random')

axs[0,0].plot(resources,wins)
axs[0,1].plot(resources,loses)
axs[1,0].plot(resources,mcts_timer)

axs[0,0].set(xlabel='resources(samples)', ylabel='nb wins')
axs[0,1].set(xlabel='resources(samples)', ylabel='nb loses')
axs[1,0].set(xlabel='resources(samples)', ylabel='Time(sec) per move')
plt.savefig(filename)
plt.show()