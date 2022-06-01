import yfinance as yf
import pandas as pd
from datetime import date


def get_fx(pair, daily_trading, export):
    """
    Paramters
    ---------
    pair : string
        currency pair instrument name e.g. GBPUSD=X.
    daily_trading : boolean
        False retains traditional 5 trading day weeks, True enforces
        cryptocurrencies 7 trading day weeks.
    export : boolean
        Export to csv (True), or not (False)

    Returns
    -------
    history : DataFrame
        Currency pair exchange rate as far back as possible
    """
    obj = yf.Ticker(pair)
    history = obj.history(period='max')['Close']

    if daily_trading:
        earliest = history.index[0].date()
        delta = (date.today() - earliest).days
        datelist = pd.date_range(end=date.today(), freq='D',
                                 periods=delta+1)
        dummy_list = [1]*len(datelist)
        zipper = pd.Series(dummy_list, index=datelist)
        history = pd.concat([zipper, history], axis=1).fillna(method='ffill')
        history.columns = ['dummy', f'{pair}']
        history.drop(columns=['dummy'], inplace=True)

    else:
        pass

    if export:
        history.to_csv(f'{pair}.csv')
    return history
