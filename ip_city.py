import pandas as pd
import time
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def ip_int(ip_str):
    """
    input ip address such as 69.166.124.6 , return as 1168538630
    :param ip_str:str
    :return: int
    """
    list_ip = ip_str.split('.')
    num = int(int(list_ip[0])*pow(256, 3)+int(list_ip[1])*pow(256, 2)+int(list_ip[2])*pow(256, 1)+int(list_ip[3]))
    return num


df = pd.read_csv('access.log', sep='\t', encoding='utf-8', header=None, names=['Apache_log'])
df.columns = ['log']
pat1 = r'^(?P<IP>\S+)\s+\S+\s+\S+\s+'
pat2 = r'\[(?P<timestamp>.+)\]\s+'
pat3 = r'"(?P<request>.+)"\s+'
pat4 = r'(?P<code>\S+)\s+(?P<size>\S+)'
pat = pat1 + pat2 +pat3 +pat4

series = df['log'].str.split(pat, expand=True)
df['ip'] = series[1].apply(lambda x: ip_int(x))
df.drop('log', axis=1, inplace=True)
result = df.copy()
result['stamp'] = pd.to_datetime(series[2], format='%d/%m/%Y:%H:%M:%S %z')
result['request'] = series[3]
result['response_code'] = series[4]
result['response_code'] = result['response_code'].astype('category')
result['size'] = series[5]

df.set_index('ip', inplace=True)
df_city = pd.read_csv('IP2LOCATION.csv', header=None, usecols=[0, 1, 5])
df_city.columns = ['ip_begin', 'ip_end', 'city']
print(f"city data set is:\n{df_city.head()}")
print('-'*30)
ip_list = list(df_city['ip_begin'])
ip_list.append(df_city.iloc[-1, -2])
index = list(df_city.index)

begin_time = int(time.time())
# pd.cut : segment and sort data values into bins
c = pd.cut(x=df.index, bins=ip_list, include_lowest=True, labels=index).astype(int)
d = list(c)
d = df_city.iloc[d, [2]]
result.reset_index(drop=True, inplace=True)
d.reset_index(drop=True, inplace=True)
result['city'] = d['city']
result.to_csv('log.csv',index=False,header=True,mode="w")
print(result.iloc[:,[0,5]].head())
print('-'*30)
end_time = int(time.time())
print(f"This task spend  {round((end_time - begin_time) / 60, 2)} minutes.")