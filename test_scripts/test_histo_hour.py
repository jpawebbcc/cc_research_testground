import datetime as dt
import requests
from test_api_key import api


def histo_hour(fsym, tsym, start_date, export):

    start = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    limit = (dt.date.today() - start).days * 24

    url = (
        f'https://min-api.cryptocompare.com/data/v2/histohour?fsym={fsym}' +
        f'&tsym={tsym}&limit={limit}&api_key={api}'
        )

    data = requests.get(url).json()['Data']['Data']
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)

    if export is True:
        df.to_csv(f'hist_hour_{fsym}_ohlcv.csv')
    else:
        pass

    return df
