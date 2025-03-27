
import backtrader as bt
import datetime
import yfinance as yf

class SRCStrategy(bt.Strategy):
    params = dict(
        dip_pct=0.05,
        rsi_thresh=40,
        gain_target=0.10,
        loss_limit=0.05,
        max_days=30
    )

    def __init__(self):
        self.order = None
        self.entry_price = None
        self.bar_executed = None
        self.high = bt.ind.Highest(self.data.close(-1), period=60)
        delta = self.data.close - self.data.close(-1)
        gain = bt.If(delta > 0, delta, 0.0)
        loss = bt.If(delta < 0, -delta, 0.0)
        avg_gain = bt.indicators.SimpleMovingAverage(gain, period=14)
        avg_loss = bt.indicators.SimpleMovingAverage(loss, period=14)
        rs = avg_gain / avg_loss
        self.rsi = 100 - (100 / (1 + rs))

    def next(self):
        if self.order:
            return

        if not self.position:
            dip = (self.high[0] - self.data.close[0]) / self.high[0]
            if dip >= self.p.dip_pct and self.rsi[0] < self.p.rsi_thresh:
                self.entry_price = self.data.close[0]
                self.bar_executed = len(self)
                self.order = self.buy()
        else:
            price = self.data.close[0]
            if price >= self.entry_price * (1 + self.p.gain_target) or                price <= self.entry_price * (1 - self.p.loss_limit) or                len(self) - self.bar_executed >= self.p.max_days:
                self.order = self.sell()

def run_src_strategy(params):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SRCStrategy,
                        dip_pct=params.get("dip_pct", 0.05),
                        rsi_thresh=params.get("rsi_thresh", 40),
                        gain_target=params.get("gain_target", 0.10),
                        loss_limit=params.get("loss_limit", 0.05),
                        max_days=params.get("max_days", 30))

    data = yf.download(params["ticker"], start=params["start"], end=params["end"])
    data_bt = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_bt)
    cerebro.broker.setcash(1000.0)
    cerebro.run()
    return {"final_value": cerebro.broker.getvalue()}
