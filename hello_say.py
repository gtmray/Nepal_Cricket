import pandas as pd
import matplotlib.pyplot as plt
file = pd.read_csv("t20_matches.csv",sep=",")
filtered = file[['match_id','series_id','match_details','result','scores','date','venue','winner','DL_method']].copy()
'''pd.options.mode.chained_assignment = None
print(filtered[(filtered.winner!='No result') & (filtered.winner!='Match abandoned without a ball bowled')].winner.value_counts())
filtered.DL_method.replace({"1.0":"True","":"False"},inplace = True)'''
filtered.DL_method = filtered.DL_method.fillna(0)
filtered['DL_method'] = filtered.DL_method.astype(bool)
filtered['date'] = pd.to_datetime(filtered['date'])
filtered.set_index('date',inplace=True)
filtered.drop(['match_id','series_id'],axis='columns',inplace = True)
nep_data = filtered[filtered['match_details'].str.contains('Nepal')].copy()
nep_data.dropna( subset = ['scores'],inplace= True)
#except AttributeError: nepal_score =
scores = []
for i in range(0,len(nep_data.index)):
    nepal = nep_data.scores.iloc[i].partition("Nepal")[2]
    try:
        nepal_score = int(nepal.partition("/")[0])
    except ValueError:
        try:
            nepal_score = int(nepal.partition("(")[0])
        except:
            nepal_score = 0
    #print(nepal_score)
    scores.append(nepal_score)
    #nep_data['Nepal score'] = pd.Series(scores)
nep_data['Nepal_score'] = scores
daily_score = nep_data.groupby(nep_data.venue).Nepal_score.mean()
daily_score.plot(kind='bar')
plt.xlabel('Venue')
plt.ylabel('Score of Nepal')
plt.title('T20s score of Nepal from 2012-2017')
plt.show()
print(nep_data.head())
print(nep_data.info())

