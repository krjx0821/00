# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 15:11:53 2020

@author: 19749
"""
import pandas as pd
#读取表格
df1 = pd.read_excel('00.xls', encoding = "gb2312",sheet_name = 'Sheet4',
                    usecols=['日期', '证券代码', '市值', '市值比净值(%)', 'type'])
df1 = df1.iloc[:-1]
df1 = df1.sort_values(by = ['证券代码', '日期'])
df1['证券代码'] = [str(int(i)).zfill(6) for i in df1['证券代码']]

code_list = df1['证券代码'].sort_values().unique().tolist()
date_list = df1['日期'].sort_values().unique().tolist()
a = [0 for i in date_list]
b = [0 for i in date_list]
ipo = [0 for i in date_list]
for code in code_list:
    df = df1[df1['证券代码']==code]
    if df['type'].tolist()[0] == 'IPO':
        l = []
        ipo0 = []
        b0 = []
        for i in range(len(date_list)):
            date = date_list[i]
            try:
                ai = df['市值'][df['日期']==date].tolist()[0]
                l.append(ai)
            except:
                l.append(0)           
        for i in range(20):
            ipo0.append(l[i])
            b0.append(0)
        for i in range(20, len(date_list)):
            bi = min(l[i-20:i])
            b0.append(bi)
            ipo0.append(l[i]-bi)
        ipo = [i+j for i,j in zip(ipo, ipo0)]
        b = [i+j for i,j in zip(b, b0)]
    else:
        l = []
        a0 = []
        b0 = []
        for i in range(len(date_list)):
            date = date_list[i]
            try:
                ai = df['市值'][df['日期']==date].tolist()[0]
                l.append(ai)
            except:
                l.append(0)
        for i in range(20):
            a0.append(l[i])
            b0.append(0)
        for i in range(20, len(date_list)):
            bi = min(l[i-20:i])
            b0.append(bi)
            a0.append(l[i]-bi)
        a = [i+j for i,j in zip(a, a0)]
        b = [i+j for i,j in zip(b, b0)]
            
l1 = df1['市值'].tolist()
l2 = df1['市值比净值(%)'].tolist()
l3 = []
for i,j in zip(l1, l2):
    try:
        l3.append((i/j)*100)
    except:
        l3.append('i/j')
df1['净值'] = l3
df = df1.copy()
df = df[~df['净值'].isin(['i/j'])]
df = df.drop_duplicates(subset=['日期'], keep='first')

nav = df['净值'].tolist()
a = [(i/j)*100 for i,j in zip(a,nav)]
b = [(i/j)*100 for i,j in zip(b,nav)]
#一百倍大的ipo
ipo = [(i/j)*10000 for i,j in zip(ipo,nav)]
p_list = [a,b,ipo]
    
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

plt.figure(figsize=(25, 13))

date_list_p = []
for i in range(len(date_list)):
    if i/2 != i//2:
        date_list_p.append('')
    else:
        date_list_p.append(date_list[i])
plt.xticks(range(len(date_list)), date_list_p)
plt.xlim(0,len(date_list)-1)
plt.ylim(0, 100)

ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(10))

plt.grid(True)


color_list = ['red', 'orangered', 'chocolate',
              'orange', 'gold', 'yellow',
              'yellowgreen', 'palegreen', 'green',
              'springgreen','aqua','deepskyblue',
              'royalblue', 'blueviolet', 'violet',
              'hotpink', 'crimson']
x = list(range(len(date_list)))
print(x)
for i in range(3):
    plt.plot(p_list[i], color_list[i*3])    

