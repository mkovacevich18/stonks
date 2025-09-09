# What is Volatility Forecasting
As the name implies, our goal is to forecast the future volatility of certian equities. In doing so, we can trade options or hedge options based off volatility. Rather than having to predict the future price, we can theoretically profit based on the spread of the implied volatility (IV) and the realized volatility (and make bets based off the theoretical volatility) - which leads to delta hedging. 

## Delta Hedging
Mathematically, delta is represented as the partial derivative:
![delta equation](https://latex.codecogs.com/svg.latex?\Delta=\frac{\partial%20V}{\partial%20S})

of the option's fair value with respect to the spot price of the underlying security.

Delta is a function of the spot price \( S \), strike price, and time to expiry.
