import numpy as np
import pulp as opt
import random
import utils_


class RTPM(object):

    def __init__(self, seed, n_state):

        """
        Construction method for the MCTPM class

        :param seed: Integer, determines the random seed
        :param n_state: Integer, identifies the number of states in the MDP model
        """

        random.seed(seed)  # Random Seed
        self.n_state = n_state  # Number of states
        self.opt_model = opt.LpProblem('Monte Carlo TPM Generation', opt.LpMaximize)  # Define optimization model

        # Decision Variables:
        # ------------------
        # 1) A Markov Chain for the Normal Care Action
        # 2) A Markov Chain for the Complex Care Action

        self.mc_n = opt.LpVariable.dicts('P1',
                                         [(i, j) for i in range(self.n_state) for j in range(self.n_state)],
                                         0, 1,
                                         opt.LpContinuous
                                         )  # MC for Normal Care, Each element in it is a continuous random variable

        self.mc_c = opt.LpVariable.dicts('P2',
                                         [(i, j) for i in range(self.n_state) for j in range(self.n_state)],
                                         0, 1,
                                         opt.LpContinuous
                                         )  # MC for Complex Care, Each element in it is a continuous random variable

        # Create Random Coefficients
        # --------------------------
        # With the help of this we will be generating multiple random TPM obeying expert hierarchies

        # Dictionary Forms
        self.c_n = {(i, j): random.random() for i in range(self.n_state) for j in range(self.n_state)}
        self.c_c = {(i, j): random.random() for i in range(self.n_state) for j in range(self.n_state)}

    def define_objective_function(self):

        """
        This method introduces the objective function to the optimization model developed
        :return: None
        """

        # First include the prod-sum for the normal care markov chain
        self.opt_model += (opt.lpSum(self.c_n[(i, j)] * self.mc_n[(i, j)]
                                    for i in range(self.n_state) for j in range(self.n_state)) +
                           opt.lpSum(self.c_c[(i, j)] * self.mc_c[(i, j)]
                                     for i in range(self.n_state) for j in range(self.n_state)))

    def getting_worse_constraints(self):

        """
        This method includes the getting-worse constraints
        :return: None
        """

        # Getting worse probabilities should be higher for the normal care compare to the complex care

        self.opt_model += self.mc_n[(0, 2)] >= self.mc_c[(0, 2)]
        self.opt_model += self.mc_n[(1, 3)] >= self.mc_c[(1, 3)]
        self.opt_model += self.mc_n[(2, 4)] >= self.mc_c[(2, 4)]
        self.opt_model += self.mc_n[(3, 5)] >= self.mc_c[(3, 5)]

    def getting_better_constraints(self):

        """
        This method includes the getting-better constraints
        :return: None
        """

        # Getting better probabilities should be lower for the normal care compare to the complex care

        self.opt_model += self.mc_n[(2, 0)] <= self.mc_c[(2, 0)]
        self.opt_model += self.mc_n[(3, 1)] <= self.mc_c[(3, 1)]
        self.opt_model += self.mc_n[(4, 2)] <= self.mc_c[(4, 2)]
        self.opt_model += self.mc_n[(5, 3)] <= self.mc_c[(5, 3)]

    def getting_worse_PAM_relation_constraints(self):

        """
        This method includes getting-worse PAM relation constraints
        :return: None
        """

        # The probability of getting worse for the Low PAM patients
        # should be higher than patients with high PAM value

        self.opt_model += self.mc_n[(0, 2)] >= self.mc_n[(1, 3)]
        self.opt_model += self.mc_c[(0, 2)] >= self.mc_c[(1, 3)]
        self.opt_model += self.mc_n[(2, 4)] >= self.mc_n[(3, 5)]
        self.opt_model += self.mc_c[(2, 4)] >= self.mc_c[(3, 5)]

    def getting_better_PAM_relation_constraints(self):

        """
        This method includes getting-better PAM relation constraints
        :return: None
        """

        # The probability of getting better for the high PAM patients
        # should be higher than patients with low PAM value

        self.opt_model += self.mc_n[(3, 1)] >= self.mc_n[(2, 0)]
        self.opt_model += self.mc_c[(3, 1)] >= self.mc_c[(2, 0)]
        self.opt_model += self.mc_n[(5, 3)] >= self.mc_n[(4, 2)]
        self.opt_model += self.mc_c[(5, 3)] >= self.mc_c[(4, 2)]

    def getting_higher_constraints(self):

        """
        This method includes getting higher constraints
        :return: None
        """

        # Transition probability from low to high PAM
        # is higher for the patients taking complex care

        self.opt_model += self.mc_c[(0, 1)] >= self.mc_n[(0, 1)]
        self.opt_model += self.mc_c[(2, 3)] >= self.mc_n[(2, 3)]
        self.opt_model += self.mc_c[(4, 5)] >= self.mc_n[(4, 5)]

    def getting_lower_constraints(self):

        """
        This method includes getting lower constraints
        :return: None
        """

        # Transition probability from high to low PAM
        # is higher for the patients taking normal care

        self.opt_model += self.mc_c[(1, 0)] <= self.mc_n[(1, 0)]
        self.opt_model += self.mc_c[(3, 2)] <= self.mc_n[(3, 2)]
        self.opt_model += self.mc_c[(5, 4)] <= self.mc_n[(5, 4)]

    def death_probability_constraints(self):

        """
        This method introduces death probabilities
        :return: None
        """

        # In the same state, patient taking normal care
        # is more likely to die compare to patients taking complex care and
        # all dead probabilities should be less than or equal to 0.20

        for i in range(self.n_state - 1):
            self.opt_model += self.mc_n[(i, self.n_state - 1)] >= self.mc_c[(i, self.n_state - 1)]
            self.opt_model += self.mc_n[(i, self.n_state - 1)] <= 0.20
            self.opt_model += self.mc_c[(i, self.n_state - 1)] <= 0.15
            self.opt_model += self.mc_n[(i, self.n_state - 1)] >= 0.07
            self.opt_model += self.mc_c[(i, self.n_state - 1)] >= 0.03

        # In the same PAM level, worse patients' dead probability should be higher

        self.opt_model += self.mc_n[(4, self.n_state - 1)] >= self.mc_n[(2, self.n_state - 1)]
        self.opt_model += self.mc_c[(4, self.n_state - 1)] >= self.mc_c[(2, self.n_state - 1)]
        self.opt_model += self.mc_n[(2, self.n_state - 1)] >= self.mc_n[(0, self.n_state - 1)]
        self.opt_model += self.mc_c[(2, self.n_state - 1)] >= self.mc_c[(0, self.n_state - 1)]
        self.opt_model += self.mc_n[(5, self.n_state - 1)] >= self.mc_n[(3, self.n_state - 1)]
        self.opt_model += self.mc_c[(5, self.n_state - 1)] >= self.mc_c[(3, self.n_state - 1)]
        self.opt_model += self.mc_n[(3, self.n_state - 1)] >= self.mc_n[(1, self.n_state - 1)]
        self.opt_model += self.mc_c[(3, self.n_state - 1)] >= self.mc_c[(1, self.n_state - 1)]

        # In the same complexity level, low patients are more likely to die
        self.opt_model += self.mc_n[(0, self.n_state - 1)] >= self.mc_n[(1, self.n_state - 1)]
        self.opt_model += self.mc_n[(2, self.n_state - 1)] >= self.mc_n[(3, self.n_state - 1)]
        self.opt_model += self.mc_n[(4, self.n_state - 1)] >= self.mc_n[(5, self.n_state - 1)]
        self.opt_model += self.mc_c[(0, self.n_state - 1)] >= self.mc_c[(1, self.n_state - 1)]
        self.opt_model += self.mc_c[(2, self.n_state - 1)] >= self.mc_c[(3, self.n_state - 1)]
        self.opt_model += self.mc_c[(4, self.n_state - 1)] >= self.mc_c[(5, self.n_state - 1)]

        # Death is an absorbing state
        self.opt_model += self.mc_n[(self.n_state - 1, self.n_state - 1)] == 1
        self.opt_model += self.mc_c[(self.n_state - 1, self.n_state - 1)] == 1

    def limit_getting_better_probabilities(self):

        """
        We don't want to much getting better events due to characteristics of chronic diseases
        :return: None
        """

        self.opt_model += self.mc_n[(2, 0)] <= 0.1
        self.opt_model += self.mc_n[(3, 1)] <= 0.1
        self.opt_model += self.mc_n[(4, 2)] <= 0.1
        self.opt_model += self.mc_n[(5, 3)] <= 0.1

        self.opt_model += self.mc_c[(2, 0)] <= 0.15
        self.opt_model += self.mc_c[(3, 1)] <= 0.15
        self.opt_model += self.mc_c[(4, 2)] <= 0.15
        self.opt_model += self.mc_c[(5, 3)] <= 0.15

    def limit_diagonal_worse(self):

        """
        Includes rules related to the diagonal getting worse conditions
        :return: None
        """

        self.opt_model += self.mc_n[(1, 2)] <= 0.3
        self.opt_model += self.mc_n[(3, 4)] <= 0.3
        self.opt_model += self.mc_c[(1, 2)] <= 0.2
        self.opt_model += self.mc_c[(3, 4)] <= 0.2

        self.opt_model += self.mc_n[(1, 2)] >= self.mc_c[(1, 2)]
        self.opt_model += self.mc_n[(3, 4)] >= self.mc_c[(3, 4)]

    def zero_arc_constraints(self):

        """
        It dictates that non-allowed moves in the graph must have zero probabilities
        :return: None
        """

        # State 0
        self.opt_model += self.mc_n[(0, 3)] == 0
        self.opt_model += self.mc_n[(0, 4)] == 0
        self.opt_model += self.mc_n[(0, 5)] == 0
        self.opt_model += self.mc_c[(0, 3)] == 0
        self.opt_model += self.mc_c[(0, 4)] == 0
        self.opt_model += self.mc_c[(0, 5)] == 0

        # State 1
        self.opt_model += self.mc_n[(1, 4)] == 0
        self.opt_model += self.mc_n[(1, 5)] == 0
        self.opt_model += self.mc_c[(1, 4)] == 0
        self.opt_model += self.mc_c[(1, 5)] == 0

        # State 2
        self.opt_model += self.mc_n[(2, 5)] == 0
        self.opt_model += self.mc_c[(2, 5)] == 0

        # State 3
        self.opt_model += self.mc_n[(3, 0)] == 0
        self.opt_model += self.mc_c[(3, 0)] == 0

        # State 4
        self.opt_model += self.mc_n[(4, 0)] == 0
        self.opt_model += self.mc_n[(4, 1)] == 0
        self.opt_model += self.mc_c[(4, 0)] == 0
        self.opt_model += self.mc_c[(4, 1)] == 0

        # State 5
        self.opt_model += self.mc_n[(5, 0)] == 0
        self.opt_model += self.mc_n[(5, 1)] == 0
        self.opt_model += self.mc_c[(5, 0)] == 0
        self.opt_model += self.mc_c[(5, 1)] == 0
        self.opt_model += self.mc_n[(5, 2)] == 0
        self.opt_model += self.mc_c[(5, 2)] == 0

    def stochastic_matrix_constraint(self):

        """
        It enables the model to satisfy the requirements of being stochastic matrix
        :return: None
        """

        for i in range(self.n_state):
            self.opt_model += opt.lpSum(self.mc_c[i, j] for j in range(self.n_state)) == 1
            self.opt_model += opt.lpSum(self.mc_n[i, j] for j in range(self.n_state)) == 1

    def run_get_tpm(self):

        self.define_objective_function()
        self.getting_worse_constraints()
        self.getting_better_constraints()
        self.getting_worse_PAM_relation_constraints()
        self.getting_better_PAM_relation_constraints()
        self.getting_higher_constraints()
        self.getting_lower_constraints()
        self.death_probability_constraints()
        self.limit_getting_better_probabilities()
        self.limit_diagonal_worse()
        self.zero_arc_constraints()
        self.stochastic_matrix_constraint()

        self.opt_model.solve()
        p_n = np.empty(shape=(self.n_state, self.n_state))
        p_c = np.empty(shape=(self.n_state, self.n_state))
        for i in range(self.n_state):
            for j in range(self.n_state):
                p_n[i, j] = self.mc_n[(i, j)].varValue
                p_c[i, j] = self.mc_c[(i, j)].varValue

        return p_n, p_c

class MCTPM(object):

    def __init__(self, n_state, sample_size):

        self.n_state = n_state
        self.sample_size = sample_size

    def get_samples(self):

        ls_pn, ls_pc = [], []
        count = 0
        for seed in range(self.sample_size):
            model = RTPM(seed, self.n_state)
            pn, pc = model.run_get_tpm()
            ls_pn.append(pn)
            ls_pc.append(pc)
            count+=1
            print(count)

        return ls_pn, ls_pc

    def get_transition_probs(self):

        pn, pc = self.get_samples()
        pn = sum(pn) / self.sample_size
        pc = sum(pc) / self.sample_size
        utils_.mc_normalization(pn)
        utils_.mc_normalization(pc)

        return pn, pc
