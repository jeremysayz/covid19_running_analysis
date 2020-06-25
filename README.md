# covid19_running_analysis

Frequently, people are claiming that the rise in raw COVID19 positive results is simply because we are testing more people. This code demonstrates the method to correct for the testing rate (by returning the PERCENT of tests run that were positive). If this relative rate goes up, it is NOT due to the number of tests. It may still be influenced by the cross-section of people being tested. For example, if a state starts testing less randomly and captures more symptomatic individuals or a higher-risk population like front-line workers, the measured rate will increase but not because the actual average across the entire population is going up. However, at the *state* level, such shifts would be diluted across the many different testing agencies. If a rate is increasing, it is likely due to a larger-scale population level drift.

For a Google Colab version of this tool, see [COVID19 State Trajectories](https://colab.research.google.com/drive/1xg70PshvTjZJRqFKLZWWTpybttnUPbvT)

Python code to:
* grab the latest COVID19 testing results from any state (from [covidtracking.com](http://covidtracking.com))
* calculate the % positive rate (i.e. correct for the NUMBER of tests done)
* calculate a running trend
* display a plot, for each state
