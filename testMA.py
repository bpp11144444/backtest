from pyalgotrade import plotter
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
import sma_crossover
# 运行前先调整 r instrument feed | adjust params(r,instrument,feed) before running
# 无风险利率 risk free rate
r = 0.04

# Load the bar feed from the CSV file
instrument="google"
feed = quandlfeed.Feed()
# 调整需要的CSV路径 Adjust CSV file
feed.addBarsFromCSV(instrument, 'E:\\backtest\\csv\\'+instrument+'csv.csv')

# 修改长短期均线 Adjust fast and slow MA
fastMA=5
slowMA=20
##line 55 调整存储图片路径 Change the root of saving image
#========================================================================================
# Evaluate the strategy with the feed's bars.
myStrategy = sma_crossover.SMACrossOver(feed, instrument, fastMA,slowMA)

# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
sharpeRatioAnalyzer = sharpe.SharpeRatio()
drawdown=drawdown.DrawDown()
trades=trades.Trades()
myStrategy.attachAnalyzer(returnsAnalyzer)
myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
myStrategy.attachAnalyzer(drawdown)
myStrategy.attachAnalyzer(trades)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
plt.getInstrumentSubplot(instrument).addDataSeries("fastSMA", myStrategy.getshortSMA())
plt.getInstrumentSubplot(instrument).addDataSeries("slowSMA", myStrategy.getlongSMA())
# Plot the simple returns on each bar.
# plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())


# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
myStrategy.info("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(r))
myStrategy.info("Max drawdown: %.2f" % drawdown.getMaxDrawDown())
myStrategy.info(drawdown.getLongestDrawDownDuration())
myStrategy.info("Total trading times: %.2f" % trades.getCount())

# Plot the strategy.
plt.plot()
# 保存图片，修改instrument前面项为你想要存储的根目录| Save image. Change the root before +instrument
plt.savePlot('E:\\backtest\\csv\\'+instrument+'_'+'MA('+str(fastMA)+','+str(slowMA)+')'+'.png',200)
