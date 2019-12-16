package var_mdp;

import ilog.concert.IloException;
import ilog.concert.IloLinearNumExpr;
import ilog.concert.IloNumVar;
import ilog.concert.IloNumVarType;
import ilog.cplex.IloCplex;

public class Math_Model {
	
	int nState;
	int nAction;
	int nScenario;
	
	IloCplex cplex ;
	
	// Decision Variables
	
	IloNumVar[][][][] x; 
	IloNumVar[][] w;
	IloNumVar[][] v;
	IloNumVar[] z;
	IloNumVar y;
	
	public Math_Model(int n_state, int n_action, int n_scenario) throws IloException {
		
		nState = n_state ;
		nAction = n_action ;
		nScenario = n_scenario ;
		
		try {
			cplex = new IloCplex();
		} catch (IloException e) {
			e.printStackTrace();
		}

		x = new IloNumVar[nState-1][nState-1][nScenario][nAction];
		w = new IloNumVar[nState-1][nAction];
		v = new IloNumVar[nState-1][nScenario];
		z = new IloNumVar[nScenario];
		
		y = cplex.numVar(0, 10000, IloNumVarType.Float, "y");
		
		for(int s=0;s<nScenario;s++) {
			z[s] = cplex.numVar(0, 1, IloNumVarType.Bool,"z"+"_"+s);
		}
		
		for(int i=0;i<nState-1;i++) {
			for(int s=0;s<nScenario;s++) {
				v[i][s] = cplex.numVar(0, 10000, IloNumVarType.Float,"v"+"_"+i+"_"+s);
			}
		}
		
		for(int i=0;i<nState-1;i++) {
			for(int a=0;a<nAction;a++) {
				w[i][a] = cplex.numVar(0, 1, IloNumVarType.Bool,"w"+"_"+i+"_"+a);
			}
		}
		
		for(int i=0;i<nState-1;i++) {
			for(int j=0;j<nState-1;j++) {
				for(int s=0;s<nScenario;s++) {
					for(int a=0;a<nAction;a++) {
						x[i][j][s][a] = cplex.numVar(0, 10000, IloNumVarType.Float,"x"+"_"+i+"_"+j+"_"+s+"_"+a);
					}
				}
			}
		}
	}

	public void set_objective() throws IloException {
		cplex.addMinimize(y);
	}
	
	public void one_policy_to_each_state_constraint() throws IloException{
		for(int i=0;i<nState-1;i++) {
			IloLinearNumExpr linExpr = cplex.linearNumExpr();
			for(int a=0;a<nAction;a++) {
				linExpr.addTerm(1, w[i][a]);
			}
			cplex.addEq(linExpr,1);
		}
	}
	
	public void greater_than_beta_constraint(double[] p_s, double beta) throws IloException{
		IloLinearNumExpr linExpr = cplex.linearNumExpr();
		for(int s=0;s<nScenario;s++) {
			linExpr.addTerm(z[s], p_s[s]);
		}
		cplex.addGe(linExpr,beta);
	}
	
	public void v_y_constraint(double[] alpha) throws IloException {
		
		for(int s=0;s<nScenario;s++) {
			IloLinearNumExpr linExpr = cplex.linearNumExpr();
			for(int i=0;i<nState-1;i++) {
				linExpr.addTerm(alpha[i], v[i][s]);
			}
			cplex.addLe(linExpr, cplex.sum(y, cplex.prod(cplex.sum(1, cplex.prod(-1, z[s])), 10000)));
		}
	}
	
	public void bellman_optimality_constraint(double[][] c, double[][][] p_n, double[][][] p_c, double gamma) throws IloException{
		for(int i=0;i<nState-1;i++) {
			for(int s=0;s<nScenario;s++) {
				IloLinearNumExpr linExpr = cplex.linearNumExpr();
				for(int a=0;a<nAction;a++) {
					for(int j=0;j<nState-1;j++) {
						if(a==0) {
							linExpr.addTerm(p_n[i][j][s], x[i][j][s][a]);
						}
						if(a==1) {
								linExpr.addTerm(p_c[i][j][s], x[i][j][s][a]);
						}
					}
				}
				double temp0 = p_n[i][nState-1][s] * c[nState-1][s];
				double temp1 = p_c[i][nState-1][s] * c[nState-1][s];
				linExpr.addTerm(temp0, w[i][0]);
				linExpr.addTerm(temp1, w[i][1]);
				
				cplex.addGe(v[i][s], cplex.sum(c[i][s], cplex.prod(gamma, linExpr)));
			}
		}
 }

	public void linearization_constraints() throws IloException {
		for(int i=0;i<nState-1;i++) {
			for(int j=0;j<nState-1;j++) {
				for(int s=0;s<nScenario;s++) {
					for(int a=0;a<nAction;a++) {
						cplex.addLe(x[i][j][s][a], cplex.prod(10000, w[i][a]));
						cplex.addLe(x[i][j][s][a], v[j][s]);
						cplex.addGe(x[i][j][s][a], cplex.sum(v[j][s], cplex.prod(-10000, cplex.sum(1, cplex.prod(-1, w[i][a])))));
						
					}
				}
			}
		}
	}
}
