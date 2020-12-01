# coding:utf-8
import requests
import pandas as pd
from config import *


def get_rank_info(response_data, sort_by):
    data = response_data.split("[\"")[1].split("\"]")[0]
    cnt = 0
    fund_list = []
    for line in data.split("\",\""):
        item_list = line.split(",")
        if len(item_list) > 0:
            cnt += 1
            fund_dict = dict()
            fund_dict['code'] = item_list[0]
            fund_dict[sort_by] = cnt
            fund_dict['name'] = item_list[1]
            fund_list.append(fund_dict)
    fund_df = pd.DataFrame(fund_list)
    return fund_df


def get_return_rate_rank(fund_type, num, sort_by_list):
    ret = None
    for sort_by in sort_by_list:
        fund_url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={0}&rs=&gs=0&sc={1}zf" \
                   "&st=desc&pi=1&pn={2}&dx=1".format(fund_type, sort_by, num)
        response = requests.get(fund_url, timeout=100, headers=COMMON_HEADERS)
        df = get_rank_info(response.text, sort_by)
        if ret is None:
            ret = df.copy()
        else:
            ret = ret.merge(df.drop('name', axis=1), on='code', how='outer')
    col_list = ['code', 'name'] + sort_by_list
    ret = ret.ix[:, col_list]
    ret['rank_avg'] = ret.apply(lambda x: int(x[2:].mean()), axis=1)
    ret['rank_std'] = ret.apply(lambda x: int(x[2:].std()), axis=1)
    col_list = ['code', 'rank_avg', 'rank_std'] + sort_by_list + ['name']
    ret = ret.ix[:, col_list]
    ret = ret.sort_values(by=['rank_avg', 'rank_std'], ascending=True)
    return ret.reset_index(drop=True)


def rr_rank_master(chose_type, time_list):
    rank_df = get_return_rate_rank(fund_type=chose_type, num=10000, sort_by_list=time_list)
    rank_df.to_csv(u'data/{}基金_收益率排名_{}.csv'.format(FUND_TYPE.get(chose_type), DATE_NOW), index=False,
                   encoding='utf-8')
    print(rank_df.shape)
    print(rank_df.head())
    return


if __name__ == '__main__':
    rr_rank_master('zs', ['1y', '3y', '6y', '1n', '2n'])
