# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:47:13 2021

@author: jason
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
#import statistics 

# setting decimals 
np.set_printoptions(precision=2, suppress=True)

roll_count = 15000

roll = ['crit','wild','hit','hit','block','blank','blank','failure']

result_list = []

crit_result_list = []

mod_list = []

crit = 0

total_roll_result_list = []

user_input_roll = int(input('How many attack dice should we roll?'))

reroll_q = int(input('How manys attack rerolls do you get?'))

reduce_damage = str(input('Reduce damage by 1 to a minimum of 1? T or F.'))

modok = str(input('Are you attacking MODOK? T or F.'))

modok = modok.lower()
if modok == 't':
    modok = True
else:
    modok = False

reduce_damage = reduce_damage.lower()
if reduce_damage == 't':
    reduce_damage = True
else:
    reduce_damage = False

for n in range(roll_count):
    for i in range(user_input_roll):
        result_list.append(np.random.choice(roll))
    for i in result_list:
        if i == 'crit':
            crit = crit + 1
    #print(result_list)   
    for i in range(crit):
        crit_result_list.append(np.random.choice(roll))
    #print(crit_result_list)
    total_roll = result_list + crit_result_list
    total_roll_result_list.append(total_roll)
    
    result_list = []

    crit_result_list = []

    mod_list = []

    crit = 0

df= pd.DataFrame (total_roll_result_list)

df['possible reroll count'] = df.eq('block').sum(axis=1) + df.eq('blank').sum(axis=1)



reroll_result = []
for value in df['possible reroll count']:
    if value >= 1 and reroll_q >= 1:
        reroll_result.append(np.random.choice(roll))
    else:
        reroll_result.append(None)
        
df['reroll result'] = reroll_result

second_reroll_result = []
for value in df['possible reroll count']:
    if value >= 2 and reroll_q > 1:
       second_reroll_result.append(np.random.choice(roll))
    else:
        second_reroll_result.append(None)
        
df['second reroll result'] = second_reroll_result

if modok == True:
    df['success count'] = df.eq('crit').sum(axis=1) + df.eq('hit').sum(axis=1)
else:
    df['success count'] = df.eq('crit').sum(axis=1) + df.eq('wild').sum(axis=1) + df.eq('hit').sum(axis=1)

describe_success = df['success count'].describe()
df_describe_success = pd.DataFrame(describe_success)

# pareto line not used
df['pareto'] = 100 * df['success count'].cumsum() / df['success count'].sum()

  
pareto = df['success count'].value_counts().reset_index().values
df_pareto = pd.DataFrame(pareto)
df_pareto.rename(columns={0: 'Hits', 1: 'Hits Count'}, inplace=True)
df_pareto = df_pareto.sort_values(by=['Hits'])


## NEXT TASK... make a bar chart showing results

ax = df_pareto.plot.bar(x='Hits',y='Hits Count', rot=0)


####### DEFENSE ROLLS AFTER THIS

d_roll = ['crit', 'wild', 'hit', 'hit', 'block', 'blank', 'blank', 'failure']

d_result_list = []

d_crit_result_list = []

d_mod_list = []

d_crit = 0

d_total_roll_result_list = []

d_user_input_roll = int(input('How many defense dice should we roll?'))

d_reroll_q = int(input('How many defense rerolls do you get?'))

for n in range(roll_count):
    for i in range(d_user_input_roll):
        d_result_list.append(np.random.choice(d_roll))
    for i in d_result_list:
        if i == 'crit':
            d_crit = d_crit + 1
    # print(result_list)   
    for i in range(d_crit):
        d_crit_result_list.append(np.random.choice(d_roll))
    # print(crit_result_list)
    d_total_roll = d_result_list + d_crit_result_list
    d_total_roll_result_list.append(d_total_roll)

    d_result_list = []

    d_crit_result_list = []

    d_mod_list = []

    d_crit = 0

d_df = pd.DataFrame(d_total_roll_result_list)

d_df['possible reroll count'] = d_df.eq('block').sum(axis=1) + d_df.eq('blank').sum(axis=1)

d_reroll_result = []
for value in d_df['possible reroll count']:
    if value >= 1 and d_reroll_q >= 1:
        d_reroll_result.append(np.random.choice(d_roll))
    else:
        d_reroll_result.append(None)

d_df['reroll result'] = d_reroll_result

d_second_reroll_result = []
for value in d_df['possible reroll count']:
    if value >= 2 and d_reroll_q > 1:
        d_second_reroll_result.append(np.random.choice(d_roll))
    else:
        d_second_reroll_result.append(None)

d_df['second reroll result'] = d_second_reroll_result


d_df['success count'] = d_df.eq('crit').sum(axis=1) + d_df.eq('wild').sum(axis=1) + d_df.eq('block').sum(axis=1)

d_describe_success = d_df['success count'].describe()
d_df_describe_success = pd.DataFrame(d_describe_success)

# pareto line not used
d_df['pareto'] = 100 * d_df['success count'].cumsum() / d_df['success count'].sum()

d_pareto = d_df['success count'].value_counts().reset_index().values
d_df_pareto = pd.DataFrame(d_pareto)
d_df_pareto.rename(columns={0: 'Blocks', 1: 'Blocks Count'}, inplace=True)
d_df_pareto = d_df_pareto.sort_values(by=['Blocks'])

## NEXT TASK... make a bar chart showing results

d_ax = d_df_pareto.plot.bar(x='Blocks', y='Blocks Count', rot=0)


# combine each instance of a roll off

final_comparison = pd.concat([df['success count'], d_df['success count']], axis=1, keys=['hits', 'blocks'])
final_comparison['hits through'] = final_comparison['hits'] - final_comparison['blocks']

# change all negatives to 0
final_comparison['hits through'][final_comparison['hits through'] < 0] = 0

# subtract 1 from any greater than 1
if reduce_damage == True:
    final_comparison['hits through'][final_comparison['hits through'] > 1] = [final_comparison['hits through'] - 1]

    

final_comparison_pareto = final_comparison['hits through'].value_counts().reset_index().values
final_comparison_pareto = pd.DataFrame(final_comparison_pareto)
final_comparison_pareto.rename(columns={0: 'hits through', 1: 'hits through count'}, inplace=True)
final_comparison_pareto = final_comparison_pareto.sort_values(by=['hits through'])

final_comparison_pareto_ax = final_comparison_pareto.plot.bar(x='hits through', y='hits through count', rot=0)