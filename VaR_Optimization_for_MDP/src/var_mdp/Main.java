package var_mdp;

import ilog.concert.IloException;

public class Main {

	public static void main(String[] args) throws IloException {
		
		int n_state = 7;
		int n_action = 2;
		int n_scenario = 5;
		
		double[] p_s = {0.2, 0.2, 0.2, 0.2, 0.2};
		double[] alpha = {0.1, 0.2, 0.2, 0.3, 0.1, 0.1, 0};
		double beta = 0.90;
		double[][] mc_n = new double[n_state][n_state];
		double[][] mc_c = new double[n_state][n_state];
		
		double[] cost = {10,0,50,20,100,70,100};
		
		Read reader1 = new Read("normal_care_transitions.xlsx");
		Read reader2 = new Read("complex_care_transitions.xlsx");
		reader1.read_transition(mc_n);
		reader2.read_transition(mc_c);
		
		Math_Model model = new Math_Model(n_state, n_action, n_scenario);
		model.set_objective();
		model.one_policy_to_each_state_constraint();
		model.greater_than_beta_constraint(p_s, beta);
		model.v_y_constraint(alpha);
		System.out.println(model.cplex.solve());
		System.out.println("works well");
	}
}
