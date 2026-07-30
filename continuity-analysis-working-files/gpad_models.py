exec(open('/tmp/replicate2.py').read().split("print('merged")[0])
g=pd.read_csv('/tmp/gpad_agg.csv')
jf=g[g.period.eq('janfeb')].set_index('GP_CODE')
m=g[g.period.eq('mar')].set_index('GP_CODE')
for c in ['all_fast','all_known','all_total','gp_fast','gp_known','gp_total']:
 jf[c+'_3m']=jf[c].add(m[c],fill_value=0)
jf['gpad_all_2m']=jf.all_fast/jf.all_known;jf['gpad_gp_2m']=jf.gp_fast/jf.gp_known
jf['gpad_all_3m']=jf.all_fast_3m/jf.all_known_3m;jf['gpad_gp_3m']=jf.gp_fast_3m/jf.gp_known_3m
D=d.merge(jf.reset_index(),left_on='ad_practicecode',right_on='GP_CODE',how='left')
basecov=['imd','loglist','rural','dispensing']+age[:-1]
def fit2(ycol,preds,wcol='received'):
 z=D[[ycol,wcol]+preds+basecov].dropna();
 X=np.column_stack([np.ones(len(z))]+[z[c].to_numpy(float) for c in preds+basecov]);y=z[ycol].to_numpy(float);w=z[wcol].to_numpy(float)
 sw=np.sqrt(w);Xw=X*sw[:,None];yw=y*sw;inv=np.linalg.pinv(Xw.T@Xw);b=inv@(Xw.T@yw);e=y-X@b
 meat=X.T@(((w**2)*e**2)[:,None]*X);V=inv@meat@inv*len(z)/(len(z)-X.shape[1]);se=np.sqrt(np.diag(V))
 return len(z),b[1:1+len(preds)],se[1:1+len(preds)]
print('coverage',D[['gpad_all_2m','gpad_gp_2m','gpad_all_3m','gpad_gp_3m']].notna().sum().to_dict())
print('corr',D[['speed','gpad_all_2m','gpad_gp_2m','gpad_all_3m','gpad_gp_3m']].corr().round(3).to_string())
models={
'GPPS speed':['localgpservicesprefhpsee.pcteval','speed'],
'GPAD all 2m':['localgpservicesprefhpsee.pcteval','gpad_all_2m'],
'GPAD GP 2m':['localgpservicesprefhpsee.pcteval','gpad_gp_2m'],
'Both + all 2m':['localgpservicesprefhpsee.pcteval','speed','gpad_all_2m'],
'Both + GP 2m':['localgpservicesprefhpsee.pcteval','speed','gpad_gp_2m'],
'GPAD all 3m':['localgpservicesprefhpsee.pcteval','gpad_all_3m'],
'GPAD GP 3m':['localgpservicesprefhpsee.pcteval','gpad_gp_3m']}
for mn,preds in models.items():
 print('\nMODEL',mn)
 for name,y in outs.items():
  n,b,se=fit2(y,preds); vals=' '.join(f'{p}={bb*10:.3f}pp(se{ss*10:.3f})' for p,bb,ss in zip(preds,b,se)) # proportion*0.1*100 = *10 pp
  print(name,n,vals)
