#########script to optimise different 5 year data#################

import pandas as pd 
import openpyxl as pxl
import numpy as np 
import statistics as st
from scipy.optimize import minimize, Bounds, LinearConstraint
from datetime import datetime
from math import exp
######################################################################################
def main(number,risk,weight):
    df=pd.read_csv(f"/Users/tejasvichabbra/Desktop/Portfolio_Analysis/data/combined{number}.csv")
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    df=df[df['SERIES']=='EQ']
    companies=df['SYMBOL'].unique()
    final_day=pd.read_csv('finalday.csv')
    final_day=final_day[final_day['SERIES']=='EQ']
    final_day_companies=final_day['SYMBOL'].unique()
    path_first_day=f"/Users/tejasvichabbra/Desktop/Portfolio_Analysis/firstday_data1/firstday{number}.csv"
    first_day=pd.read_csv(path_first_day)
    first_day=first_day[first_day['SERIES']=='EQ']
    first_day_companies=first_day['SYMBOL'].unique()
    final_day_companies = set(final_day_companies).intersection(first_day_companies)
    df.sort_values(by=['SYMBOL','TIMESTAMP'],inplace=True)
    companies=df['SYMBOL'].unique()
    companies1=[]
    for x in companies:
        for j in final_day_companies:
            if (x==j):
                companies1.append(x)
                break
    len(companies1)
    companies=companies1
    
    ds=[]
    for i in companies:
        ds.append(df[df['SYMBOL']==i])
    index=0
    final_companies=[]
    final_prices=[]
    
    max_len=len(ds[0])
    for i in ds:
        if (len(i)>max_len):
            max_len=len(i)
    for i in ds: 
        if (len(i)==max_len):
            final_prices.append(i)
            final_companies.append(companies[index])
        index=index+1
        
################### CLEANING DONE ########################

################### CALCULATION OF MEAN/STDEV ##############
    returns_list=[]
    mean_list=[]
    stddev_list=[]
    for i in range(0,len(final_companies)): 
        prices=final_prices[i]['CLOSE']
        prices=prices.to_numpy()
        returns=np.zeros(len(prices)-1)
        j=-1
        for h in range((len(prices)-1),0,-1):
            j=j+1
            returns[j]=(prices[h]-prices[h-1])/prices[h-1]
        
        returns_list.append(returns)
        mean_list.append(returns.mean())
        stddev_list.append(returns.std())    
    
#################### CALCULATION DONE ###########################

#################### CALCULATION OF CORR/COV ####################
    
    corr_matrix=np.zeros(len(returns_list)**2).reshape(len(returns_list),len(returns_list))
    cov_matrix=np.zeros(len(returns_list)**2).reshape(len(returns_list),len(returns_list))

    for x in range(0,len(returns_list)):
        i=returns_list[x]
        for y in range(0,len(returns_list)):
            j=returns_list[y]
            corr_temp=np.corrcoef(i, j)
            corr=corr_temp[0][1]
            cov=corr*stddev_list[x]*stddev_list[y]
            corr_matrix[x][y]=corr
            cov_matrix[x][y]=cov

#################### CALCULATION DONE ##############################

    final_just_prices=[]
    for i in final_prices:
        final_just_prices.append(i['CLOSE'])

################### ALL VARIABLES CALCULATED #######################
        ##### ALL THE VARIABLES CALCULATED TILL NOW ######

# print(len(final_just_prices))# companywise prices arrays 
# print(returns_list)# comapnywise returns arrays 
# print(mean_list)# company wise mean returns 
# print(stddev_list)# companywise stddev of returns
# print(corr_matrix)# correlation matrix 
# print(cov_matrix)#covariance matrix 

#################### OPTIMISATION #################################
    
    W = np.ones((len(returns_list),1))*(1.0/len(returns_list))
    mean_list=np.array(mean_list)
    def optimize(func, W, exp_ret, cov, target_risk):
        opt_bounds = Bounds(0, 1)
        opt_constraints = ({'type': 'eq','fun': lambda W: weight - np.sum(W)},{'type': 'eq','fun': lambda W: target_risk - (W.T@cov@W)**0.5})
        optimal_weights = minimize(func, W, args=(exp_ret, cov),method='SLSQP',bounds=opt_bounds,constraints=opt_constraints)
        return optimal_weights['x']
    def ret_return(W, exp_ret, cov):
        return -((W.T@exp_ret))
    x = optimize(ret_return,W,mean_list, cov_matrix, target_risk=risk)
    
################### OPTIMISATION COMPLETE ########################

################### RESULTS #######################################
    expected_return=mean_list.T@x
    expected_risk=(x.T@cov_matrix)@x
    ctr=0
    indi_final_returns=[]
    path_first_day=f"/Users/tejasvichabbra/Desktop/Portfolio_Analysis/firstday_data1/firstday{number}.csv"
    first_day=pd.read_csv(path_first_day)
    first_day=first_day[first_day['SERIES']=='EQ']

    for i in range(0,len(final_companies)):
        tmp=final_day[final_day['SYMBOL']==final_companies[i]]
        end=float(tmp['CLOSE'])
        tmp1=first_day[first_day['SYMBOL']==final_companies[i]]
        start=float(tmp1['CLOSE'])
        ctr+=1
        indi_final_returns.append(end-start)
    individual_returns=np.array(indi_final_returns)
    individual_returns=individual_returns.reshape(len(indi_final_returns),1)
    x=x.reshape(len(x),1)
    final_earnings=x.T@individual_returns
    return [expected_return,expected_risk**0.5,float(final_earnings)]
######################################################################

####################### EXCEL WRITER ################################
col_names=['Expected Return' ,'Expected risk' ,'Final Earnings']

fin_df=pd.DataFrame(columns=col_names)
for x in np.arange(0.01,0.21,0.01):
    weight=1
    for i in range (1,26):
        final_dic=main(i,x,weight)
        a_series = pd.Series(final_dic, index = fin_df.columns)
        fin_df = fin_df.append(a_series, ignore_index=True)
        weight*=exp(0.0225*0.25)
        print(fin_df)

fin_df.to_excel(f"final_output.xlsx")