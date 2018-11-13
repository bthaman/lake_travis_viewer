import lcra_gage_selenium as lcra
import pandas as pd
import numpy as np
import datetime
import os


def plot_travis_volume_since_1943(days_before_today=365):
    os.chdir(os.path.dirname(sys.argv[0]))
    # print(os.getcwd())
    df = pd.read_csv('Travis.08154500.1943-2018.csv', encoding='ISO-8859-1')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    # date1 = '1943-01-01'
    # date2 = '2050-01-05'
    # date2 = '2050-12-31'
    date2 = datetime.date(year=2050, month=12, day=31)
    # get the difference in days between today and the last day in the csv read above (1/5/2018)
    dt_today = datetime.date.today()
    dt_last = datetime.date(year=2018, month=5, day=23)
    num_days = dt_today - dt_last
    # read elevation since 1/22/2018 and append to df
    x, y, full, header, latest_vals = lcra.import_gage_data(site_num='3963', full_level=681.0)
    # make a df
    df_new = pd.DataFrame({'Date': x, 'Level_ft': y}).set_index('Date')
    # df = df.append(df_new, ignore_index=True)
    df = df.append(df_new, ignore_index=False)
    # remove duplicate index rows
    df = df[~df.index.duplicated(keep='last')]
    # remove blank rows
    df = df.dropna(axis=0)
    # overwrite the source csv with updated data
    df.to_csv('Travis.08154500.1943-2018.csv')
    df = df.reset_index()
    # filter by date
    #   get start date
    date1 = dt_today - datetime.timedelta(days=days_before_today)
    # print(str(date1) + ' to ' + str(dt_today))
    df = df[(df['Date'] >= pd.Timestamp(date1)) & (df['Date'] <= pd.Timestamp(date2))]
    # round to 2 decimals to match up with the stage-area-volume table
    df.Level_ft = df.Level_ft.round(2)
    x = df['Date'].values
    level_ft = df['Level_ft'].values
    header = 'Lake Travis (hydromet.lcra.org)'
    # read stage-storage
    df2 = pd.read_csv('stage.vol.travis.2dec.csv', encoding='ISO-8859-1')
    # chain together: merging the df's, setting the index to Date, and sorting by Date
    df3 = pd.merge(df, df2, left_on='Level_ft', right_on='ELEVATION').set_index('Date').sort_index()
    df3.to_csv('travis.csv', index=True)
    # pull out volume array and convert to % full
    pct_full = df3.VOL_ACFT.values / 1123478 * 100
    # make horizontal line at 100%
    pct100 = np.zeros(pct_full.shape[0]) + 100.0
    lcra.subplots(x, pct_full, header, 1, 1, latest_vals=None, full=pct100, show_axis_labels=True,
                  ylabel='Percent Full (%)')
    lcra.plot()

    level100 = np.zeros(level_ft.shape[0]) + 681.0
    lcra.subplots(x, level_ft, header, 1, 1, latest_vals=latest_vals, full=level100, show_axis_labels=True,
                  ylabel='Level (ft)')
    lcra.plot()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        plot_travis_volume_since_1943(days_before_today=int(float(sys.argv[1])))
    else:
        try:
            dt_today = datetime.date.today()
            dt_first = datetime.date(year=1943, month=2, day=1)
            max_days = (dt_today - dt_first).days
            str_max_days = '\nEnter number of days to plot (max={:,.0f}): '.format(max_days)
            numdays = int(float(input(str_max_days)))
            if numdays < 1:
                raise ValueError('You entered {}. Number must be positive.'.format(numdays))
            plot_travis_volume_since_1943(days_before_today=numdays)
        except Exception as e:
            print('\n' + str(e) + '\n')
            # using 'input' keeps the command window open so the user can view the error
            input('press enter to exit...')
