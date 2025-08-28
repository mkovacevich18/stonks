# Data Preprocessing
This page refers to how we preprocess and source our data. 

**Data Source:** `Polygon.io` ([Polygon Website](https://polygon.io/))

The ETL pipeline is currently set up to read in an API_KEY from `Polygon.io` - this API_KEY should be unique to each user of this repo. Polygon has data pertaining to options, futures, Forex, etc. The we are able to access if a function of which tier we are willing to pay for. For historical ticker data, we just use the free option. For stock options, we use the `option starter` plan.

So far, the goal is relavitely simple in how we load and clean data. We get options contracts that are set to expire within a range of days from today's current data (by defauly the range is 20 - 120 days from now). We filter out options contracts that have NULL values and no valid greeks.
* We could make a cleaner dataset by placing filters on the option's open interest, etc (further eda is needed here).
* The notebook `options.ipynb` contains brief showings of what the filtered contracts dataframe looks like as well
### Options Data Fields:

- cfi  
- contract_type  
- exercise_style  
- expiration_date  
- primary_exchange  
- shares_per_contract  
- strike_price  
- ticker  
- underlying_ticker  
- greeks.details.contract_type  
- greeks.details.exercise_style  
- greeks.details.expiration_date  
- greeks.details.shares_per_contract  
- greeks.details.strike_price  
- greeks.details.ticker  
- greeks.greeks.delta  
- greeks.greeks.gamma  
- greeks.greeks.theta  
- greeks.greeks.vega  
- greeks.implied_volatility  
- greeks.open_interest  
- greeks.underlying_asset.ticker  
- greeks.day.change  
- greeks.day.change_percent  
- greeks.day.close  
- greeks.day.high  
- greeks.day.last_updated  
- greeks.day.low  
- greeks.day.open  
- greeks.day.previous_close  
- greeks.day.volume  
- greeks.day.vwap  

Analyzing the same ticker, we pull in 2 years of historical data and look at the chart. This data is a lot more limited since it is "free" but nonetheless, it provides a good starting point.

### Historical Data Fields
- volume
- vw
- open
- close
- high
- low
- timestamp
- n (number of trades)

There are additional types of data that we could look into - maybe Futures such a `VIX` or maybe other data vendors. We also need to figure out the gaps in Polygon's data and how what data we could use to fill these gaps.





