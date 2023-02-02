from verifai.samplers.scenic_sampler import ScenicSampler
from verifai.scenic_server import ScenicServer
from dotmap import DotMap
from verifai.falsifier import mtl_falsifier, generic_falsifier
from verifai.features.features import *
from verifai.monitor import specification_monitor, mtl_specification
from time import sleep
import pickle
import math
import sys
import os

PORT = 8888
MAXREQS = 5
BUFSIZE = 4096

MODE = sys.argv[1]
assert MODE in ["falsify", "smc"]
print("Mode:", MODE)

METHOD = sys.argv[2]
assert METHOD in ["compositional", "monolithic"]
print("Method:", METHOD)

ALPHA = float(sys.argv[3]) # Typical values: [0.05, 0.03, 0.01]
assert ALPHA > 0 and ALPHA <= 1
print("Alpha:", ALPHA)

EPSILON = float(sys.argv[4]) # Typical values: [0.1, 0.05, 0.01]
assert EPSILON > 0 and EPSILON <= 1
print("Epsilon:", EPSILON)

SIGMA = float(sys.argv[5])
assert (SIGMA > 0.0) and (SIGMA <= 1.0)
print("Sigma:", SIGMA)

MAX_ITERS = math.ceil(math.log(2/ALPHA)/(2*(EPSILON**2)))
assert MAX_ITERS > 0
print("Maximum Number of Iterations:", MAX_ITERS)

BATCH_SIZE = math.ceil(MAX_ITERS*SIGMA)
assert BATCH_SIZE > 0
print("Batch Size:", BATCH_SIZE)

BATCHED_ITERS = math.ceil(1/SIGMA)
assert BATCHED_ITERS > 0
print("Number of Batched Iterations:", BATCHED_ITERS)

with open("mode.txt", "w+") as f:
    f.write(MODE)

def get_falsifier(scenario, specification):

    path = os.path.join(os.path.dirname(__file__), scenario)
    sampler = ScenicSampler.fromScenario(path)

    falsifier_params = DotMap(
        n_iters=BATCH_SIZE if MODE == "falsify" else MAX_ITERS,
        save_error_table=True,
        save_safe_table=True
    )

    server_options = DotMap(
        port=PORT,
        bufsize=BUFSIZE,
        maxreqs=MAXREQS
    )

    falsifier = mtl_falsifier(
        sampler=sampler,
        sampler_type="ce",
        specification=specification,
        falsifier_params=falsifier_params,
        server_options=server_options
    )

    return falsifier

subscenarios = None
if METHOD == "compositional":
    subscenarios = ["subscenario1", "subscenario2L", "subscenario2S", "subscenario2R"]
else:
    subscenarios = ["scenarioL", "scenarioS", "scenarioR"]

for subscenario in subscenarios:
    with open(MODE + "_csvs/" + subscenario + "_post_conditions.csv", "+w") as f:
        f.write("ego_x,ego_y,ego_heading,lead_x,lead_y,lead_heading\n")
    with open(MODE + "_csvs/" + subscenario + "_results.csv", "+w") as f:
        f.write("sample_ind,rho,sim_steps\n")

specification = ["G(distance)"]

if MODE == "falsify":
    for i in range(BATCHED_ITERS):
        print("Batched Iteration", i)
        for subscenario in subscenarios:
            falsifier = get_falsifier(subscenario + ".scenic", specification)
            print("Falsifier is running for " + subscenario + "...")
            try:
                falsifier.run_falsifier()
            except EOFError as e:
                print("Falsification ended successfully.")
                falsifier.error_table.table.to_csv(MODE + "_csvs/" + subscenario + "_error_table.csv", index=False)
                falsifier.safe_table.table.to_csv(MODE + "_csvs/" + subscenario + "_safe_table.csv", index=False)
                print("Sleeping for 60 seconds...")
                sleep(60)
                sys.exit()
            print("Done.")
            falsifier.error_table.table.to_csv(MODE + "_csvs/" + subscenario + "_error_table.csv", index=False)
            falsifier.safe_table.table.to_csv(MODE + "_csvs/" + subscenario + "_safe_table.csv", index=False)
            print("Sleeping for 60 seconds...")
            sleep(60)
else:
    for subscenario in subscenarios:
        falsifier = get_falsifier(subscenario + ".scenic", specification)
        print("Falsifier is running for " + subscenario + "...")
        falsifier.run_falsifier()
        print("Done.")
        falsifier.error_table.table.to_csv(MODE + "_csvs/" + subscenario + "_error_table.csv", index=False)
        falsifier.safe_table.table.to_csv(MODE + "_csvs/" + subscenario + "_safe_table.csv", index=False)
        print("Sleeping for 60 seconds...")
        sleep(60)
