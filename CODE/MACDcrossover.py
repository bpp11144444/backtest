import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
# 运行前先调整r adj instrument df参数 | adjust params(r,adj,instrument,df) before running

# 无风险利率 set risk free rate
r=0.04
# 持有策略填写'Close' MACD策略填写'total' set holding stratagy as 'Close' or MACD strategy as 'total'
adj = 'Close'
# Company Name
instrument="pingan"
# Csv file
df = pd.read_csv('E:\\backtest\\csv\\'+instrument+'csv.csv')
# MACD params
fastperiod=12
slowperiod=26
signalperiod=9
##line 93 调整存储图片路径 Change the root of saving image
#========================================================================================
# Get MACD from Talib
df['macd'],df['macdsig'],df['macdhist']=ta.MACD(np.asarray(df.Close),fastperiod, slowperiod, signalperiod)
start_amount=1000000
df['amount']=start_amount
df['shares']=0
df['total']=0
df.ix[0,'total']=start_amount
# drop NaN
df.dropna()
# initial trading times
trade_time = 0

for i in range(1, len(df)):
        df.ix[i, 'shares']=df.ix[i-1,'shares']
        df.ix[i, 'amount']=df.ix[i-1,'amount']
        df.ix[i, 'total']=df.ix[i, 'shares']*df.ix[i,'Close']+df.ix[i,'amount']
        if df.ix[i,'shares'] == 0 and df.ix[i,'macdsig'] < df.ix[i,'macd']:
            df.ix[i,'shares'] = df.ix[i,'amount']/df.ix[i,'Close']
            df.ix[i,'amount'] = df.ix[i,'amount']-df.ix[i,'shares']*df.ix[i,'Close']
            trade_time+=1
        elif df.ix[i,'shares'] > 0 and df.ix[i,'macdsig'] >= df.ix[i,'macd']:
            df.ix[i, 'amount']=df.ix[i,'shares']*df.ix[i,'Close']
            df.ix[i,'shares']=0
            trade_time += 1
        else:
            continue

# date
x=df.Date
# macd DIF line
y=df.macd
# macd signal line
z=df.macdsig
# total portfolio worth
total=df.total
# Close price
close=df.Close
# plot three pic
fig = plt.figure(num=3, figsize=(15, 8),dpi=80)

ax1 = fig.add_subplot(3,1,2)
ax2 = fig.add_subplot(3,1,3)
ax3 = fig.add_subplot(3,1,1)

# choose each pic and set x range
plt.sca(ax1)
plt.xticks(np.arange(0, 1080, step=60), rotation=13)
plt.sca(ax2)
plt.xticks(np.arange(0, 1080, step=60), rotation=13)
plt.sca(ax3)
plt.xticks(np.arange(0, 1080, step=60), rotation=13)

# plot first pic

ax1.plot(x,y,color='g',label='DIF')
ax1.plot(x,z,color='b',label='DEA')
ax1.legend()

# plot second pic

ax2.plot(x,total,label='portfolio')
ax2.legend()

# plot third pic

ax3.plot(x,close,label='Stock Price')
ax3.legend()

# plot title

plt.title(instrument)
# 保存图片，修改instrument前面项为你想要存储的根目录| Save image. Change the root before +instrument
plt.savefig('E:\\backtest\\csv\\'+instrument+'_'+'MACD('+str(fastperiod)+','+str(slowperiod)+','+str(signalperiod)+').png')
plt.show()



data = df


# 每日收益率 get daily return
data['return']=(data[adj].shift(-1)-data[adj])/data[adj]

# 每日超额收益率 get extra return
data['exReturn']=data['return']-r/252

# 获得夏普比率get sharpe ratio 15.8745=sqrt(252)
sharperatio=15.8745*data['exReturn'].mean()/data['exReturn'].std()
print('该策略的夏普率为： ', sharperatio)
print('sharpe ratio： ', sharperatio)
data[adj].plot()

# 计算累积收益率 calculate Cumulative return cumret=(1+return).cumsum
data['cumret']=np.cumprod(1+data['exReturn'])-1

# initial
Max_cumret = np.zeros(len(data))
retracement = np.zeros(len(data))
Re_date=np.zeros(len(data))
Re_date2=np.zeros(len(data))

# 计算累积最大收益率 calculate max return rate
# 计算最最大回撤幅度 calculate max retracement rate
for i in range(len(data)):
    if i==0:
        Max_cumret[0] = data['cumret'][0]
        retracement[0] = (1 + Max_cumret[0]) / (1 + data['cumret'][0]) - 1
    else:
        Max_cumret[i] = max(Max_cumret[i - 1], data['cumret'][i])
        retracement[i] = float(abs((1 +data['cumret'][i] ) / (1 + Max_cumret[i]) - 1))
    if retracement[i]==0:
        Re_date[i] = 0
    else:
        Re_date[i] = Re_date[i - 1] + 1


for i in range (len(data)):
    if i ==0:
        max = data[adj][0]
        Re_date2[0] = 0
    elif data[adj][i]>max:
        Re_date2[i] = 0
        max = data[adj][i]
    elif data[adj][i] <= max:
        Re_date2[i] = Re_date2[i-1] +1




retracement = np.nan_to_num(retracement)
Max_re = retracement.max()
# 计算最大回撤时间
Max_reDate=Re_date.max()
print('该策略的最大回撤为:', Max_re)
print('The largest drawdown:', Max_re)

##print('该策略的最大回撤时间为:', Max_reDate)
##print('The deepest drawdown duration:', Max_reDate)

print('该策略的最长回撤时间为:', Re_date2.max())
print('The largest drawdown time duration:', Re_date2.max())

if adj == 'total':
    print('该策略的总交易次数为:', trade_time)
    print('Total trading times:', trade_time)
elif adj == 'Close':
    print('该策略的总交易次数为:', 1)
    print('Total trading times:', 1)

print('最终净值:',data.ix[len(data)-1,adj]/data.ix[0,adj])
print('Total Net Value:',data.ix[len(data)-1,adj]/data.ix[0,adj])


# 存储到csv | Save to csv
#data.to_csv(r'C:\Users\MSI-PC\Desktop\bloomberg\csv\MACDapple.csv')

