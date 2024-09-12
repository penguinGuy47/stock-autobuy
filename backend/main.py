from services.chase import *
from services.fidelity import *
from services.firstrade import buy as firstrade_buy
from services.public import *
from services.robinhood import buy as robinhood_buy
from services.schwab import buy as schwab_buy
from services.tornado import *
from services.sofi import *
from services.tradier import *
from services.webull import *
from services.wellsfargo import *

def main():
    # ticker = input("Enter the ticker you would to purchase: ")
    ticker = 'APPL'
    chrome_path = r"C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data" # add the path to your chrome
    chrome_profile = r"Profile 5" # change this accordingly
    trade_share_count = '1'
    # buy_share_count = '1'
    # sell_share_count = input("How many shares would you like to sell? For all shares, type 'all', else enter an amount: ")

    # chase.buy(ticker)

    # tradier.buy(ticker)
    # fidelity.buy(ticker, chrome_path, chrome_profile)
    # fidelity.sell(ticker, chrome_path, chrome_profile)

    firstrade_buy(ticker, chrome_path, chrome_profile)

    # schwab_buy(ticker, chrome_path, chrome_profile)

    # sofi.buy(ticker, chrome_path, chrome_profile)

    # robinhood_buy(ticker, chrome_path, chrome_profile, trade_share_count)
    # robinhood.sell(ticker, chrome_path, chrome_profile, trade_share_count)


if __name__ == "__main__":
    main()
