package var_mdp;

import ilog.concert.IloException;

public class Main {

	public static void main(String[] args) throws IloException {
		
		int n_state = 7;
		int n_action = 2;
		double discount_factor = 0.90;
		
		double[] alpha = {1.0 /6, 1.0 /6, 1.0 /6, 1.0 /6, 1.0 /6, 1.0 /6};
		// double[] alpha = {0.1, 0.2, 0.3, 0.1, 0.2, 0.1};
		double[][] mc_n = new double[n_state][n_state];
		double[][] mc_c = new double[n_state][n_state];
		Read reader1 = new Read("normal_care_transitions.xlsx");
		Read reader2 = new Read("complex_care_transitions.xlsx");
		reader1.read_transition(mc_n);
		reader2.read_transition(mc_c);
		
		Read reader3 = new Read("mc_ns.xlsx");
		Read reader4 = new Read("mc_cs.xlsx");
		Read reader5 = new Read("mc_costs.xlsx");
		int n_scenario = 50;
		double[][][] mc_ns = new double[n_state][n_state][n_scenario];
		double[][][] mc_cs = new double[n_state][n_state][n_scenario];
		double[][] cost = new double[n_state][n_scenario];
		reader3.read_scenario_transition(mc_ns, n_scenario);
		reader4.read_scenario_transition(mc_cs, n_scenario);
		reader5.read_scenario_cost(cost, n_scenario);
		
		/*
		Simple_Model model = new Simple_Model(n_state, n_action);
		model.set_objective(alpha);
		model.deterministic_policy_constraint();
		model.bellman_optimality_constraint(cost, mc_n, mc_c, discount_factor);
		model.linearization_constraints();
		System.out.println(model.cplex.solve());
		System.out.println(model.cplex.getObjValue());
		for(int i=0;i<n_state-1;i++) {
			for(int a=0;a<n_action;a++) {
				if(model.cplex.getValue(model.w[i][a]) == 1) {
					System.out.println("State: "+i+" - "+"Action: "+a);
				}
			}
		}
		*/
		/*
		double beta = 0.01;
		double[] p_s = new double[n_scenario];
		for(int s=0;s<n_scenario;s++) {
			p_s[s]=1.0/n_scenario;
		}
		Math_Model mdl = new Math_Model(n_state, n_action, n_scenario);
		mdl.set_objective();
		mdl.one_policy_to_each_state_constraint();
		mdl.greater_than_beta_constraint(p_s, beta);
		mdl.v_y_constraint(alpha);
		mdl.bellman_optimality_constraint(cost, mc_ns, mc_cs, discount_factor);
		mdl.linearization_constraints();
		System.out.println(mdl.cplex.solve());
		System.out.println(mdl.cplex.getObjValue());
		for(int i=0;i<n_state-1;i++) {
			for(int a=0;a<n_action;a++) {
				if(mdl.cplex.getValue(mdl.w[i][a]) == 1) {
					System.out.println("State: "+i+" - "+"Action: "+a);
				}
			}
		}
		*/
		double[] p_s = new double[n_scenario];
		for(int s=0;s<n_scenario;s++) {
			p_s[s]=1.0/n_scenario;
		}
		double[] beta= {1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01};
		double[] obj = new double[beta.length];
		for(int b=0;b<beta.length;b++) {
			Math_Model mdl = new Math_Model(n_state, n_action, n_scenario);
			mdl.set_objective();
			mdl.one_policy_to_each_state_constraint();
			mdl.greater_than_beta_constraint(p_s, beta[b]);
			mdl.v_y_constraint(alpha);
			mdl.bellman_optimality_constraint(cost, mc_ns, mc_cs, discount_factor);
			mdl.linearization_constraints();
			mdl.cplex.solve();
			obj[b] = mdl.cplex.getObjValue();
		}
		for(int b=0;b<beta.length;b++) {
			System.out.println("beta: "+beta[b]+" _ "+"obj: "+obj[b]);
		}
	}
}
