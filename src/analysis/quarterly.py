
import glob
import json
import pandas as pd


HOME = glob.os.path.expanduser('~')
DATA_DIR = glob.os.path.join(HOME,'DBp/proj/meddl/data')
FILE_GLOB = glob.os.path.join(DATA_DIR,'quarterly/*.txt')

fnames = sorted(glob.glob(FILE_GLOB))

df_list = []

for fn in fnames:
    # import json
    with open(fn, 'r') as infile:
        data = json.load(infile)
    # each dict value needs to be in list format for pandas
    data = { k: [v] for k, v in data.iteritems() }
    # convert dict to 1xncols pandas dataframe
    temp_df = pd.DataFrame.from_dict(data,orient='columns')

    df_list.append(temp_df)


df = pd.concat(df_list,ignore_index=True)
