import pandas as pd
import numpy as np



def clean_injection_well_data_pre16(df,filename):
    df.fillna(np.nan, inplace = True)
    df.columns = [col.lower().replace(' ','_') for col in df.columns]
    df['approval_date'].str.replace('/','-')
    df['zone'].replace(np.nan,'NA', inplace = True)
    df['zone'].str.lower()
    df['zone'].str.replace('/','')
    df['zone'].str.replace('-',',')
    df['zone'].str.replace('&',',')
    df['zone'].str.replace('AND',',')
    df['zone'].str.strip()
    df['zone'].str.replace(' ','_')
    df['approval_date'] = pd.to_datetime(df['approval_date'],errors='raise')
    df['year'] = [x.year for x in df['approval_date']]
    df['well_count'] = 1
    well_simple = df[['api#','year','zone','bbls','psi','well_count']].copy()
    new_columns = ['unique_identifier','year','formation','bbls','psi','well_count']
    well_simple.columns = new_columns
    well_simple.set_index('unique_identifier',inplace= True)
    well_simple = well_simple[(well_simple['year'] >= 1974)].copy()
    # breakpoint()
    well_simple.to_csv(filename)
 
def clean_injection_well_data_post16(df,year,filename):
    df.fillna(np.nan, inplace = True)
    df.columns = [col.lower().replace(' ','_') for col in df.columns]
    df['formationname'].replace(np.nan,'NA',inplace=True)
    df['formationname'].str.lower()
    df['formationname'].str.replace('/',',')
    df['formationname'].str.replace('-',',')
    df['formationname'].str.replace('&',',')
    df['formationname'].str.replace('AND',',')
    df['formationname'].str.strip()
    df['formationname'].str.replace(' ','_')
 
    bbls = df['jan_vol']+ df['feb_vol']+ df['mar_vol']+ df['apr_vol']+  df['may_vol']+ df['jun_vol']+ df['jul_vol']+ df['aug_vol']+ df['sep_vol']+ df['oct_vol']+ df['nov_vol']+ df['dec_vol']
    df['bbls'] = bbls
    psi = df['jan_psi']+ df['feb_psi']+ df['mar_psi']+ df['apr_psi']+  df['may_psi']+ df['jun_psi']+ df['jul_psi']+ df['aug_psi']+ df['sep_psi']+ df['oct_psi']+ df['nov_psi']+ df['dec_psi']
    df['psi'] = psi
    df['well_count'] = 1
    df['year'] = year
    well_simple = df[['api','year','formationname','bbls','psi','well_count']].copy()
    new_columns = ['unique_identifier','year','formation','bbls','psi','well_count']
    well_simple.columns = new_columns
    well_simple.set_index('unique_identifier',inplace= True)
    well_simple.to_csv(filename)

def clean_eq_data(df,filename):
    df.fillna(np.nan, inplace = True)
    df[['date','time']] = df.time.str.split("T",expand=True) 
    df['date'] = pd.to_datetime(df['date'],errors='raise')
    df['year'] = [x.year for x in df['date']]
    mask_place = (df['place'] == 'Oklahoma')
    ok_eq = df[mask_place]
    ok_eq_date = ok_eq[(ok_eq['date'] >= '2016-01-01')].copy()
    eq_simple = ok_eq_date[['id','year','latitude','longitude','depth','mag']].copy()
    new_columns = ['unique_identifier','year','latitude','longitude','depth','magnitude']
    eq_simple.columns = new_columns
    eq_simple.set_index('unique_identifier', inplace = True)
    # breakpoint()
    eq_simple.to_csv(filename)

if __name__ == '__main__':

    wells_pre16 = pd.read_csv('../data/InjectionWells.csv')
    wells_16 = pd.read_csv('../data/2016_1012A_UIC_volumes.csv')
    wells_17 = pd.read_csv('../data/2017_UIC_volumes.csv')
    wells_18 = pd.read_csv('../data/2018_UIC_volumes.csv')
    eq_pre16 = pd.read_csv('../data/okQuakes.csv')
    eq_post16 = pd.read_csv('../data/EQ_2017_2020.csv')


    clean_injection_well_data_pre16(wells_pre16,'../data/clean/OK_Wells_tru2015.csv')
    clean_injection_well_data_post16(wells_16, 2016, '../data/clean/OK_Wells_16.csv')
    clean_injection_well_data_post16(wells_17, 2017, '../data/clean/OK_Wells_17.csv')
    clean_injection_well_data_post16(wells_18, 2018, '../data/clean/OK_Wells_18.csv')

    
    clean_eq_data(eq_pre16,'../data/clean/OK_EQ_tru2015.csv')
    clean_eq_data(eq_post16,'../data/clean/OK_EQ_2017tru2018.csv')
    clean_eq_data(eq_pre16,'../data/clean/OK_EQ_2016.csv')

    
   
    
 