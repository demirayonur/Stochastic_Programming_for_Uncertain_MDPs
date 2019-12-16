from infinite_MDP import MDP


n_state, n_action, discount_factor = 7, 2, 0.90
cost = [10, 0, 50, 20, 100, 70, 110]
model = MDP(n_state, n_action, discount_factor, cost)
model.create_P()
model.value_iteration()
model.plot_policy()
