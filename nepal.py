import pandas as pd
import matplotlib.pyplot as plt

#Data reading and cleaning
file = pd.read_csv("t20_matches.csv",sep=",")
filtered = file[['match_id','series_id','match_details','result','scores','date','venue','winner','DL_method']].copy()
filtered.DL_method = filtered.DL_method.fillna(0)
filtered['DL_method'] = filtered.DL_method.astype(bool)
filtered['date'] = pd.to_datetime(filtered['date'])
filtered.set_index('date',inplace=True)
filtered.drop(['match_id','series_id'],axis='columns',inplace = True)

#scraping Nepal's data
nep_data = filtered[filtered['match_details'].str.contains('Nepal')].copy()
nep_data.dropna( subset = ['scores'],inplace= True)

#scraping Nepal's score
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
    scores.append(nepal_score)
nep_data['Nepal_score'] = scores
score_certain = nep_data.groupby(nep_data.venue).Nepal_score.mean()

#Data Visualization
score_certain.plot(kind='bar')
plt.xlabel('Venue')
plt.ylabel('Score of Nepal')
plt.title('T20s score of Nepal from 2012-2017')
plt.show()

