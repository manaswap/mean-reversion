# mean-reversion

Mean Reversion is a trading strategy where you look at a weeks performance for a stock, then you determine if its going in an upwards trend or a downwards trend. If its going down, we predict that it will return to the mean the next week, going in a positive direction, and vice versa. The way I have calculated a positive and negative trend is by using pythons linear algebra library, and quantopians open source api which provides daily stock movement. 
