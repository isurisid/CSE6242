import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
from numpy import dot
from numpy.linalg import norm 
from decimal import Decimal

class CBRecommend():
    def __init__(self, df):
        self.df = df
        
    def cosine_sim(self, v1,v2):
        '''
        This function will calculate the cosine similarity between two vectors
        '''
        v1=np.array(v1)
        v2=np.array(v2)
        return dot(v1,v2)/(norm(v1)*norm(v2))
    
    def l2Norm(self,v1,v2):
        v1=np.array(v1)
        v2=np.array(v2)
        return np.sum(np.square(v1 - v2))
    
    def recommend(self, record, n_rec):
        """
        df (dataframe): The dataframe
        song_id (string): Representing the song name
        n_rec (int): amount of rec user wants
        """
        inputVec = self.df.astype(object).loc[record].values
        print(inputVec)
        inputVec=np.array(inputVec)
        self.df['sim']= self.df.apply(lambda x: self.cosine_sim(inputVec, np.array(x.astype(object).values)), axis=1)
        #print(self.df)
        #self.df['euclidean_distance']=self.df.apply(lambda x: self.l2Norm(inputVec,x.astype(object).values),axis=1)
        return self.df.nlargest(n_rec,"sim")

def getDataset():
    df=pd.read_csv("./ML/rp/data/rp-final-dataset.csv")
    df=df[["period_end","county","state","state_code","median_ppsf","percentage_fully_vaccinated","tax_burden",'risk_index', 'risk',
        'cost_of_living_rank','medianage','elementary_school_rating','middle_school_rating','high_school_rating']]
    df['tax_burden'] = df['tax_burden'].astype(str).apply(lambda x: x.split("%")[0]).astype(float)
    return df


def getGroupedDf(df):
    grouped_df=df.groupby(['county','state_code']).agg(median_ppsf=("median_ppsf","mean"),percentage_fully_vaccinated=("percentage_fully_vaccinated","mean"),total_tax_burden=("tax_burden",pd.Series.mode),risk_index=("risk_index",pd.Series.mode),cost_of_living_rank=("cost_of_living_rank",pd.Series.mode),median_age=("medianage",np.median),elementary_school_rating=("elementary_school_rating","mean"),middle_school_rating=("middle_school_rating","mean"),high_school_rating=("high_school_rating","mean"))
    grouped_df=grouped_df.astype(object)
    grouped_df=grouped_df.dropna()
    return grouped_df

def generatePreferences(pivotRecommendations):
    pr=pivotRecommendations
    df=getDataset()
    grouped_df=getGroupedDf(df)
    cbr=CBRecommend(df=grouped_df)
    new_df=cbr.recommend(record=pr.index[0],n_rec=len(grouped_df))
    new_df['sim']=new_df['sim'].apply(lambda x: Decimal(x))
    new_df['rank'] = new_df['sim'].rank(ascending = 0).astype(int)
    new_df['Top 20'] = np.where(new_df['rank']<= 19, True, False).astype("str")
    new_df=new_df.reset_index()
    new_df.rename(columns={'state_code':'state'}, inplace=True)
    new_df=new_df.drop(['sim'], axis=1)
    print(f"NEW DF {new_df} ")
    print(new_df.dtypes)
    return new_df