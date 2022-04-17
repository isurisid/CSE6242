import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
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
        inputVec=np.array(inputVec)
        self.df['sim']= self.df.apply(lambda x: self.cosine_sim(inputVec, np.array(x.astype(object).values)), axis=1)
        #self.df['euclidean_distance']=self.df.apply(lambda x: self.l2Norm(inputVec,x.astype(object).values),axis=1)
        return self.df.nlargest(n_rec,"sim")

def getDataset():
    df=pd.read_csv("../rp/data/v2-HousingRecommenderFinalDataset.csv")
    df=df[["period_end","county","state","state_code","property_type","property_type_id","median_sale_price","median_ppsf","percentage_fully_vaccinated","tax_burden",'risk_index', 'risk',
        'cost_of_living_rank','medianage']]
    df['tax_burden'] = df['tax_burden'].astype(str).apply(lambda x: x.split("%")[0]).astype(float)
    df=df[df['property_type']=="All Residential"]
    return df


def randomizeSchoolRatings(df):
    elem_school=[random.uniform(1,10) for i in range(0,len(df))]
    middle_school=[random.uniform(1,10) for i in range(0,len(df))]
    high_school=[random.uniform(1,10) for i in range(0,len(df))]
    df['elementary_school_rating']=elem_school
    df['middle_school_rating']=middle_school
    df['high_school_rating']=high_school
    return df

def getGroupedDf(df):
    grouped_df=df.groupby(['county','state']).agg(median_sale_price=("median_sale_price","mean"),median_ppsf=("median_ppsf","mean"),percentage_fully_vaccinated=("percentage_fully_vaccinated","mean"),total_tax_burden=("tax_burden",pd.Series.mode),risk_index=("risk_index",pd.Series.mode),cost_of_living_rank=("cost_of_living_rank",pd.Series.mode),median_age=("medianage",np.median),elementary_school_rating=("elementary_school_rating","mean"),middle_school_rating=("middle_school_rating","mean"),high_school_rating=("high_school_rating","mean"))
    grouped_df=grouped_df.astype(object)
    grouped_df=grouped_df.dropna()
    return grouped_df

def generatePreferences(pivotRecommendations):
    pr=pivotRecommendations
    print(pr)
    df=getDataset()
    df=randomizeSchoolRatings(df)
    grouped_df=getGroupedDf(df)
    print(grouped_df)
    cbr=CBRecommend(df=grouped_df)
    new_df=cbr.recommend(record=grouped_df.index[0],n_rec=len(grouped_df))
    new_df['sim']=new_df['sim'].apply(lambda x: Decimal(x))
    print(new_df['sim'])

