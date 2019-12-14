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

		x = new IloNumVar[nState][nState][nScenario][nAction];
		w = new IloNumVar[nState][nAction];
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
		
		for(int i=0;i<nState;i++) {
			for(int a=0;a<nAction;a++) {
				w[i][a] = cplex.numVar(0, 1, IloNumVarType.Bool,"w"+"_"+i+"_"+a);
			}
		}
		
		for(int i=0;i<nState;i++) {
			for(int j=0;j<nState;j++) {
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
		for(int i=0;i<nState;i++) {
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
}
