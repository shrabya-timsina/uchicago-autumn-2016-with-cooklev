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

    # Your code here...

    # replace [0,0,0,0] with a suitable return value
    
    valid_gender = ["Male", "Female", "All"]

    possible_single_races = ["WhiteOnly", "BlackOnly", 
        "AmericanIndian/AlaskanNativeOnly", "AsianOnly", 
        "Hawaiian/PacificIslanderOnly"]

    valid_races = possible_single_races + ["Other", "All"]
    
    valid_ethnicity = ["Hispanic", "Non-Hispanic", "All"]
    
   

    if (gender not in valid_gender) or (race not in valid_races) \
        or (ethnicity not in valid_ethnicity):
        return (0,0,0,0)

    
    search_criteria = (df.hours_worked_per_week > 35) & \
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
    #print(filtered_df)

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
    return []


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
    return None



    

    
    
morg_filename = "data/morg_d07.csv"
df = build_morg_df(morg_filename)
gender = "All"
race = "BlackOnly"
ethnicity = "Non-Hispanic"
zz = calculate_weekly_earnings_stats_for_fulltime_workers(df, gender, race, ethnicity)
print(zz)