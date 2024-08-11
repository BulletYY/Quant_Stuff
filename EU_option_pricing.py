import QuantLib
print(dir(QuantLib))

import QuantLib as ql

option_type = ql.Option.Call
underlying_price = 100
strike_price = 100
expiry_date = ql.Date(31, 12, 2024)
volatility = 0.2
risk_free_rate = 0.05

option = ql.EuropeanOption(ql.PlainVanillaPayoff(option_type, strike_price),
                           ql.EuropeanExercise(expiry_date))

spot_handle = ql.QuoteHandle(ql.SimpleQuote(underlying_price))
flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(expiry_date, risk_free_rate, ql.Actual360()))
flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(expiry_date, ql.NullCalendar(), volatility, ql.Actual360()))
bs_process = ql.BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)

engine = ql.AnalyticEuropeanEngine(bs_process)
option.setPricingEngine(engine)

option_price = option.NPV()
print("Option Price:", option_price)
