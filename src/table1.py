import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 读取数据
stock = 'sh600000'
input_path = 'data/stock_data/sh600000.csv'
df_input = pd.read_csv(input_path, skiprows=1, encoding='GB18030')

stock_trade_record = pd.DataFrame(columns=['股票代码', '股票名称', '持有期限', '买入日期','卖出日期', '买入价格', '卖出价格',
                                           '收益率', '浮盈', '浮亏'])


# 数据初始化
peak_value = df_input['总市值'][0]
stock_holding = False  # 判断是否持有股票
return_rate = 1.0  # 收益率
max_return_rate = 1.0  # 浮盈
min_return_rate = 1.0  # 浮亏
win = 0  # 盈利次数
loss = 0  # 亏损次数
trade_times = 0  # 交易次数
holding_days = 5  # 持有期限

# 遍历数据，找到股票价值达到新高的时刻
for i in range(len(df_input)):
    if stock_holding == True:
        date = datetime.datetime.strptime(df_input['交易日期'][i], '%Y/%m/%d')
        # 单日涨跌幅
        change = (df_input['收盘价'][i]/df_input['前收盘价'][i]) - 1
        # 累计收率率
        return_rate *= (1 + change)
        # 最大浮盈
        if return_rate > max_return_rate:
            max_return_rate = return_rate
        # 最大浮亏
        if return_rate < min_return_rate:
            min_return_rate = return_rate

        # 判断股票的持有期限，此处为5天
        # 持有时间超过期限时，计算指标数据
        if (date - buy_date).days >= holding_days:
            stock_holding = False
            # 当股票涨停或跌停时，无法对股票进行操作
            if df_input['开盘价'][i] != df_input['最高价'][i] and \
                    df_input['最高价'][i] != df_input['最低价'][i] and \
                    df_input['开盘价'][i] != df_input['最低价'][i]:
                sell_date = datetime.datetime.strptime(df_input['交易日期'][i], '%Y/%m/%d')
                sell_value = df_input['开盘价'][i]
                if return_rate >= 1:
                    win += 1
                else:
                    loss += 1
                stock_trade_record.loc[trade_times] = [df_input['股票代码'][i], df_input['股票名称'][i], holding_days,
                                                       buy_date, sell_date, buy_value, sell_value, return_rate,
                                                       max_return_rate, min_return_rate]
                trade_times += 1
                return_rate = 1.0
                max_return_rate = 1.0
                min_return_rate = 1.0

    # 股票市值达到新高时，认为股票价值达到新高，买入股票并持有
    if df_input['总市值'][i] > peak_value and stock_holding == False:
        peak_value = df_input['总市值'][i]
        stock_holding = True
        buy_date = datetime.datetime.strptime(df_input['交易日期'][i], '%Y/%m/%d')
        buy_value = df_input['开盘价'][i]

print(stock_trade_record)