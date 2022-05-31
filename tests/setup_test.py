import requests

def test():
    url = 'https://www.cryptocompare.com/'
    response = requests.get(url)
    print(response)
    return


if __name__ == '__main__':
    test()
