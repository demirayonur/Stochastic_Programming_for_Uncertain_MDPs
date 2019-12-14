from infinite_MDP import MDP


n_state, n_action, discount_factor = 7, 2, 0.99
# cost = [10, 0, 50, 20, 100, 70, 110]
# cost = [40, 38, 48, 42, 60, 55, 100]
# cost = [30, 24, 50, 44, 100, 94, 110]
# cost = [10, 0, 50, 20, 100, 70, 400]
cost = [100, 0, 1000, 750, 5000, 4000, 10000]
model = MDP(n_state, n_action, discount_factor, cost)
model.create_P()
model.value_iteration()
model.plot_policy()
