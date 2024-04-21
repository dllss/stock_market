import numpy as np
import pandas as pd


class Account:

    def __init__(self,
                 money_init,
                 start_date='',
                 end_date='',
                 stop_loss_rate=-0.03,
                 stop_profit_rate=0.05,
                 max_hold_period=5):
        self.cash = money_init  # 现金
        self.stock_value = 0  # 股票价值
        self.market_value = money_init  # 总市值
        self.stock_name = []  # 记录持仓股票名字
        self.stock_id = []  # 记录持仓股票id
        self.buy_date = []  # 记录持仓股票买入日期
        self.stock_num = []  # 记录持股股票剩余持股数量
        self.stock_price = []  # 记录股票的买入价格
        self.start_date = start_date
        self.end_date = end_date
        self.stock_asset = []  # 持仓数量
        self.buy_rate = 0.0003  # 买入费率
        self.buy_min = 5  # 最小买入费率
        self.sell_rate = 0.0003  # 卖出费率
        self.sell_min = 5  # 最大买入费率
        self.stamp_duty = 0.001  # 印花税
        # self.info = []  # 记录所有买入卖出记录
        self.max_hold_period = max_hold_period  # 最大持股周期
        self.hold_day = []  # 股票持股时间

        self.cost = []  # 记录真实花费
        # self.profit = []  # 记录每次卖出股票收益

        self.stop_loss_rate = stop_loss_rate  # 止损比例
        self.stop_profit_rate = stop_profit_rate  # 止盈比例

        self.victory = 0  # 记录交易胜利次数
        self.defeat = 0  # 记录失败次数

        self.cash_all = [money_init]  # 记录每天收盘后所持现金
        self.stock_value_all = [0.0]  # 记录每天收盘后所持股票的市值
        self.market_value_all = [money_init]  # 记录每天收盘后的总市值
        self.max_market_value = money_init  # 记录最大的市值情况，用来计算回撤
        self.min_after_max_market_value = money_init  # 记录最大市值后的最小市值
        self.max_retracement = 0  #记录最大回撤率
        self.info = pd.DataFrame(
            columns=['ts_code', 'name', 'buy_price', 'buy_date', 'buy_num', 'sell_price', 'sell_date', 'profit'])

    # 股票买入
    def buy_stock(self, stock_id, stock_name, buy_date, stock_price, buy_num):
        """
        :param stock_id: 买入股票的id
        :param stock_name: 买入股票的名字
        :param buy_date: 买入日期
        :param stock_price: 买入股票的价格
        :param buy_num: 买入股票的数量
        :return:
        """
        if stock_id in self.stock_id:
            return
        self.stock_id.append(stock_id)
        self.stock_name.append(stock_name)
        self.buy_date.append(buy_date)
        self.stock_price.append(stock_price)
        self.hold_day.append(1)
        tmp_len = len(self.info)
        if stock_id not in self.stock_id:
            self.stock_id.append(stock_id)
            self.stock_name.append(stock_name)
            self.buy_date.append(buy_date)
            self.stock_price.append(stock_price)
            self.hold_day.append(1)

            self.info.loc[tmp_len, 'ts_code'] = stock_id
            self.info.loc[tmp_len, 'name'] = stock_name
            self.info.loc[tmp_len, 'buy_price'] = stock_price
            self.info.loc[tmp_len, 'buy_date'] = buy_date

            if str(buy_date) == '20190813':
                print('go')
            # 更新市值、现金及股票价值
            tmp_money = stock_price * buy_num
            service_change = tmp_money * self.buy_rate
            if service_change < self.buy_min:
                service_change = self.buy_min
            cash_change = tmp_money + service_change
            if cash_change > self.cash:
                buy_num = buy_num - 100
                tmp_money = stock_price * buy_num
                service_change = tmp_money * self.buy_rate
                if service_change < self.buy_min:
                    service_change = self.buy_min
                cash_change = tmp_money - service_change
            self.cash = self.cash - cash_change
            self.info.loc[tmp_len, 'buy_num'] = buy_num
            self.stock_num.append(buy_num)

        # self.info.append(info)

    def sell_stock(self, sell_date, stock_name, stock_id, sell_price, sell_num, flag):
        """
        :param sell_date: 卖出日期
        :param stock_name: 卖出股票的名字
        :param stock_id: 卖出股票的id
        :param sell_price: 卖出股票的价格
        :param sell_num: 卖出股票的数量
        :return:
        """

        if stock_id not in self.stock_id:
            raise TypeError('该股票未买入')
        # 首先找到需要卖出的股票在持仓股票中的索引
        idx = self.stock_id.index(stock_id)
        # 然后更新现金：（需要计算印花税、卖出费率等）
        tmp_money = sell_num * sell_price
        service_change = tmp_money * self.sell_rate
        if service_change < self.sell_min:
            service_change = self.sell_min
        stamp_duty = self.stamp_duty * tmp_money
        self.cash = self.cash + tmp_money - service_change - stamp_duty

        # self.stock_value = self.stock_value - tmp_money
        # self.market_value = self.cash + self.stock_value

        service_change = stamp_duty + service_change
        # self.profit.append(tmp_money-service_change)
        profit = tmp_money - service_change - self.cost[idx]
        # 更新其他一些信息
        if self.stock_num[idx] == sell_num:
            # 全部卖出
            del self.stock_num[idx]
            del self.stock_id[idx]
            del self.stock_name[idx]
            del self.buy_date[idx]
            del self.stock_price[idx]
            del self.hold_day[idx]
            del self.cost[idx]
        else:
            self.stock_num[idx] = self.stock_num[idx] - sell_num
            # 还需要补充profit的计算先放着
            pass

        if flag == 0:
            info = str(sell_date) + '  到期卖出' + stock_name + ' (' + stock_id + ') ' \
                   + str(int(sell_num)) + '股，股价：'+str(sell_price) + ',收入：' + str(round(tmp_money,2)) + ',手续费：' \
                   + str(round(service_change, 2)) + '，剩余现金：' + str(round(self.cash, 2))
            if profit > 0:
                info = info + '，最终盈利：' + str(round(profit, 2))
                self.victory += 1
            else:
                info = info + '，最终亏损：' + str(round(profit, 2))
                self.defeat += 1
        elif flag == 1:
            info = str(sell_date) + '  止盈卖出' + stock_name + ' (' + stock_id + ') ' \
                   + str(int(sell_num)) + '股，股价：' + str(sell_price) + ',收入：' + str(round(tmp_money, 2)) + ',手续费：' \
                   + str(round(service_change, 2)) + '，剩余现金：' + str(round(self.cash, 2)) \
                   + '，最终盈利：' + str(round(profit, 2))
            self.victory += 1
        elif flag == 2:
            info = str(sell_date) + '  止损卖出' + stock_name + ' (' + stock_id + ') ' \
                   + str(int(sell_num)) + '股，股价：' + str(sell_price) + ',收入：' + str(round(tmp_money, 2)) + ',手续费：' \
                   + str(round(service_change, 2)) + '，剩余现金：' + str(round(self.cash, 2)) \
                   + '，最终亏损：' + str(round(profit, 2))
            self.defeat += 1

        print(info)
        idx = (self.info['ts_code'] == stock_id) & self.info['sell_date'].isna()
        self.info.loc[idx, 'sell_date'] = sell_date
        self.info.loc[idx, 'sell_price'] = sell_price
        self.info.loc[idx, 'profit'] = profit

    # 买入触发时间，后期可以补
    def buy_trigger(self):
        pass

    # 卖出触发器：判断是否达到卖出条件
    def sell_trigger(self, stock_id, day, all_df, index_df):
        """
        :param stock_id: 股票id
        :param day: 回测时间
        :param all_df: 所有数据的DataFrame
        :param index_df: 指数的DataFram
        :return: 第一个返回是否卖出，第二个返回卖出类型，第三个返回
                  卖出价格；若不卖出，后面两个值无意义
        """
        # print(day, stock_id)
        # 首先根据日期和股票id定位到特定的股票当天一些信息
        # 可能会有一些停牌企业，后期再改
        idx = (all_df['trade_date'] == day) & (all_df['ts_code'] == stock_id)
        # print(all_df[idx]['low'])
        try:
            low = all_df[idx]['low'].values[0]
            high = all_df[idx]['high'].values[0]
            open = all_df[idx]['open'].values[0]
            close = all_df[idx]['close'].values[0]
            # 找到该股在持仓股票的id
            idx = self.stock_id.index(stock_id)
            # 判断开盘价是否到止盈或止损点
            tmp_rate = (open - self.stock_price[idx]) / self.stock_price[idx]
            if tmp_rate <= self.stop_loss_rate:  # 止损卖出，开盘价卖出
                return True, 2, open
            elif tmp_rate >= self.stop_profit_rate:  # 止盈卖出，开盘价卖出
                return True, 1, open
            # 如果没有，则先判断当日最低是否到止损点，再判断当日最高是否到止盈点（这里优先考虑差的情况，实际可能先到止盈点再到止损点）。
            # 这里有点bug，先判断最低吧，优先出现最差的可能
            tmp_rate = (low - self.stock_price[idx]) / self.stock_price[idx]
            if tmp_rate <= self.stop_loss_rate:  # 止损卖出，止损价卖出
                # 假设都止损价不能马上卖出，多损失 0.01%
                sell_price = self.stock_price[idx] * (1 + self.stop_loss_rate - 0.01)
                return True, 2, sell_price

            tmp_rate = (high - self.stock_price[idx]) / self.stock_price[idx]
            if tmp_rate >= self.stop_profit_rate:  # 止盈卖出，止盈价卖出
                sell_price = self.stock_price[idx] * (1 + self.stop_profit_rate)
                return True, 1, sell_price

            # 判断持股周期是否达到上限（这里我们追求短线炒股，所以最大持股时间设置为5天）
            hold_day = self.hold_day[idx]
            if hold_day >= self.max_hold_period:  # 收盘价卖出
                return True, 0, close

            return False, 3, 0
        except Exception:
            print('sell_trigger Exception: ', Exception)
            return False, 3, 0
    # 更新信息
    # 需要一个更新当日股票的市值及总市值的一个操作
    def update(self, day, all_df):
        # 得到持仓股票的收盘价
        stock_price = []
        for j in range(len(self.stock_id)):
            self.hold_day[j] = self.hold_day[j] + 1  # 更新持股时间
            idx = (all_df['trade_date'] == day) & (all_df['ts_code'] == self.stock_id[j])
            close = all_df.loc[idx]['close'].values[0]
            stock_price.append(close)
        # 更新市值等信息
        # print(stock_price)
        stock_price = np.array(stock_price)
        stock_num = np.array(self.stock_num)
        self.stock_value = np.sum(stock_num * stock_price)
        self.market_value = self.cash + self.stock_value
        self.market_value_all.append(self.market_value)
        self.stock_value_all.append(self.stock_value)
        self.cash_all.append(self.cash)

        # 更新最大回撤等信息
        if self.max_market_value < self.market_value:
            self.max_market_value = self.market_value
            self.min_after_max_market_value = 99999999999
        elif self.min_after_max_market_value > self.market_value:
            self.min_after_max_market_value = self.market_value
            #  计算回撤率
            retracement = np.abs((self.max_market_value - self.min_after_max_market_value) / self.max_market_value)
            if retracement > self.max_retracement:
                self.max_retracement = retracement
        info = '结算日: ' + str(day) + ' 总市值: ' + str(self.market_value)
        print(info)
    # 回测系统：
    # 就是输入每日可买入的股票（这些股票是经过模型筛选得到的），然后回测系统根据一些条件买入卖出等操作。
    def BackTest(self, buy_df, all_df, index_df, buy_price='close'):
        """
        :param buy_df: buy_df为我们模型筛选后每日可买入的股票，输入为DataFrame
        :param all_df: 所有股票的DataFrame
        :param index_df: 指数对应时间的df
        :return:
        """
        # 先按时间顺序排列，然后遍历选择股票
        day_info = np.sort(index_df['trade_date'])
        for i in range(len(day_info)):
            # 买股票，这里我们假设对于每支股票，我们利用当前总市值的20%的现金去购买，如果现金小于5000就不买了。
            day = day_info[i]
            tmp_idx = buy_df['trade_date'] == day
            tmp_df = buy_df.loc[tmp_idx].reset_index()
            # tmp_df = buy_df.loc[tmp_idx].sort_values('label_prob', ascending=False).reset_index()

            # 然后判断持仓股票是否达到卖出要求，若达到则卖出，否则继续持有
            # 先买后卖吧
            # ----买股
            if len(tmp_df) != 0:
                for j in range(len(tmp_df)):
                    money = self.market_value * 0.2
                    if money > self.cash:
                        money = self.cash
                    if money < 5000:  # 假设小于5000RMB，就不买股票
                        break
                    # print(1)
                    # print(tmp_df)
                    # print(tmp_df['close'])

                    # // 是一个运算符，表示整数除法（也称为地板除法）。这意味着当你使用 // 进行除法运算时，结果会是一个整数，小数部分会被丢弃，并且结果总是向负无穷大方向舍入。
                    # 两层的价格除以金额再转换成100股 => 1手
                    buy_num = (money / tmp_df[buy_price][j]) // 100
                    if buy_num == 0:
                        # 如果买的手数是0
                        continue
                    buy_num = buy_num * 100
                    self.buy_stock(tmp_df['ts_code'][j], tmp_df['name'][j], day, tmp_df[buy_price][j], buy_num)

            # ----卖股
            # import datetime
            # start = datetime.datetime.now()
            for j in range(len(self.stock_id) - 1, -1, -1):
                if self.buy_date[j] == day:
                    continue
                stock_id = self.stock_id[j]
                stock_name = self.stock_name[j]
                sell_num = self.stock_num[j]  # 假设全卖出去

                is_sell, sell_kind, sell_price = self.sell_trigger(stock_id, day, all_df, index_df)
                if is_sell:
                    self.sell_stock(day, stock_name, stock_id, sell_price, sell_num, sell_kind)

            # 更新持股周期及信息
            try:
                self.update(day, all_df)
            except Exception:
                print('BackTest error', Exception)
                pass
            # end = datetime.datetime.now()
            # print('running time:%s'%(end-start))

        # self.info['buy_date'] = self.info['buy_date'].apply(lambda x: int(x))
        # self.info['sell_date'] = self.info['sell_date'].apply(lambda x: int(x))
        # self.info['buy_num'] = self.info['buy_num'].apply(lambda x: int(x))
        try:
            self.info[['buy_date', 'sell_date', 'buy_num']] = self.info[['buy_date', 'sell_date',
                                                                         'buy_num']].astype(int)
        except Exception:
            pass
