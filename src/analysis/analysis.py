'''
TODO:
    - add something that prints out warnings for missing data
    - make dataframe for LuCiD scale factors
'''

import glob
import json
import yaml
import numpy as np
import pandas as pd


fnames = sorted(glob.glob('data/morning/*.txt'))


df_list = []

for fn in fnames:
    # read into dataframe
    df = pd.read_json(fn,orient='index')
    # reset the index to a multiindex
    entry_tstamp = [glob.os.path.basename(fn).split('.')[0]]
    drm_indices = df.index.values.astype(str)
    df.index = pd.MultiIndex.from_product([entry_tstamp,drm_indices],names=['entry_tstamp','drm'])
    # add to cumulative list
    df_list.append(df)

# stack entries
df = pd.concat(df_list).reset_index(level='entry_tstamp')

# the drm labels with 0 are initial entry form stuff,
# and the A's are appendments
# so drop them for dream analysis stuff
df_drms = df.drop(labels=['A1','A2']).reset_index()
## TODO: make sure that all other values of drm==0 are NaNs,
##      so that they don't affect analysis on other drms
##      - OTHERWISE could just drop them out later too



# make a col converting each entrystamp to more useful dates
# need a weekly col to do weekly stats, and a daily col for stats within the week
def extract_from_stamp(x,desired='week'):
    # turn the string into time object
    stamp_obj = time.strptime(x,'%Y%m%d%H%M%S')
    if desired == 'week':
        # week number where week starts on Monday
        return int(time.strftime('%W',stamp_obj))
    elif desired == 'day':
        # get day of the week, starting with Mondays as zero
        ### BEWARE, using strftime('%w') gets the weekday num but starts on Monday
        return stamp_obj.tm_wday
    else:
        raise Warning('Don\'t understand desired formatting.')

for desired_time in ['week','day']:
    # df_drms.loc[:,desired_time] = df_drms['entry_tstamp'].apply(extract_from_stamp,args=(desired_time,))
    df_drms[desired_time] = df_drms['entry_tstamp'].apply(extract_from_stamp,args=(desired_time,))




# # get the number of dreams per DAY per week
# drms_per_day = df_drms.groupby(['week','day'])['drm'].max().astype(int)

# make a dataframe of daily info

#### TODO: somehow need to add indices for missing days (ie, when 0)
####     - add some other aggregated info here,
####        - many things can get aggregated here for plotting (eg, other lucidity characteristics)
drms_per_day = df_drms.groupby(['week','day']
    ).aggregate(
        {'drm': lambda x: float(max(x)), ## BEWARE here, that if there
                     ## are multiple entries on same day 
                     ## it will NOT add them together!!!
         'dream_type': lambda x: sum(x>2),
        }
    ).rename(columns=
        {'drm':        'n_dreams',
         'dream_type': 'n_LDs'
        }
    )

##### for LuCiD Scale (move up later)



#####



# # get dataframe of descriptives
# drms_per_week = drms_per_day.groupby('week').describe()

#### TODO:
####    - would it be better to do a count or mean??
####    - to get a mean should i divide by 7 instead??

drms_per_week = drms_per_day.groupby('week').sum()

# plot per week
# can't do error bars,
# but plot counts
ax = sea.barplot(data=drms_per_week.reset_index(),
    x='week',y='n_dreams',
    color='lightgray')
# overlay LD counts
sea.barplot(data=drms_per_week.reset_index(),
    x='week',y='n_LDs',
    color='blue',ax=ax)
# overlay circles for the count from each morning
sea.swarmplot(data=drms_per_day.reset_index(),
    x='week',y='n_dreams',
    color='white',ax=ax)










