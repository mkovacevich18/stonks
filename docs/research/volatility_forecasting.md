# What is Volatility Forecasting
As the name implies, our goal is to forecast the future volatility of certian equities. In doing so, we can trade options or hedge options based off volatility. Rather than having to predict the future price, we can theoretically profit based on the spread of the implied volatility (IV) and the realized volatility (and make bets based off the theoretical volatility) - which leads to delta hedging. 

## Delta Hedging
Mathematically, delta is represented as the partial derivative:

$$
\Delta = \frac{\partial V}{\partial S}, \quad \Delta \in [-1, 1]
$$

of the option's fair value with respect to the spot price of the underlying security. This shows that $\Delta$ is a function of the spot price $S$, strike price, and time to expiry. $\Delta$ is really measuring the rate of change of an option's value as the stock moves up or down in price. Note that by delta hedging, we are keeping as close to delta-neutral as we can. 
