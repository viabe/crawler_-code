
import datetime
import pandas as pd


def convert_date_str_to_ts(date_str):
    # date_str format 'YYYY/MM/DD'
    # return is timestamp

    year, month, day = [ int(date_info) for date_info in date_str.split("/") ]
    dtime = datetime.datetime(year,month,day)
    ts = int(dtime.timestamp())
    return ts


def save_result_date(dict_list, file_path):
        result_df = pd.DataFrame(dict_list)
        result_df.to_csv(file_path)