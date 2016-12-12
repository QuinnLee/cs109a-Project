# -*- coding: utf-8 -*-
import os
import pandas as pd
import enchant as en

# TODO
# add encoding of (certain, not all) categorical vars
# 

def clean_data(dataset):
    '''Retaining all columns that are mostly non-null

    The rule is that every columns where the
    majority of the obs are NA is dropped. Everything
    else is kept.

    Args:
        dataset:    A pandas df of the raw csv

    Returns: 
        df:         A pandas df with only the
                    main 'base' features
    
    '''

    print "Now cleaning data."

    # Removing columns of mostly null values
    cols_to_keep = []

    for i in dataset.columns.values:
        if dataset[i].isnull().any() == True:
            ok = dataset[i].isnull().value_counts(sort = False) / len(dataset[i])
            ok = ok.reset_index()
            
            # Drop only cols for whom more than the majority (>50%) are missing
            if ok[ok['index'] == False][i].item() > 0.5:
                cols_to_keep.append(i)
        else:
            cols_to_keep.append(i)

    # Removing outliers
    df = dataset[(dataset['annual_inc'] <= 400000) & \
        (dataset['delinq_2yrs'].isnull() == False) & \
        (dataset['revol_util'] <= 130) & \
        (dataset['collections_12_mths_ex_med'].isnull() == False)].copy()

    # Ensuring everything is a float
    continous_cols =  ['loan_amnt','funded_amnt','funded_amnt_inv',\
        'installment','dti','revol_bal']

    for feature_name in continous_cols:
        df[feature_name] = df[feature_name].astype(float)
    
    # Converting strings to datetime objects
    for i in ['issue_d', 'last_pymnt_d', 'next_pymnt_d', 'last_credit_pull_d']:
        df[i] = pd.to_datetime(df[i])


    return df[cols_to_keep].copy()


def impute_missing(dataset):
    '''Imputing missing values

    Floats are filled with zero. Also, encodes categoricals.

    Args:
        dataset:    A pandas df.

    Returns self.
    '''
    print "Now imputing missing values."

    dataset[['tot_cur_bal', \
            'tot_coll_amt', \
            'total_rev_hi_lim']].fillna(value = 0, inplace = True)

    # Encode categoricals
    cat_cols = dataset.select_dtypes(include=['object']).columns

    dummy = pd.get_dummies(dataset[cat_cols])
    dataset.drop(cat_cols, axis = 1, inplace = True)
    df = pd.concat([dataset, dummy], axis=1)

    return df


def misspelling_intensity(data_cell):
    '''Gives an 'intensity' of spelling errors

    For every data cell with a string in it (e.g. employment title),
    splits the string into words, spell checks those words, and returns
    the % of words that were incorrectly spelled.

    This func will be applied to a pandas df using the .apply()
    method.

    Args:
        data_cell:      A pandas df cell. 

    Returns:
        percent_wrong:  The % of words that the person spelled
                        incorrectly.

    '''

    # scope problem: defines this every time it's run
    spell_check = en.Dict('en_US')

    string_list = str(data_cell).split()
    errors_list = [spell_check.check(x) for x in string_list]
    percent_wrong = float(errors_list.count(False)) / len(errors_list)

    return percent_wrong


def spelling_mistakes(dataset):
    '''Calculates the percentage of misspellings for each string column

    Args:
        dataset:    A pandas df, expects it to be cleaned.

    Returns:
        self, with two new columns
    
    '''

    print "Now calculating spelling mistakes.\nThis may take a while."

    for s in ['emp_title', 'title']:
        dataset['{}_percent_misspelled'.format(s)] = dataset[s].apply(misspelling_intensity)

    dataset.drop(['emp_title', 'title'], inplace = True) 

    return dataset.copy()


if __name__ == '__main__':
    print "Just do this in the jupyter notebook. Don't bother here."



