#fitting eheating low temp and high temp fitting with 1e-7A photodiode current break point
#data from 2024-03-15-1450
#fitted temperature check
#SS paddle position 2 and #123 on position 3 based fitting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d
import os
import csv
import loop_finding_breakpoint_for_eheating_fitting as LL

fig,ax=plt.subplots(2,1)
ax1=ax[0].twinx()
ax[0].set_xlabel('SS TC temp/C')
ax[0].set_ylabel('Photodiode current/A')
ax1.set_ylabel('Fitted temp error/C')
#PDcurrent from reading from file
T_heat=[23,56,119,222,308,403,479,521,557,601,708,809,892,964,996,1078]
T_cool=[898,790,698,620,580,520,489,433,397,344,296,188]
T=T_heat+T_cool
PDcurrent_heat=[1e-17,3.4682895444504425e-10,1.2644078006829318e-09,2.9709426030422037e-09,4.359284044852529e-09,
                1.3305852419875919e-08,4.081208615502874e-08,7.459379958163481e-08,1.2418077233178337e-07,
                2.1855220211364212e-07,7.203491918517102e-07,1.8430639556754613e-06,3.6417598039406585e-06,
                6.164129899843829e-06,7.570449270133395e-06,1.3492575817508623e-05]
PDcurrent_cool=[3.584089199648588e-06,1.4481013295153389e-06,5.805486011922767e-07,2.3782062896771095e-07,
                1.40902514544905e-07,6.167101673781872e-08,3.983319274425412e-08,1.6646508171902497e-08,
                9.9996171343264e-09,4.942312781253122e-09,2.435297297154193e-09,6.547646869137225e-10]
PDcurrent=PDcurrent_heat+PDcurrent_cool


breakpoint=[2.435297297154193e-09, 4.5e-09, 2e-07]
PDcurrent_fraction,T_fraction=LL.fraction_generate(PDcurrent,T,breakpoint)
fitted_functions={}
T_differences={}
T_Errors={}
poly_Ts={}
f_catalogs={}
PDcurrent,T=LL.sort_lists(PDcurrent,T)
for (PDcurrent_key_list,PDcurrent_list),(T_key_list,T_list) in zip(PDcurrent_fraction.items(), T_fraction.items()):
    sec_fitted_function,T_difference,T_error,poly_T,f_catalog=LL.sec_fitting_generate(PDcurrent_list,T_list)
    fitted_functions[PDcurrent_key_list]=sec_fitted_function
    T_differences[PDcurrent_key_list]=T_difference
    T_Errors[PDcurrent_key_list]=T_error
    f_catalogs[PDcurrent_key_list]=f_catalog
    #print(poly_T)
    poly_Ts[PDcurrent_key_list]=poly_T

def fitting_region_split(PDcurrent_point):
    for i in range(len(breakpoint)-1):
        if breakpoint[i]<= PDcurrent_point <= breakpoint[i+1]:
            fitt_fun=f_catalogs[f'{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}'](PDcurrent_point)
    if breakpoint[0]>PDcurrent_point:
        fitt_fun=f_catalogs[f' PDcurrent[j]< {breakpoint[0]}'](PDcurrent_point)
    elif PDcurrent_point>breakpoint[-1]:
        fitt_fun=f_catalogs[f'PDcurrent[j]> {breakpoint[-1]}'](PDcurrent_point)
    return fitt_fun


fitted_T=[]
for i in range(len(PDcurrent)):
    fitted_T.append(fitting_region_split(PDcurrent[i]))
#print(T)
#print(fitted_T)
'''def write_polynomial(coefficients):
    degree = len(coefficients) - 1
    terms = []

    for i, coef in enumerate(coefficients):
        if i == 0:
            terms.append(f"{coef:.2e}")
        else:
            terms.append(f"{coef:.2e} * x^{i}")

    polynomial = " + ".join(terms)
    return polynomial
'''



# Define the equation
'''
ax1=ax[0].twinx()
ax[0].plot(T_low,poly_T_low,color='blue',label=f'fitting:{poly_function_low} \n with mse:{mse_low:.2e} \n with temperature rms-error:{np.sqrt(T_error_low):.2f}C')
ax[0].plot(T_high,poly_T_high,color='red',label=f'fitting:{poly_function_high} \n with mse:{mse_high:.2e} \n with temperature rms-error:{np.sqrt(T_error_high):.2f}C')
ax1.scatter(T_low,T_difference_low,marker='^',color='blue',label='error of fiting middle temp')
ax[0].plot(T_llow,poly_T_llow,color='orange',label=f'fitting:{poly_function_llow} \n with mse:{mse_llow:.2e} \n with temperature rms-error:{np.sqrt(T_error_llow):.2f}C')
ax1.scatter(T_llow,T_difference_llow,marker='^',color='orange',label='error of fiting low temp')
ax1.scatter(T_high,T_difference_high,marker='^',color='red',label='error of fiting high temp')
ax[0].scatter(T,PDcurrent)
ax[0].set_xlabel('SS paddle Temperature/C')
ax[0].set_ylabel('Photodiode current/A')
ax1.set_ylabel('fitted errot (TC temp - fitted temp)/C')
ax[0].legend()
ax1.legend(loc='upper right')
plt.show()
  '''    