# -*- coding: utf-8 -*-
import os
import pandas as pd


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
    for i in ['last_pymnt_d', 'next_pymnt_d', 'last_credit_pull_d']:
        df[i] = pd.to_datetime(df[i])


    return df[cols_to_keep]


def impute_missing(dataset):
    '''Imputing missing values

    Floats are filled with zero.
    String NaNs 

    todo docstring
    '''

    dataset[['tot_cur_bal', \
            'tot_coll_amt', \
            'total_rev_hi_lim']].fillna(value = 0, inplace = True)


    return dataset


# def spelling_mistakes(dataset):
#     '''
#     todo docstring
#     '''

#     import enchant as en

#     spell_check = en.Dict('en_US')

#     for s in ['emp_title', 'title']:
#         df[]

#     dataset['num_spell_errors'] = 0



if __name__ == '__main__':
    print "Just do this in the jupyter notebook. Don't bother here."
