import requests
import pandas as pd
import datetime as dt


def ohlcv(
        fsym=None, tsym='USD', start_date='2018-01-01', e=None, convert=False,
        export=False
        ):
    """
    Parameters:
        fsym: Cryptocurrency
        tsym: Conversion to
        start_date: string of earliest date required 'yyyy-mm-dd'
        e: Optionally specify exchange

    Returns: OHLCV DataFrame Object
    """

    start = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    limit = (dt.date.today() - start).days

    market_url = (
         f'https://min-api.cryptocompare.com/data/v2/histoday?'
         f'fsym={fsym}&tsym={tsym}&limit={limit}'
         )
    if e:
        market_url = market_url + f'&e={e}'
    else:
        pass

    if convert is True:
        market_url = market_url + '&tryConversion=true'
    else:
        market_url = market_url + '&tryConversion=false'
    print(fsym)
    market_df = pd.DataFrame(requests.get(market_url).json()['Data']['Data'])
    market_df = market_df.rename(columns={'time': 'Date'})
    market_df['Date'] = pd.to_datetime(market_df['Date'], unit='s')
    market_df.set_index(market_df['Date'], inplace=True)
    market_df.drop(columns=['conversionType', 'conversionSymbol'],
                   inplace=True)
    market_df = market_df[market_df.columns[[3, 1, 2, 6, 4, 5]]]
    market_df.columns = market_df.columns.str.upper()

    if export is True:
        market_df.to_csv(f'{fsym}_{tsym}_ohlcv.csv')
    else:
        pass

    return market_df


def looper(fsym_list):
    """
    Parameters
    ----------
    fsym_list : list
        List of all crypto-symbols.

    Returns
    -------
    aggregate : DataFrame
        Close prices of all fsyms.
    """
    aggregate = pd.DataFrame()
    for f in fsym_list:
        # This could be made more dynamic
        try:
            data = ohlcv(fsym=f, tsym='USD', start_date='2021-01-01', e=None,
                         convert=False, export=False)
            data.rename(columns={'CLOSE': f}, inplace=True)
            aggregate = pd.concat([aggregate, pd.DataFrame(data[f])], axis=1)
        except KeyError as e:
            print(e)
            print('No data for', f)
    return aggregate


def kline_resampler(ohlcv, pd_dot_resample):
    """
    Parameters
    ----------
    ohlcv : DataFrame
    pd_dot_resample_rule : str
        Pandas resample rule arg W, M, 3T etc.

    Returns
    -------
    kline : DataFrame
        Resampled OHLCV DataFrame.
    """
    kline = pd.DataFrame()
    kline['OPEN'] = ohlcv['OPEN'].resample(pd_dot_resample).first()
    kline['HIGH'] = ohlcv['HIGH'].resample(pd_dot_resample).max()
    kline['LOW'] = ohlcv['LOW'].resample(pd_dot_resample).min()
    kline['CLOSE'] = ohlcv['CLOSE'].resample(pd_dot_resample).last()
    kline['VOL_FSYM'] = ohlcv['VOLUMEFROM'].resample(pd_dot_resample).sum()
    kline['VOL_TSYM'] = ohlcv['VOLUMETO'].resample(pd_dot_resample).sum()

    return kline
