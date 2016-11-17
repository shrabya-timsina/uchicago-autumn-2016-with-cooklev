# CS121: Current Population Survey (CPS) 
#
# Functions for mining CPS data 

import csv
import math
import numpy as np
import os
import pandas as pd
import sys
import tabulate
import pa6_helpers

# Constants 
HID = "h_id" 
AGE = "age"
GENDER = "gender" 
RACE = "race" 
ETHNIC = "ethnicity" 
STATUS = "employment_status"
HRWKE = "hours_worked_per_week" 
EARNWKE = "earnings_per_week" 

FULLTIME_MIN_WORKHRS = 35

# CODE_TO_FILENAME: maps a code to the name for the corresponding code
# file
CODE_TO_FILENAME = {"gender_code":"data/gender_code.csv",
                    "employment_status_code": "data/employment_status_code.csv",
                    "ethnicity_code":"data/ethnic_code.csv",
                    "race_code":"data/race_code.csv"}


# VAR_TO_FILENAME: maps a variable-of-interest to the name for the
# corresponding code file
VAR_TO_FILENAME = {GENDER: CODE_TO_FILENAME["gender_code"],
                        STATUS: CODE_TO_FILENAME["employment_status_code"],
                        ETHNIC: CODE_TO_FILENAME["ethnicity_code"],
                        RACE: CODE_TO_FILENAME["race_code"]}




def build_morg_df(morg_filename):
    '''
    Construct a DF from the specified file.  Resulting dataframe will
    use names rather than coded values.
    
    Inputs:
        morg_filename: (string) filename for the morg file.

    Returns: pandas dataframe
    '''

    # Your code here...

    # replace None with suitable return value

    
    if os.path.exists(morg_filename) == False:
        return None
      
    morg_df = pd.read_csv(morg_filename)

    for col_name in morg_df.columns[2:6]:
        
        code_file = pd.read_csv(CODE_TO_FILENAME[col_name])
        categories = code_file[code_file.columns[1]].values

        if col_name != "ethnicity_code":
           
            morg_df[col_name] = pd.Categorical.from_codes(morg_df[col_name] - 1, categories)

        else:
            morg_df[col_name] = morg_df[col_name].fillna(value = 0)
            morg_df[col_name] = pd.Categorical.from_codes(morg_df[col_name], categories)
    
        
        morg_df.rename(columns = {col_name: col_name[:len(col_name) - 5]}, inplace=True)

    return morg_df



def calculate_weekly_earnings_stats_for_fulltime_workers(df, gender, race, ethnicity):
    '''
    Calculate statistics for different subsets of a dataframe.

    Inputs:
        df: morg dataframe
        gender: "Male", "Female", or "All"
        race: specific race from a small set, "All", or "Other",
            where "Other" means not in the specified small set
        ethnicity: "Hispanic", "Non-Hispanic", or "All"

    Returns: (mean, median, min, max) for the rows that match the filter.
    '''

    
    valid_gender = ["Male", "Female", "All"]

    possible_single_races = ["WhiteOnly", "BlackOnly", 
        "AmericanIndian/AlaskanNativeOnly", "AsianOnly", 
        "Hawaiian/PacificIslanderOnly"]

    valid_races = possible_single_races + ["Other", "All"]
    
    valid_ethnicity = ["Hispanic", "Non-Hispanic", "All"]
    
   

    if (gender not in valid_gender) or (race not in valid_races) \
        or (ethnicity not in valid_ethnicity):
        return (0,0,0,0)

    
    search_criteria = (df.hours_worked_per_week >= 35) & \
        (df.employment_status == 'Working')


    if gender != "All":
        search_criteria = search_criteria & (df.gender == gender)

   
    if race in possible_single_races:
        search_criteria = search_criteria & (df.race == race)
    elif race == "Other":
        search_criteria = search_criteria & \
            (df.race.isin(possible_single_races) == False)


    if ethnicity == "Hispanic":
        search_criteria = search_criteria & (df.ethnicity != "Non-Hispanic")
    elif ethnicity == "Non-Hispanic":
        search_criteria = search_criteria & (df.ethnicity == "Non-Hispanic")

   

    filtered_df = df[search_criteria]

    mean_earning = filtered_df[EARNWKE].mean()
    median_earning = filtered_df[EARNWKE].median()
    min_earning = filtered_df[EARNWKE].min()
    max_earning = filtered_df[EARNWKE].max()

    return (mean_earning, median_earning, min_earning, max_earning)


