import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class MDP(object):

    def __init__(self, n_state, n_action, discount_factor, cost):

        self.n_state = n_state
        self.n_action = n_action
        self.gamma = discount_factor
        self.cost = cost  # cost vector

        self.P = np.empty(shape=(self.n_state, self.n_action, self.n_state))  # 3D transition probability tensor

        self.V = np.zeros(shape=(self.n_state-1))
        self.policy = {}

    def create_P(self):

        mc_n = pd.read_excel('normal_care_transitions.xlsx', header=None)
        mc_c = pd.read_excel('complex_care_transitions.xlsx', header=None)

        self.P[:, 0, :] = mc_n
        self.P[:, 1, :] = mc_c

    def value_iteration(self):

        # Iterate until convergence
        count = 0
        while True:
            delta = 0
            for state in range(self.n_state - 1):
                old_state_value = self.V[state]
                self.V[state] = self.cost[state] + self.gamma * min(
                    [np.sum(self.P[state, action,:-1] * self.V[:]) + self.P[state, action, self.n_state - 1] *self.cost[-1]
                     for action in range(self.n_action)])
                delta = max(delta, abs(self.V[state] - old_state_value))
            if delta < 1e-18:
                break
            count += 1
            print('iteration number: '+ str(count))
        # Extract the optimal policy

        for state in range(self.n_state - 1):
            self.policy[state] = np.argmin(np.array([np.sum(self.P[state, action,:-1] * self.V[:]) + self.P[state, action, -1] * self.cost[-1]
                                                     for action in range(self.n_action)]))

    def plot_policy(self):

        states = list(range(self.n_state - 1))
        actions = list(range(self.n_action))

        plt.figure(figsize=(18, 5))
        plt.plot(states, [self.policy[state] for state in states], c='purple')
        plt.xlabel('states')
        plt.ylabel('actions')
        plt.xticks(np.arange(min(states), max(states) + 1, 1.0))
        plt.yticks(np.arange(min(actions), max(actions) + 1, 1.0))
        plt.title('Optimal Policy After Value Iteration')
        plt.grid()
        plt.show()