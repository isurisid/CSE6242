# %%
# Libraries
import re
import pandas as pd
from typing import Callable

# Imports
from . import median_ppsf as median_ppsf
from . import median_sale_price as median_sale_price
from . import percentage_fully_vaccinated as percentage_fully_vaccinated
from . import school_rating as school_rating
from . import tax_burden as tax_burden

# Reading the data
# ? WARNING: this might change in the future depending on data location
# dataset = pd.read_csv( "../data/v2-HousingRecommenderFinalDataset.csv")
# this multiplier can be changed if we consider to change importance's weight
IMPORTANCE_MULTIPLIER = 1.0
# Columns to index results
INDEX_COLS = ['county', 'state']

# Sample input
sample_input = {
  "House": "Single Family",
  "House Importance": "10",
  "Price": "$700,000+",
  "Price Importance": "5",
  "Feet": "2500+",
  "Feet Importance": "5",
  "Bedrooms": "3+",
  "Bedroom Importance": "7",
  "Bathrooms": "2+",
  "Bathroom Importance": "7",
  "TaxBurden": "25",
  "Tax Importance": "10",
  "Elementary": "8+",
  "Elementary Importance": "10",
  "Middle": "8+",
  "Middle Importance": "10",
  "High": "No Preference",
  "High Importance": "1",
  "Vaccinated": "50%+",
  "Vaccinated Importance": "3"
}


def remove_special_characters(raw_string: str) -> str:
    pattern = re.compile('[\\W_]+', re.UNICODE)
    return pattern.sub('', raw_string)


def sanitize_input(raw_input: dict) -> dict:
    clean_input = {
        'tax_burden': {
            'value': raw_input.get('TaxBurden', None),
            'importance': raw_input.get('Tax Importance', None)
        },
        'percentage_fully_vaccinated': {
            'value': raw_input.get('Vaccinated', None),
            'importance': raw_input.get('Vaccinated Importance', None)
        },
        'elementary_school_rating': {
            'value': raw_input.get('Elementary', None),
            'importance': raw_input.get('Elementary Importance', None)
        },
        'middle_school_rating': {
            'value': raw_input.get('Middle', None),
            'importance': raw_input.get('Middle Importance', None)
        },
        'high_school_rating': {
            'value': raw_input.get('High', None),
            'importance': raw_input.get('High Importance', None)
        }
    }
    # ? Fields compatible with R&P

    # !WARNING: all the following fields are not compatible with R&P
    # !WARNING: uncomment this once these columns are added to the R&P models
    # clean_input['median_sale_price'] = {
    #     'value': raw_input.get('Price', None),
    #     'importance': raw_input.get('Price Importance', None)
    # }
    # clean_input['property_type'] = {
    #     'value': raw_input.get('House', None),
    #     'importance': raw_input.get('House Importance', None)
    # }
    # clean_input['house_area'] = {
    #     'value': raw_input.get('Feet', None),
    #     'importance': raw_input.get('Feet Importance', None)
    # }
    # clean_input['bedroom_number'] = {
    #     'value': raw_input.get('Bedrooms', None),
    #     'importance': raw_input.get('Bedroom Importance', None)
    # }
    # clean_input['bathroom_number'] = {
    #     'value': raw_input.get('Bathrooms', None),
    #     'importance': raw_input.get('Bathroom Importance', None)
    # }

    # Converting the fields to float
    # If a field could not be converted, it is ignored
    final_input = {}
    for user_column, user_input in clean_input.items():
        if (user_input['value'] is None) or (user_input['importance'] is None):
            print(f"Field: '{user_column}' is not provided")
            continue
        try:
            final_input[user_column] = {
                'value': float(remove_special_characters(user_input['value'])),
                'importance': float(user_input['importance'])
            }
        except ValueError:
            print(f"Field: '{user_column}' could not be casted into float")

    return final_input


# ? For some counties of most recent datapoint is 2012-12-31
def calculate_coefficients(
    original_df: pd.DataFrame,
    column: str,
    user_value: float,
    importance: float,
    rp_function: Callable[[float, float], float]
) -> pd.DataFrame:
    result_df = (
        original_df
        .copy().set_index(INDEX_COLS).loc[:, [column]].dropna()
    )
    result_df[f'{column}_coeff'] = result_df[column].apply(
        lambda data_value: rp_function(user_value, data_value)
    )

    min_val = result_df[f'{column}_coeff'].min()
    max_val = result_df[f'{column}_coeff'].max()

    result_df[f'{column}_coeff_scaled'] = (
        (result_df[f'{column}_coeff'] - min_val) / (max_val - min_val)
    )

    result_df[f'{column}_results'] = (
        result_df[f'{column}_coeff_scaled']*(importance*IMPORTANCE_MULTIPLIER)
    )

    return result_df.loc[:, [f'{column}_results']]


def get_rp_function(column: str) -> Callable[[float, float], float]:
    # rp_function = Callable[[float, float], float]
    if column == 'median_ppsf':
        rp_function = median_ppsf.reward_and_punishment
    elif column == 'median_sale_price':
        rp_function = median_sale_price.reward_and_punishment
    elif column == 'percentage_fully_vaccinated':
        rp_function = percentage_fully_vaccinated.reward_and_punishment
    elif column == 'tax_burden':
        rp_function = tax_burden.reward_and_punishment
    elif column in [
        'high_school_rating',
        'middle_school_rating',
        'elementary_school_rating'
    ]:
        rp_function = school_rating.reward_and_punishment
    else:
        msg = f"Provided column: {column} is not valid for the R&P model"
        raise ValueError(msg)
    return rp_function


def main(original_df: pd.DataFrame, preferences_data: dict):
    results_df = original_df.copy().set_index(INDEX_COLS)
    results_df = results_df.drop(labels=results_df.columns, axis=1)
    for user_column, user_input in preferences_data.items():
        user_value = user_input['value']
        user_importance = user_input['importance']
        column_df = calculate_coefficients(
            original_df=original_df,
            column=user_column,
            user_value=user_value,
            importance=user_importance,
            rp_function=get_rp_function(column=user_column)
        )
        results_df = results_df.merge(
            column_df,
            how='left',
            right_index=True,
            left_index=True
        )
    results_df['score'] = results_df.fillna(0.0).sum(axis=1)
    return (
        results_df
        .sort_values(['score'], ascending=[0]).loc[:, ['score']].head(15)
    )


def reward_punishment_orchestrator(dataset, user_input):
    """
    Takes the R&P dataset and the user's input and generates the list of
    top 15 counties
    :param dataset: R&P dataset
    :param user_input: sanitized user input
    :return: dataframe with county and state as indices and score as the single column
    """
    preferences = sanitize_input(user_input)
    reward_punishment_recommendations = main(dataset, preferences)
    return reward_punishment_recommendations


if __name__ == '__main__':
    dataset = pd.read_csv("ML/rp/data/rp-final-dataset.csv")
    sample_preferences = sanitize_input(raw_input=sample_input)
    final_df = main(original_df=dataset, preferences_data=sample_preferences)
    print(final_df.head(5))
