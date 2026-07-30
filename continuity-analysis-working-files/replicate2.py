import pandas as pd, numpy as np
P='/tmp/gpps_practice.csv'
age=[f'aboutyouagemerged_{i}.pct' for i in range(1,10)]
outs={'Overall experience':'overallexp.pcteval','Wait acceptable':'lastgpapptwait.pcteval','Needs met':'lastgpapptneeds.pcteval','Confidence/trust':'lastgpapptconf.pcteval','Involved in decisions':'lastgpapptdecision.pcteval'}
bases={'Overall experience':'overallexp.baseevalw','Wait acceptable':'lastgpapptwait.baseevalw','Needs met':'lastgpapptneeds.baseevalw','Confidence/trust':'lastgpapptconf.baseevalw','Involved in decisions':'lastgpapptdecision.baseevalw'}
cols=['ad_practicecode','received','popsize','localgpservicesprefhpsee.pcteval','lastgpapptlengthgap_1.pct','lastgpapptlengthgap_2.pct']+age+list(outs.values())+list(bases.values())
d=pd.read_csv(P,usecols=cols,na_values=['/'],low_memory=False)
for c in cols:
 if c!='ad_practicecode': d.loc[pd.to_numeric(d[c],errors='coerce')<0,c]=np.nan
d['speed']=d['lastgpapptlengthgap_1.pct']+d['lastgpapptlengthgap_2.pct']
# covars
imd=pd.read_csv('/tmp/imd.csv'); imd=imd[imd['Area Type'].eq('GPs')][['Area Code','Value']].rename(columns={'Area Code':'ad_practicecode','Value':'imd'})
pay=pd.read_csv('/tmp/payments.csv',encoding='utf-8-sig',low_memory=False)
pay=pay[['Practice Code','Dispensing Practice','Practice Rurality','Average Number of Registered Patients']].rename(columns={'Practice Code':'ad_practicecode','Dispensing Practice':'dispensing','Practice Rurality':'rurality','Average Number of Registered Patients':'listsize'})
pay['dispensing']=(pay['dispensing'].astype(str).str.strip().str.lower()=='yes').astype(float)
pay['rural']=(pay['rurality'].astype(str).str.strip().str.lower()=='rural').astype(float)
d=d.merge(imd,on='ad_practicecode',how='left').merge(pay,on='ad_practicecode',how='left')
d['listsize']=pd.to_numeric(d['listsize'],errors='coerce').fillna(d['popsize']);d['loglist']=np.log(d['listsize'])
# WLS with HC1 sandwich
def fit(dat,ycol,weightcol,cov_age=True):
 predictors=['localgpservicesprefhpsee.pcteval','speed','imd','loglist','rural','dispensing']+(age[:-1] if cov_age else ['aboutyouagemerged_8.pct','aboutyouagemerged_9.pct'])
 z=dat[[ycol,weightcol]+predictors].dropna().copy()
 X=np.column_stack([np.ones(len(z))]+[z[c].to_numpy(float) for c in predictors]); y=z[ycol].to_numpy(float); w=z[weightcol].to_numpy(float)
 sw=np.sqrt(w); Xw=X*sw[:,None]; yw=y*sw
 inv=np.linalg.pinv(Xw.T@Xw); b=inv@(Xw.T@yw); resid=y-X@b
 # HC1 for WLS: score x_i*w_i*e_i
 meat=X.T@(((w**2)*resid**2)[:,None]*X); V=inv@meat@inv*len(z)/(len(z)-X.shape[1]); se=np.sqrt(np.diag(V))
 return len(z),predictors,b,se
print('merged',len(d),'valid base covars',d[['imd','loglist','rural','dispensing']].notna().all(axis=1).sum())
print('means imd continuity top vs speed top')
for sel in ['localgpservicesprefhpsee.pcteval','speed']:
 z=d.dropna(subset=[sel]).sort_values(sel);n=round(len(z)*.1);print(sel,'top',np.average(z.iloc[-n:].imd.dropna()),'bottom',np.average(z.iloc[:n].imd.dropna()),'n',n)
print('\nPRIMARY WLS outcome-specific base, full age shares')
for name,y in outs.items():
 n,p,b,se=fit(d,y,bases[name],True); bc=b[1]*.1;bs=b[2]*.1; sec=se[1]*.1;ses=se[2]*.1
 print(name,n,'cont',bc,sec,'speed',bs,ses,'ratio',bc/bs)
print('\nWLS received, full age shares')
for name,y in outs.items():
 n,p,b,se=fit(d,y,'received',True); print(name,n,'cont',b[1]*.1,se[1]*.1,'speed',b[2]*.1,se[2]*.1,'ratio',b[1]/b[2])
print('\nUNWEIGHTED, full age shares')
d['one']=1
for name,y in outs.items():
 n,p,b,se=fit(d,y,'one',True); print(name,n,'cont',b[1]*.1,se[1]*.1,'speed',b[2]*.1,se[2]*.1,'ratio',b[1]/b[2])