def create_histogram(df, var_of_interest, num_buckets, min_val, max_val):
    '''
    Compute the number of full time workers who fall into each bucket
    for a specified number of buckets and variable of interest.

    Inputs:
        df: morg dataframe
        var_of_interest: one of EARNWKE, AGE, HWKE
        num_buckets: the number of buckets to use.
        min_val: minimal value (lower bound) for the histogram (inclusive)
        max_val: maximum value (lower bound) for the histogram (non-inclusive).

    Returns:
        list of integers where ith element is the number of full-time workers who fall into the ith bucket.

        empty list if num_buckets <= 0 or max_val <= min_val
    '''

    # Your code here...

    # replace [] with a suitable return value
    
    if (num_buckets <= 0) or (max_val <= min_val):
        return []

    boundaries = np.linspace(min_val, max_val, num = num_buckets + 1)
    print(boundaries)
    
    working_criteria = (df.hours_worked_per_week >= 35) & \
        (df.employment_status == 'Working')

    filtered_df = df[working_criteria]

    filtered_df["bin"] = pd.cut(filtered_df[var_of_interest], 
                            bins=boundaries,
                            labels=range(len(boundaries)-1),
                            include_lowest=True, right=False)


    bucket_counts_series = (filtered_df["bin"].value_counts().sort_index())
    bucket_counts_list = bucket_counts_series.tolist()
    print(bucket_counts_list)

    return bucket_counts_list


def calculate_unemployment_rates(filenames, age_range, var_of_interest):
    '''
    Calculate the unemployment rate for participants in a given age range (inclusive)
    by values of the variable of interest.

    Inputs:
        filenames: (list of strings) list of morg filenames
        age_range: (pair of ints) (lower_bound, upper_bound)
        var_of_interest: one of "gender", "race", "ethnicity"

    Returns: pandas dataframe
    '''

    # Your code here...

    # replace None with suitable return value
    

    

    valid_var_of_interest = [GENDER, RACE, ETHNIC]   

    if (var_of_interest not in valid_var_of_interest):
        return (0,0,0,0)
    
    (lower_bound, upper_bound) = age_range
     
    
    code_file = pd.read_csv(VAR_TO_FILENAME[var_of_interest])
    categories = code_file[code_file.columns[1]].values
    unemployment_rates_df = pd.DataFrame(index = categories)
    #print(unemployment_rates_df)




    for dataset in filenames:

        year = dataset[11:13]
        unemployment_rates_df[year] = np.nan 
        #year_series = pd.Series(np.zeros(shape = (len(unemployment_rates_df.index),) ) )
        

        df = build_morg_df(dataset)
        
        search_criteria = (df.age >= lower_bound) & (df.age <= upper_bound)
        #search_criteria = search_criteria & (df.employment_status == "Layoff") | (df.employment_status == "Looking")
        df = df[search_criteria]

        

        for category in categories:
            print(category)

            filtered_df = df[df[var_of_interest] == category]
            print(filtered_df)
            
            num_of_unemployed = (filtered_df[STATUS] == "Layoff").sum() + \
                (filtered_df[STATUS] == "Looking").sum()
            print("unemp", num_of_unemployed)

            total_num_of_individuals = num_of_unemployed + (filtered_df[STATUS] == "Working").sum()
            print("unemp", total_num_of_individuals)

            if total_num_of_individuals > 0:
                unemployment_rate = num_of_unemployed / total_num_of_individuals
                                
            else:
                unemployment_rate = 0.0

            print(unemployment_rate)

            unemployment_rates_df.set_value(category, year, unemployment_rate)
            print(unemployment_rates_df)





    return unemployment_rates_df
   
morg_filename = "data/morg_d10_mini.csv"
df = build_morg_df(morg_filename)
gender = "Female"
race = "WhiteOnly"
ethnicity = "Non-Hispanic"

"""
code_file = pd.read_csv(VAR_TO_FILENAME[RACE])
categories = code_file[code_file.columns[1]].values
unemployment_rates = pd.DataFrame(index = categories)
print(unemployment_rates)
print(type(unemployment_rates))
"""

rate_df = calculate_unemployment_rates(["data/morg_d14.csv", "data/morg_d10.csv", "data/morg_d07.csv"], (50, 70), GENDER)
print(rate_df)