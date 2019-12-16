from monte_carlo_tpm_generation import MCTPM
from scenario_generation import SG
import xlsxwriter
import pandas as pd
import numpy as np
import utils_

n_sample = 1000
n_state = 7
n_scenario = 50
dev = 0.9
temp = MCTPM(n_state, n_sample)
pn, pc = temp.get_transition_probs()
cost = [10, 0, 50, 20, 100, 70, 110]
sc = SG(dev, pn, pc, n_scenario, cost)
s1, s2, s3  =  sc.get_scenarios()

writer_n = pd.ExcelWriter('mc_ns.xlsx', engine='xlsxwriter')
writer_c = pd.ExcelWriter('mc_cs.xlsx', engine='xlsxwriter')
writer_cost = pd.ExcelWriter('mc_costs.xlsx', engine='xlsxwriter')
for i in range(n_scenario):
    df_n = pd.DataFrame(s1[i])
    df_c = pd.DataFrame(s2[i])
    df_cost = pd.DataFrame(s3[i])
    name = 'Sheet'+str(i)
    df_n.to_excel(writer_n, sheet_name=name, header=None, index=None)
    df_c.to_excel(writer_c, sheet_name=name, header=None, index=None)
    df_cost.to_excel(writer_cost, sheet_name=name, header=None, index=None)
writer_n.save()
writer_c.save()
writer_cost.save()
