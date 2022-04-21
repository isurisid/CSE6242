from io import StringIO
import requests
import pandas as pd

def get_covid_data():
    API_KEY="2c581a67ac0045ff88f776e32dff0564"
    response = requests.get(f"https://api.covidactnow.org/v2/counties.csv?apiKey={API_KEY}")
    covid_data = StringIO(response.text) 
    coviddf=pd.read_csv(covid_data)
    coviddf=coviddf[["state","county","actuals.cases","metrics.vaccinationsCompletedRatio","riskLevels.overall"]]
    riskLevelMapper={0:"Low",1:"Medium",2:"High",3:"Critical",4:"Unknown",5:"Extreme"}
    coviddf['risk']=coviddf['riskLevels.overall'].apply(lambda value: riskLevelMapper[value])
    coviddf.rename(columns={'state':'state_code','actuals.cases':'daily_cases','metrics.vaccinationsCompletedRatio':'percentage_fully_vaccinated','riskLevels.overall':'risk_index'}, inplace=True)
    coviddf['percentage_fully_vaccinated']=coviddf['percentage_fully_vaccinated']*100
    return coviddf


def get_final_dataset():
    property_df=pd.read_csv("/home/housingrecommendations/CSE6242/Housing Recommender System/DataExtraction/CleanedData/HousingRecommenderMetrics.csv")
    coviddf=get_covid_data()
    dfinal = property_df.merge(coviddf, on=["state_code","county"], how = 'left')
    dfinal=dfinal.drop(['Unnamed: 0'],axis=1)
    dfinal.to_csv("/home/housingrecommendations/CSE6242/Housing Recommender System/DataExtraction/final_data/HousingRecommenderFinalDataset.csv",index=False)
    print(dfinal.columns)
    return dfinal

def get_county_aggregated_dataset():
    dfinal=get_final_dataset()
    df_subset=dfinal[['county', 'state', 'state_code', 'tax_burden', 'medianage', 'cost_of_living_rank','elementary_school_rating', 'middle_school_rating','high_school_rating', 'daily_cases', 'percentage_fully_vaccinated','risk_index', 'risk']]
    df_unique = df_subset.groupby(by=['county','state_code'], as_index=False).first()
    df_unique.to_csv("/home/housingrecommendations/CSE6242/Housing Recommender System/DataExtraction/final_data/HousingRecommenderCountyAggregateDataset.csv",index=False)
    return df_unique

