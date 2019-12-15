from monte_carlo_tpm_generation import MCTPM
from scenario_generation import SG
import pandas as pd
import numpy as np
import utils_

n_sample = 1000
n_state = 7
temp = MCTPM(n_state, n_sample)
pn, pc = temp.get_transition_probs()
cost = [10, 0, 50, 20, 100, 70, 110]
sc = SG(0.05, pn, pc, 100, cost)
s1, s2, s3  =  sc.get_scenarios()
