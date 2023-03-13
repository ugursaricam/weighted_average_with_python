###################################################
# Rating Products
###################################################

# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating
# - Bayesian Average Rating Score

############################################
# Data Preparation
############################################

import pandas as pd
import datetime as dt

# pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_csv('datasets/course_reviews.csv')
df = df_.copy()

df.head()
df.shape
df.info()
df.isnull().sum()
df.describe().T

# rating distribution
df['Rating'].value_counts()

df['Questions Asked'].value_counts()

df.groupby('Questions Asked').agg({'Questions Asked': 'count',
                                   'Rating': 'mean'})

############################################
# Calculating Average
############################################

df['Rating'].mean()  # 4.764284061993986

############################################
# Time-Based Weighted Average
############################################

df.info()

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

df['Timestamp'].max()  # Timestamp('2021-02-05 07:45:55')

today_date = pd.to_datetime('2021-02-10 0:0:0') # Timestamp('2021-02-05 07:45:55') + 5 days

df['days'] = (today_date - df['Timestamp']).dt.days

# calculating customer age
df['Enrolled'] = pd.to_datetime(df['Enrolled'])
df['customer_age_days'] = (today_date - df['Enrolled']).dt.days
df.sort_values('customer_age_days', ascending=True)

# ratings made in the last 30 days
last_30 = df[df['days'] <= 30]['Rating'].mean()
# alt # df.loc[df['days'] <= 30, 'Rating'].mean()

# rating between 30 days and 90 days
between_30_90 = df[(df['days'] > 30) & (df['days'] <= 90)]['Rating'].mean()
# alt # df.loc[(df['days'] > 30) & (df['days'] <= 90), 'Rating'].mean()

# rating between 90 days and 180 days
between_90_180 = df[(df['days'] > 90) & (df['days'] <= 180)]['Rating'].mean()

# rating made more than 180 days ago
older_than_180 = df[df['days'] > 180]['Rating'].mean()

time_based_mean = last_30 * .28 + between_30_90 * .26 + between_90_180 * .24 + older_than_180 * .22
time_based_mean # 4.765025682267194

############################################
# Functionalized Time-Based Weighted Average
############################################

def time_based_weighted_average(dataframe, w1=.28, w2=.26, w3=.24, w4=.22):
    last_30 = dataframe[dataframe['days'] <= 30]['Rating'].mean()
    between_30_90 = dataframe[(dataframe['days'] > 30) & (dataframe['days'] <= 90)]['Rating'].mean()
    between_90_180 = dataframe[(dataframe['days'] > 90) & (dataframe['days'] <= 180)]['Rating'].mean()
    older_than_180 = dataframe[dataframe['days'] > 180]['Rating'].mean()
    time_based_mean = last_30 * w1 + between_30_90 * w2 + between_90_180 * w3 + older_than_180 * w4
    return time_based_mean


time_based_weighted_average(df) # 4.765025682267194
time_based_weighted_average(df, .40, .30, .20, .10) # 4.766601778153862

############################################
# User-Based Weighted Average
############################################

df.groupby('Progress').agg({'Rating': 'mean'})

df[df['Progress'] < 10].describe().T

progress_less_than_10 = df[df['Progress'] <= 10]['Rating'].mean()
progress_between_10_45 = df[(df['Progress'] > 10) & (df['Progress'] <= 45)]['Rating'].mean()
progress_between_45_75 = df[(df['Progress'] > 45) & (df['Progress'] <= 75)]['Rating'].mean()
progress_more_than_75 = df[df['Progress'] > 75]['Rating'].mean()

user_based_mean = progress_less_than_10 * .22 + progress_between_10_45 * .24 + progress_between_45_75 * .26 + progress_more_than_75 * .28

user_based_mean # 4.800257704672543

############################################
# Functionalized User-Based Weighted Average
############################################

def user_based_weighted_average(dataframe, w1=.22, w2=.24, w3=.26, w4=.28):
    progress_less_than_10 = dataframe[dataframe['Progress'] <= 10]['Rating'].mean()
    progress_between_10_45 = dataframe[(dataframe['Progress'] > 10) & (dataframe['Progress'] <= 45)]['Rating'].mean()
    progress_between_45_75 = dataframe[(dataframe['Progress'] > 45) & (dataframe['Progress'] <= 75)]['Rating'].mean()
    progress_more_than_75 = dataframe[dataframe['Progress'] > 75]['Rating'].mean()
    user_based_mean2 = progress_less_than_10 * w1 + progress_between_10_45 * w2 + progress_between_45_75 * w3 + progress_more_than_75 * w4
    return user_based_mean2


user_based_weighted_average(df) # 4.800257704672543
user_based_weighted_average(df, .10, .20, .30, .40) # 4.819874780755226

# Progress based
# (df['Progress']/df['Progress'].sum()).sum()
# (df['Rating'].mean() * (df['Progress']/df['Progress'].sum())).sum()

############################################
# Weighted Rating
############################################

def weighted_rating(dataframe, time_based=.50, user_based=.50):
    return (time_based_weighted_average(dataframe) * time_based) + (user_based_weighted_average(dataframe) * user_based)

weighted_rating(df) # 4.782641693469868
weighted_rating(df, .2, .8) # 4.793211300191473

# SOR
# df.groupby('Timestamp').agg({'Rating': 'mean'}).sort_values('Timestamp', ascending=False)
# df['segment'] = pd.qcut(df['Timestamp'].rank(method='first'), 4, labels=['D', 'C', 'B', 'A'])
## df['segment'] = pd.cut(df['days'], 4, labels=['A', 'B', 'C', 'D'])
## df[df['days'] <= 161]['Rating'].mean()
# df.groupby('segment').agg({'Rating' : 'mean'})


