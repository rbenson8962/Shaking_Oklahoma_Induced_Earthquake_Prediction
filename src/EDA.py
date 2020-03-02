import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns



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
    
# def simple_plot(x,y1,y2,y3, xlabel, ylabel,title, filename):
#     fig, ax = plt.subplots()
#     plt.plot( 'x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
#     plt.plot( 'x', 'y2', data=df, marker='', color='olive', linewidth=2)
#     plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
#     plt.legend()


#     ax.set(xlabel = xlabel, ylabel = ylabel, title = title)
#     ax.grid()
#     plt.tight_layout()
#     fig.savefig(filename)
#     plt.show()




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
    # plt.ylabel("")
    # plt.xlabel("")
    plt.legend()
    plt.grid()
    plt.savefig('../images/Earthquake_count_mag_depth.png')
    plt.show()

## Well Occurance, bbls, psi over time
    fig, ax = plt.subplots()
    plt.plot(all_data.index,all_data['well_count'], '-', label = 'Number of Earthquakes')
    plt.plot(all_data.index,all_data['bbls'], '-', label= 'Cumulative BBLS')
    plt.plot(all_data.index,all_data['psi'], '-', label= 'Average PSI')
    plt.yscale('log')
    plt.title("Well Counts, BBLS, and Average PSI Over Time")
    # plt.ylabel("")
    # plt.xlabel("")
    plt.legend()
    plt.grid()
    plt.savefig('../images/Well_count_bbls_psi.png')
    plt.show()

## Figures for EDA 




    ## Build df for mean bbls and psi for wells for each month in data set (binned by year/month)

    # well_bbl_psi = wells[['approval_date','bbls','psi']].copy()

    # well_bbl_psi['year'] = [x.year for x in well_bbl_psi['approval_date']]
    # well_bbl_psi['month'] = [x.month for x in well_bbl_psi['approval_date']]
    
    # bbl_psi = well_bbl_psi.groupby(['year', 'month']).agg({'bbls': sum ,'psi':'mean'}).reset_index().copy()
    # bbl_psi.fillna(0,inplace = True)

    # bbl_psi['date']= pd.to_datetime([f'{y}-{m}-01' for y, m in zip(bbl_psi.year, bbl_psi.month)])
    # bbl_psi['date']= pd.to_datetime(bbl_psi['date'], format="%Y%m") + MonthEnd(1)

    # bbl_psi.drop('year', axis=1, inplace = True)
    # bbl_psi.drop('month', axis=1, inplace = True)

    # bbl_psi['date']= pd.DatetimeIndex(bbl_psi['date'])
    # bbl_psi.set_index('date', inplace = True)

    # # bbl_psi.plot.line()
    # # plt.savefig('../images/well_bbl_psi_binned_by_month.png')

    # ## Figures for EDA 

    # fig, ax = plt.subplots(3,2, figsize = (10,10))
    # ax[0,0].plot(well_eq_by_month.index, well_eq_by_month['num_wells/month'])
    # ax[0,0].set_title('Number of Wells per Month', loc = 'center')
    # ax[0,1].plot(well_eq_by_month.index, well_eq_by_month['num_eq/month'])
    # ax[0,1].set_title('Number of Earthquakes per Month', loc = 'center')
    # ax[1,0].plot(bbl_psi.index, bbl_psi['bbls'])
    # ax[1,0].set_title('Barrels Injected per Month', loc = 'center')
    # ax[1,1].plot(bbl_psi.index, bbl_psi['psi'])
    # ax[1,1].set_title('Average Injection PSI per Month', loc = 'center')
    # ax[2,0].plot(mag_depth.index, mag_depth['epicenter_depth'])
    # ax[2,0].set_title('Average Earthquake Epicenter Depth', loc = 'center')
    # ax[2,1].plot(mag_depth.index, mag_depth['magnitude'])
    # ax[2,1].set_title('Average Earthquake Magnitude', loc = 'center')
    # plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    # plt.savefig('../images/eda_fig1.png')


    # ## Merging dataframes for count of well/earthquakes, mean earthquake magnitude and epicenter depth, and sum of well bbls pumped and mean psi to create dataframe for predictive modeling 

    # count_mag_depth = well_eq_by_month.merge(mag_depth, how='outer', left_index=True, right_index=True)

    # well_eq_all = count_mag_depth.merge(bbl_psi, how='outer', left_index=True, right_index=True)
    # new_columns= ['count_wells','count_eq','avg_epicenter_depth','avg_magnitude','sum_bbls_injected','avg_injection_psi']

    # well_eq_all.columns = new_columns

    # well_eq_all.to_csv('../data/df_for_model.csv')

    # pre_2012 = well_eq_all[(well_eq_all.index < '2010-01-01')]
    # post_2012 = well_eq_all[(well_eq_all.index > '2010-01-01')]

    # scatter_matrix(pre_2012,'../images/eda_scatter_pre_2010.png')
    
    # scatter_matrix(post_2012,'../images/eda_scatter_post_2010.png')

