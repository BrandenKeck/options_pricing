# IMPORTS
import json, webbrowser, pyetrade, datetime, time
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


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
        driver = webdriver.Chrome()
        driver.get(auth_url)
        driver.implicitly_wait(1)
        driver.find_element(by=By.ID, value="user_orig").send_keys(keys['user'])
        driver.find_element(by=By.CSS_SELECTOR, value="input[type='password']").send_keys(keys['pwd'])
        driver.find_element(by=By.ID, value="logon_button").click()
        driver.implicitly_wait(1)
        driver.find_element(by=By.XPATH, value="//input[@value='Accept']").click()
        driver.implicitly_wait(1)
        vcode = driver.find_element(by=By.TAG_NAME, value="input").get_attribute('value')
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
        quotes = [tick['All']['ask'] for tick in self.market.get_quote(tickers,resp_format='json')['QuoteResponse']['QuoteData']]
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
                            expiry,
                            put_option['strikePrice']
                        )
                    )


# Class for options data objects
class kusanagi():

    def __init__(self, ticker, type, quote_price, opt_price, curr_date, exp_date, strike):

        # Define Underlying
        self.ticker = ticker
        self.quote_price = quote_price

        # Option Information
        self.opt_type = type
        self.opt_price = opt_price
        self.strike_price = strike
        self.curr_date = curr_date
        self.exp_date = exp_date
        delta = self.exp_date - self.curr_date
        self.dT = delta.days/365

        # Model Parameters
        self.theta = 0.2
        self.sigma = 1

    def simulate(self, timesteps):
        dt = self.dT / timesteps
        S = [self.quote_price]
        for tt in np.arange(timesteps):
            S_0 = S[len(S)-1]
            dS = self.theta*S_0*dt + self.sigma*np.sqrt(dt)*np.random.normal()
            S.append(S_0 + dS)
        return S

    def to_json(self):
        return {
            "ticker": self.ticker,
            "type": self.opt_type,
            "quote": self.quote_price,
            "price": self.opt_price,
            "strike": self.strike_price,
            "expiry": self.exp_date
        }

len(sus.models)
idx = 1200
sus = susanoo()
sus.get_options(["NVDA"])
sus.models[idx].to_json()
S = sus.models[idx].simulate(1000)
dT = sus.models[idx].dT
dT * 365

plt.plot(365 * dT * np.arange(len(S))/len(S), S)

ticker = "COIN"
dates = sus.market.get_option_expire_date(ticker)['OptionExpireDateResponse']['ExpirationDate']
date = dates[2]
yy = int(date['year'])
mm = int(date['month'])
dd = int(date['day'])
expiry = datetime.date(yy, mm, dd)

quote = sus.market.get_quote([ticker],resp_format='json')['QuoteResponse']['QuoteData']
quote[0]["All"]["bid"]
quote[0]["All"]["ask"]
quote[0]["All"]["totalVolume"]
quote[0]["All"]["pe"]
quote[0]["All"]["beta"]
quote[0]["All"]["marketCap"]

opts = sus.market.get_option_chains(ticker, expiry)['OptionChainResponse']['OptionPair'][50]["Call"]
opts["OptionGreeks"]
ask = opts["ask"]
bid = opts["bid"]
np.mean([float(x) for x in [ask, bid]])
