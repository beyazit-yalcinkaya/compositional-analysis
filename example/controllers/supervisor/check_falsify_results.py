import numpy as np

monolithic = []
compositional = []
for i in range(1, 11):
	sL = np.genfromtxt("falsify_csvs_" + str(i) + "/scenarioL_results.csv", delimiter=",", names=True)
	sS = np.genfromtxt("falsify_csvs_" + str(i) + "/scenarioS_results.csv", delimiter=",", names=True)
	sR = np.genfromtxt("falsify_csvs_" + str(i) + "/scenarioR_results.csv", delimiter=",", names=True)
	s1 = np.genfromtxt("falsify_csvs_" + str(i) + "/subscenario1_results.csv", delimiter=",", names=True)
	s2L = np.genfromtxt("falsify_csvs_" + str(i) + "/subscenario2L_results.csv", delimiter=",", names=True)
	s2S = np.genfromtxt("falsify_csvs_" + str(i) + "/subscenario2S_results.csv", delimiter=",", names=True)
	s2R = np.genfromtxt("falsify_csvs_" + str(i) + "/subscenario2R_results.csv", delimiter=",", names=True)
	monolithic.append(sL["sim_steps"].sum() + sS["sim_steps"].sum() + sR["sim_steps"].sum())
	compositional.append(s1["sim_steps"].sum() + s2L["sim_steps"].sum() + s2S["sim_steps"].sum() + s2R["sim_steps"].sum())
	print("---- Sample", i, "----")
	print("Monolithic:", sL["sim_steps"].sum() + sS["sim_steps"].sum() + sR["sim_steps"].sum())
	print("Compositional:", s1["sim_steps"].sum() + s2L["sim_steps"].sum() + s2S["sim_steps"].sum() + s2R["sim_steps"].sum())
	print("-----------------")

print("Monolithic:", np.mean(monolithic), np.std(monolithic))
print("Compositional:", np.mean(compositional), np.std(compositional))