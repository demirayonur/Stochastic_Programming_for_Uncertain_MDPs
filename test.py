from monte_carlo_tpm_generation import MCTPM
import pandas as pd
import numpy as np
import utils_


n_sample = 1000
n_state = 7
temp = MCTPM(n_state, n_sample)
pn, pc = temp.get_samples()
pn = sum(pn) / n_sample
pc = sum(pc) / n_sample

utils_.mc_normalization(pn)
utils_.mc_normalization(pc)

for i in pc:
    print(np.sum(i))

for i in pn:
    print(np.sum(i))

pn_df = pd.DataFrame(pn)
pc_df = pd.DataFrame(pc)

pn_df.to_csv('normal_care_transitions.csv')
pc_df.to_csv('complex_care_transitions.csv')
