import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt


def scatter_matrix(df,filename):
    scatter_matrix = pd.plotting.scatter_matrix(
        df,
        figsize  = [20, 15],
        marker   = ".",
        s        = 500,
        diagonal='kde'
    )
    for ax in scatter_matrix.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 18, rotation = 0)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 18, rotation = 90)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.tick_params(axis='both', which='minor', labelsize=12)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(filename)
    
if __name__ == '__main__':
    
    wells_pre16 = pd.read_csv('../data/clean/OK_Wells_tru2015.csv')
    wells_16 = pd.read_csv('../data/clean/OK_Wells_16.csv')
    wells_17 = pd.read_csv('../data/clean/OK_Wells_17.csv')
    wells_18 = pd.read_csv('../data/clean/OK_Wells_18.csv')
    eq_pre16= pd.read_csv('../data/clean/OK_EQ_2009tru2015.csv')
    eq_16 = pd.read_csv('../data/clean/OK_EQ_2016.csv')
    eq_17_18 = pd.read_csv('../data/clean/OK_EQ_2017tru2018.csv')
          
## Merge wells_df & ok_eq 
    frames = [wells_pre16, wells_16, wells_17, wells_18]
    wells = pd.concat(frames, sort=True).copy()
    wells = wells[['year','well_count','psi','bbls']]
    wells = wells.groupby(['year']).agg({'well_count':sum, 'bbls': sum ,'psi':'mean'}).reset_index()
    wells = wells.set_index('year')
    wells['bbls'] = wells['bbls'].cumsum()
    year = ['2001','1978','1977']
    m0 = wells.index.isin(year)
    wells = wells[~m0]
    frames_eq = [eq_pre16, eq_16, eq_17_18]
    eq= pd.concat(frames_eq, sort = True).copy()
    eq = eq.reset_index()
    eq_count= eq[['year']]
    eq_count['num_eq'] = 1
    eq_count = eq_count.groupby('year').agg({'num_eq':'sum'})
    
    # eq_count = eq_count.set_index('year')
    eq_mag_depth = eq[['year','magnitude','depth']].groupby('year').agg({'depth':'mean','magnitude': 'mean'})

    # eq_mag_depth.set_index('year')
    all_eq = eq_count.merge(eq_mag_depth, how ='outer', left_index = True, right_index = True)
    all_data = wells.merge(all_eq, how ='outer', left_index = True, right_index = True)

# PLOTS
## Earthquake occurance, average depth, average magnitude over time
    fig, ax = plt.subplots()
    plt.plot(all_data.index,all_data['num_eq'], '-', label = 'Number of Earthquakes')
    plt.plot(all_data.index,all_data['magnitude'], '-', label= 'Average Magnitude')
    plt.plot(all_data.index,all_data['depth'], '-', label= 'Average Depth')
    plt.yscale('log')
    plt.title("Earthquake Occurance, Depth, and Magnitude Over Time")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('../images/Earthquake_count_mag_depth.png')
    plt.show()

## Well Occurance, bbls, psi over time
    fig, ax = plt.subplots()
    plt.plot(all_data.index,all_data['well_count'], '-', label = 'Number of Earthquakes')
    plt.plot(all_data.index,all_data['bbls'], '-', label= 'Cumulative BBLS')
    plt.plot(all_data.index,all_data['psi'], '-', label= 'Average PSI')
    plt.yscale('log')
    plt.title("Well Counts, BBLS, and Average PSI Over Time")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('../images/Well_count_bbls_psi.png')
    plt.show()

