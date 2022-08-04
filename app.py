# IMPORTS
import json, webbrowser, pyetrade, datetime

# SUSANOO Model -
# Comparing Black Scholes Option Probabilities to Market Price
class susanoo():

    def __init__(self):

        # GET KEYS
        f = open('keys.json')
        keys = json.load(f)
        consumer_key = keys['key']
        consumer_secret = keys['secret']

        # HANDLE AUTHENTICATION
        oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
        auth_url = oauth.get_request_token()
        webbrowser.open(auth_url, new=2)
        vcode = input("Enter Verification Code: ")
        tokens = oauth.get_access_token(vcode)
        self.auth_mgr = pyetrade.authorization.ETradeAccessManager(
            consumer_key,
            consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret']
        )

        # ESTABLISH A MARKET
        self.market = pyetrade.ETradeMarket(
            consumer_key,
            consumer_secret,
            tokens['oauth_token'],
            tokens['oauth_token_secret'],
            dev=False
        )

        # MODEL STORAGE
        self.models = []

    # Function to get options data
    def get_options(self, tickers):

        # Dissect Data Objects
        quotes = [tick['All']['ask'] for tick in sus.market.get_quote(tickers,resp_format='json')['QuoteResponse']['QuoteData']]
        prices = dict(zip(tickers, quotes))
        for ticker in tickers:
            dates = self.market.get_option_expire_date(ticker)['OptionExpireDateResponse']['ExpirationDate']
            for date in dates:
                yy = int(date['year'])
                mm = int(date['month'])
                dd = int(date['day'])
                expiry = datetime.date(yy, mm, dd)
                options = sus.market.get_option_chains(ticker, expiry)['OptionChainResponse']['OptionPair']
                for option in options:

                    # Create an analysis object for call options
                    call_option = option["Call"]
                    self.models.append(
                        kusanagi(
                            ticker,
                            "call",
                            prices[ticker],
                            call_option['ask'],
                            datetime.date.today(),
                            expiry,
                            call_option['strikePrice']
                        )
                    )

                    # Create an analysis object for put options
                    put_option = option["Put"]
                    self.models.append(
                        kusanagi(
                            ticker,
                            "put",
                            prices[ticker],
                            put_option['ask'],
                            datetime.date.today(),
                            date,
                            put_option['strikePrice']
                        )
                    )


# Class for options data objects
class kusanagi():

    def __init__(self, ticker, type, quote_price, opt_price, curr_date, exp_date, strike):
        self.ticker = ticker
        self.type = type
        self.quote_price = quote_price
        self.opt_price = opt_price
        self.curr_date = curr_date
        self.exp_date = exp_date
        self.strike = strike

    def black_scholes(self):
        pass

    def to_json(self):
        return {
            "ticker": self.ticker,
            "type": self.type,
            "quote": self.quote_price,
            "price": self.opt_price,
            "strike": self.strike,
            "expiry": self.exp_date
        }

sus = susanoo()
sus.get_options(["NFLX", "AAPL", "NVDA"])
sus.models[5].to_json()
