import urllib
import datetime

import matplotlib.pyplot as plt
import scipy.signal as spsig
import pandas as pd

def testcount_corrected(statelist=None):
    """Give plots for listed state(s) for total number of positives (by day) and PERCENT of positives (by day) 
    Shows how testing volume is influencing results (or not).
    
    Inputs:
        statelist  : list-like object giving states for which plots should be made
    """
    
    if statelist is None:
        # my own personal preferences for states I'm watching. :)
        statelist = ['florida', 'washington', 'texas', 'oklahoma', 'california', 'arizona']
        
    for state in statelist:

        try:
            with urllib.request.urlopen(f'https://covidtracking.com/data/state/{state.lower()}') as response:
               html = response.read()
        except urllib.error.HTTPError:
            continue #skip this "state" if it can't be read

        parsed = pd.read_html(html)

        data = parsed[1].copy()

        fmt = '%a %b %d %Y'

        data['Date'] = data['Date'].apply(lambda v: datetime.datetime.strptime(v, fmt))
        data = data.sort_values('Date')

        data['New Cases'] = data['Cases'].diff()
        data['New Cases (%)'] = data['New Cases']/data['New Tests']*100

        #NOTE: make days with >50% new positive cases MISSING - these are likely bolus data dumps from things like prisons.
        # This means our running average will be UNDER estimating positive cases for the windows where these days fall. 
        # This missing value will cause the entire ROW to be dropped (so for both raw counts and %)
        data.loc[data['New Cases (%)']>50, 'New Cases (%)'] = pd.np.nan

        data = data.set_index('Date')

        for ax,pltinfo in enumerate([
            ('New Cases (%)', plt.cm.tab10(0), '% Positve (Blue)'),
            ('New Cases', plt.cm.tab10(1), 'Total Count (Orange)'),
        ]):
            col,color,lbl = pltinfo
            if ax==1:
                plt.gca().twinx()  #second axes on right
            else:
                plt.grid(True, color=color)  #give grid for ONLY first set of data

            coldf = data.loc[datetime.datetime.strptime('2020-04-01','%Y-%m-%d'):, col].dropna()

            #main data
            plt.plot(coldf.index.values, coldf.values,'-', color=color)

            #Running average (actually a 1st order savgol with 7-point window)
            # NOTE: dropped days will be ignored in this smooth, so it's not really 7-days but 7 DATA POINTS
            coldf_sm = spsig.savgol_filter(coldf.values, 7, 1, 0)
            plt.plot(coldf.index.values, coldf_sm,'-', linewidth=6, color=color)

            plt.ylabel(lbl)
            plt.xticks(rotation=90)

        plt.title("{} (as of {})".format(state.capitalize(), datetime.datetime.now().strftime("%Y-%m-%d")))
        plt.xlabel(data.index.name)
        plt.show()