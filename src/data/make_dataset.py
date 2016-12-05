# -*- coding: utf-8 -*-
import os

import pandas as pd


def make_clean_dataset(dataset):
    '''
    todo docstring
    '''

    cols_to_keep = ['id', 'member_id', 'loan_amnt', 'funded_amnt', \
    'funded_amnt_inv', 'term', 'int_rate', 'installment', 'grade', \
    'sub_grade', 'emp_title', 'emp_length', 'home_ownership', 'annual_inc', \
    'verification_status', 'issue_d', 'loan_status', 'pymnt_plan', 'url', \
    'purpose', 'title', 'zip_code', 'addr_state', 'dti', 'delinq_2yrs', \
    'earliest_cr_line', 'inq_last_6mths', 'open_acc', 'pub_rec', 'revol_bal', \
    'revol_util', 'total_acc', 'initial_list_status', 'out_prncp', 'out_prncp_inv', \
    'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 'total_rec_int', \
    'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'last_pymnt_d', \
    'last_pymnt_amnt', 'next_pymnt_d', 'last_credit_pull_d', 'collections_12_mths_ex_med', \
    'policy_code', 'application_type', 'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal']

    df = dataset[(dataset['annual_inc'] <= 400000) & \
        (dataset['delinq_2yrs'].isnull() == False) & \
        (dataset['revol_util'] <= 130) & \
        (dataset['collections_12_mths_ex_med'].isnull() == False)].copy()

    continous_cols =  ['loan_amnt','funded_amnt','funded_amnt_inv',\
    'installment','dti','revol_bal']

    for feature_name in continous_cols:
        df[feature_name] = df[feature_name].astype(float)

    return df[cols_to_keep]


def impute_missing(dataset):
    '''
    todo docstring
    '''

    dataset['tot_cur_bal'].fillna(value = 0, inplace = True)
    dataset['tot_coll_amt'].fillna(value = dataset['tot_coll_amt'].mean(), inplace = True)

    return dataset


def spelling_mistakes(dataset):
    '''
    todo docstring
    '''

    import enchant as en

    spell_check = en.Dict('en_US')

    for s in ['emp_title', 'title']:
        df[]

    dataset['num_spell_errors'] = 0



if __name__ == '__main__':
    print "Just do this in the jupyter notebook. Don't bother here."
