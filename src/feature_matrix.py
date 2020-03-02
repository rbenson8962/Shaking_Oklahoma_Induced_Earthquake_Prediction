import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def one_hot_form(form_name, form_value):
    if form_name == form_value:
        return 1
    else:
        return 0

def one_hot_multi(multiples, well_value):
    if well_value in multiples:
        return 1
    else:
        return 0

def one_hot_formations(df,filename):
    formations = df['formation'].unique()
    multiples = []
    for form in formations:
        try:
            if form.find(',') == -1:
                col_name = 'in_' + form
                df[col_name] = df.apply(lambda row: one_hot_form(form, row['formation']), axis = 1)
            else:
                multiples.append(form)
        except AttributeError as e:
            print('formation not string')
            print(e)

    df['is_multiple_formations'] = df.apply(lambda row: one_hot_multi(multiples, row['formation']), axis = 1)
    df.to_csv(filename)


def build_matrix(df, filename):
   
    to_drop = ['unique_identifier','formation']
    df.drop(to_drop,inplace = True, axis = 1)

    agg_dict = {'well_count':'sum','psi':'mean'}
    cols = [c for c in df.columns if c not in ['year','psi','bbls','well_count']]
    for c in cols:
        col_name = 'BBLS_' + c
        #breakpoint()
        df[col_name] = df[c] * df['bbls']
        agg_dict[col_name] = 'sum'
    
    out = df.groupby('year').agg(agg_dict).copy()
    out.to_csv(filename)

def cum_sum_matrix(df,filename):
    col_save = ['year','well_count','psi']
    col = [c for c in df.columns if c not in col_save]
    for c in col:
        df[c] = df[c].cumsum()
    df.to_csv(filename)

if __name__ == "__main__":
    
    wells_pre16 = pd.read_csv('../data/clean/OK_Wells_tru2015.csv')
    wells_16 = pd.read_csv('../data/clean/OK_Wells_16.csv')
    wells_17 = pd.read_csv('../data/clean/OK_Wells_17.csv')
    wells_18 = pd.read_csv('../data/clean/OK_Wells_18.csv')
    eq_pre16= pd.read_csv('../data/clean/OK_EQ_2009tru2015.csv')
    eq_16 = pd.read_csv('../data/clean/OK_EQ_2016.csv')
    eq_17_18 = pd.read_csv('../data/clean/OK_EQ_2017tru2018.csv')
    
## Create simple x feature matrix with sum_bbls/year and num_eq/year
    frames_simple = [wells_pre16, wells_16, wells_17, wells_18]
    X_simple = pd.concat(frames_simple, sort=True)
    X_simple = X_simple[['year','bbls','psi']]
    X_simple = X_simple.groupby('year').agg({'bbls':'sum','psi':'mean'})
    # X_simple.set_index('year', inplace = True)
    year = ['2001','1978','1977']
    m0 = X_simple.index.isin(year)
    X_simple = X_simple[~m0]

    #Cumulative sum all bbls for each year
    col_save = ['psi']
    col = [c for c in X_simple.columns if c not in col_save]
    for c in col:
        X_simple[c] = X_simple[c].cumsum()
    X_simple.to_csv('../data/clean/simple_x_fm')

    #Build simple y feature matrix 
    frames_eq = [eq_pre16, eq_16, eq_17_18]
    y_simple = pd.concat(frames_eq, sort = True).copy()
    y_simple= y_simple[['year']]
    y_simple['num_eq'] = 1
    y_simple = y_simple.groupby('year').agg({'num_eq':'sum'})
    y_simple.to_csv('../data/clean/simple_y_fm')

    # Create one data set with wells from 1974 - 2018
    frames = [wells_pre16, wells_16, wells_17, wells_18]
    X_wells = pd.concat(frames, sort=True).copy()
    X_wells.sort_values('year')
    X_wells= X_wells.set_index('unique_identifier')
    X_wells = X_wells[['year','well_count','psi','bbls','formation']]
    X_wells['formation'].astype('str')
  
## Build feature matrix will all formations included 
    # One hot encode all injected formations, save to new csv, and build data set 
    one_hot_formations(X_wells,'../data/clean/X_wells.csv')
    build_matrix(X_wells_data,'../data/clean/feature_matrix_X_final.csv')
    cum_sum_matrix(X_fm_final,'../data/clean/feature_matrix_X_final_1.csv')

    # Build y_feature_matrix data set 
    frames_eq = [eq_pre16, eq_16, eq_17_18]
    y_fm = pd.concat(frames_eq, sort = True).copy()
    y_fm = y_fm.reset_index()
    y_fm= y_fm[['year']]
    y_fm['num_eq'] = 1
    y_fm = y_fm.groupby('year').count().reset_index()
    y_fm.set_index('year')
    y_fm.to_csv('../data/clean/feature_matrix_y_final.csv')

    

 

    

 
        
        
