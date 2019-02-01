import pandas as pd

originalBFQs = pd.read_excel('FLG_BFQ_ursp.xlsx')[['FahrlageID', 'BFQ']].set_index('FahrlageID')
curBFQs = pd.read_csv('flgbfq.csv').set_index('FLID')
curTimes = pd.read_csv('einzelbelTimes.csv', names=['FahrlageID', 'ResponseTime']).set_index('FahrlageID')

df = pd.concat([originalBFQs, curBFQs, curTimes], axis=1, sort=False).dropna()

print('Size: ', df.count())

def percentiles(s):
	return [s.quantile(0.5), s.quantile(0.75), s.quantile(0.9), s.quantile(0.95), s.quantile(0.99), s.quantile(0.999),  s.max()]

stats = pd.DataFrame.from_dict( {
	'Response Times': percentiles(df['ResponseTime']),
	'Automatic BFQ ZT': percentiles(df['ZTBFQ']),
	'Automatic BFQ TR': percentiles(df['TBFQ']),
	'Manual BFQ': percentiles(df['BFQ'])
	}, orient='index', columns=['50%', '75%', '90%', '95%', '99%', '99.9%', 'Max'] )

print(stats)

print("Response time above 3 minutes\n", df[df['ResponseTime']>=180].count())