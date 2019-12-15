import numpy as np
import utils_
import random


class SG(object):

    def __init__(self, dev, mc_n, mc_c, n_scenario, cost):

        self.dev = dev
        self.mc_n = mc_n
        self.mc_c = mc_c
        self.n_state = self.mc_c.shape[0]
        self.n_scenario = n_scenario
        self.cost = cost

    def get_one_scenario(self):

        s_n = np.zeros(shape=(self.n_state, self.n_state))
        s_c = np.zeros(shape=(self.n_state, self.n_state))
        s_cost = np.zeros(shape=self.n_state)

        for i in range(self.n_state):
            low_cost = self.cost[i] * (1 - self.dev)
            up_cost = self.cost[i] * (1 + self.dev)
            temp = random.uniform(low_cost, up_cost)
            s_cost[i] = max(0, temp)  # no negative cost

            for j in range(self.n_state):
                low_n = self.mc_n[i, j] * (1 - self.dev)
                up_n = self.mc_n[i, j] * (1 + self.dev)
                low_c = self.mc_c[i, j] * (1 - self.dev)
                up_c = self.mc_c[i, j] * (1 + self.dev)
                s_n[i, j] = random.uniform(low_n, up_n)
                s_c[i, j] = random.uniform(low_c, up_c)

        utils_.mc_normalization(s_n)
        utils_.mc_normalization(s_c)

        return s_n, s_c, s_cost

    def get_scenarios(self):

        ls_n, ls_c , ls_cost= [], [], []
        for i in range(self.n_scenario):
            s1, s2, s3 = self.get_one_scenario()
            ls_n.append(s1)
            ls_c.append(s2)
            ls_cost.append(s3)
            print('scenario: '+str(i))
        return ls_n, ls_c, ls_cost
