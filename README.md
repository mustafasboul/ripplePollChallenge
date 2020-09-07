### Ripple Poll Assignment

#### Prerequisites
1. **Python3+**<br>
   Download from https://www.python.org/
   
2. **gnuplot for chart graphs**<br>
   install on OSX using `brew install gnuplot` command in terminal
   
3. **Requests HTTP library**<br>
   Install using `python -m pip install requests`

#### Q1) How does your script work?
This is python script that connects periodically every `sleep_time` to target _rippled_ server defined in `server_url` .<br>
If new Ledger Sequence has been identified, it will be stored into data file `ledger_file_path`.<br>
At the same time, it collects the ledger closing time statistics and store the Total, Min, Max, and Average time consumed to close a ledger in `stats_file_path`.<br>
Chart can be generated after running the script by executing 'draw_char.p' file <br>`gnuplot -p draw_chart.p`

#### Q2) How did you decide on your polling interval?
Testing showed that ledgers are takes around 2-3 seconds to be generated mostly.
Choosing the minimum, 2 seconds, as sleeping interval was the most optimized to eliminate repetitive results on each loop.

#### Q3) What do the results tell you?
Mostly, ledgers get validated on average of 3 seconds.
In some small occasions, ledgers tend to take more time than the usual average to get validated

#### Q4) What might explain the variation in time between new ledgers?
The variation can be caused by multiple reasons:
- Similar ledger has been built that the supermajority agrees on, which means less time
- Agreement could not be reached between participating nodes due to not reaching supermajority agreement, which means more time
- Communication or Hardware Failures, which means more time
- Dishonest participants in the network, which means more time

#### Bonus 1
Check `calc_closing_stats()` function

#### Bonus 2
Using `ledger` or `server_state` method instead of `server_info` can provide `close_time` info for each ledger.
It will be more accurate to use `close_time` of the ledger instead of current time the poll request executed.