import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# EXTRACT DATA
import pylab as pl

file = 'analysis1.xlsx'
df = pd.read_excel(file, index_col='Hours')
# df['electricity demand'].plot(figsize=(20, 10))

df_electricity_demand = df['electricity demand']  # this is in type series
df_electricity_demand = df[['electricity demand']]  # double brackets changes it to Dataframe
df_electricity_demand.sort_values(by='electricity demand', ascending=False, inplace=True)
df_electricity_demand.index = np.arange(1, 2851)
print(df_electricity_demand.min())  # shows that at every instance of time the electricity
# demand is above 4015.5 (MW)

# PLOTTING
df_electricity_demand.plot()
plt.title('Load duration curve')
plt.ylabel('MW')
plt.xlabel('Hours')
# plt.show()
"""
through the load duration curve, we can see the duration of time for which the
electricity demand is greater than or equal to a specific value.
"""
# print(df_electricity_demand)

# RESIDUAL LOAD DURATION CURVE
df['residual load'] = df['electricity demand'] - df['wind generation']
df_residual_demand = df[['residual load']]
df_residual_demand.sort_values(by='residual load', ascending=False, inplace=True)
df_residual_demand.index = np.arange(1, 2851)
print(df_residual_demand)

# PLOT RESIDUAL DEMAND
df_residual_demand.plot()
plt.title('Residual load duration curve')
plt.ylabel('MW')
plt.xlabel('Hours')

"""
through the residual load duration curve, we can see the duration of time for which the
residual electricity demand is greater than or equal to a specific value.
"""
# PLOTTING BOTH CURVES TOGETHER
fig, ax = plt.subplots()

df_electricity_demand.plot(ax=ax)
df_residual_demand.plot(ax=ax)

df_demand = df_electricity_demand.join(df_residual_demand)
df_demand['load_net_net_by_wind_generation'] = df_demand['electricity demand'] - df_demand['residual load']
print(df_demand)

# PLOTTING df_demand
plt.rcParams['font.size'] = 16
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7), sharey=True)

plt.subplots_adjust(wspace=0.1)
fig.suptitle('Residual load duration curves')
df_demand[['electricity demand', 'residual load']].plot(ax=ax1, color=['cornflowerblue', 'darkorange'])
df_demand[['electricity demand', 'residual load']].plot(ax=ax2, color=['cornflowerblue', 'darkorange'],
                                                        kind='area', stacked=True)

"""
one common mistake that is usually made us that we find the duration curve for wind generation, and
plot it on top of the load duration curve for the residual demand, aiming to produce the 
load duration curve for the initial demand. this is not correct because summing up the duration curve
for the residual load with the duration curve for the wind generation does not produce the duration
curve for the initial demand and is proven with code below. If we sum up this 2 duration curves, it 
would imply that the peak residual demand happens simultaneously with the peak value for the wind
generation.
"""
# PROOF
df_wind_generation = df[['wind generation']]
df_wind_generation.sort_values(by='wind generation', ascending=False, inplace=True)
df_wind_generation.index = np.arange(1, 2851)
# print(df_wind_generation)
df_demand2 = df_residual_demand.join(df_wind_generation)

df_demand3 = df[['residual load', 'wind generation']]
df_demand3.sort_values(by='residual load', ascending=False, inplace=True)
df_demand3.index = np.arange(1, 2851)

# PLOTTING
df_demand2.plot(kind='area', stacked=True)
fig, ax = plt.subplots()
df_demand3.plot(ax=ax, kind='area', stacked=True)
plt.ylabel('MW')
plt.xlabel('Hours')
plt.legend(labels=['Dispatch-able generators', 'wind generators'], loc='upper right', fontsize=10)

# plt.show()

