
from verifai.samplers.scenic_sampler import ScenicSampler
from verifai.scenic_server import ScenicServer
from dotmap import DotMap
from verifai.falsifier import mtl_falsifier, generic_falsifier
from verifai.features.features import *
from verifai.monitor import specification_monitor, mtl_specification
from time import sleep
import pickle
import sys
import os

PORT = 8888
MAXREQS = 5
BUFSIZE = 4096

MODE = sys.argv[1]
assert MODE in ["falsify", "smc"]

MAX_ITERS = int(sys.argv[2])
assert MAX_ITERS > 0

if MODE == "falsify":
    ALPHA = float(sys.argv[3])
    assert (ALPHA > 0.0) and (ALPHA <= 1.0) and (MAX_ITERS*ALPHA == int(MAX_ITERS*ALPHA)) and (1/ALPHA == int(1/ALPHA))
else:
    ALPHA = 1.0

METHOD = sys.argv[4]
assert METHOD in ["compositional", "monolithic"]

def get_falsifier(scenario, specification):

    path = os.path.join(os.path.dirname(__file__), scenario)
    sampler = ScenicSampler.fromScenario(path)

    falsifier_params = DotMap(
        n_iters=MAX_ITERS*ALPHA if MODE == "falsify" else MAX_ITERS,
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
    concurrent_iteration_num = int(1/ALPHA)
else:
    concurrent_iteration_num = 1

for i in range(concurrent_iteration_num):
    if MODE == "falsify":
        print("Concurrent Iteration", i)
    for subscenario in subscenarios:

        falsifier = get_falsifier(subscenario + ".scenic", specification)

        print("Falsifier is running for " + subscenario + "...")
        if MODE == "falsify":
            try:
                falsifier.run_falsifier()
            except EOFError as e:
                print("Falsification ended successfully.")
                falsifier.error_table.table.to_csv(MODE + "_csvs/" + subscenario + "_error_table.csv", index=False)
                falsifier.safe_table.table.to_csv(MODE + "_csvs/" + subscenario + "_safe_table.csv", index=False)
                print("Sleeping for 60 seconds...")
                sleep(60)
                sys.exit()
        else:
            falsifier.run_falsifier()

        # print("Scenic samples for " + subscenario + "...")
        # for i in falsifier.samples.keys():
        #     print("Sample: ", i)
        #     print(falsifier.samples[i])

        # print("Error table for " + subscenario + "...")
        # print(falsifier.error_table.table)

        print("Done.")
        falsifier.error_table.table.to_csv(MODE + "_csvs/" + subscenario + "_error_table.csv", index=False)
        falsifier.safe_table.table.to_csv(MODE + "_csvs/" + subscenario + "_safe_table.csv", index=False)

        print("Sleeping for 60 seconds...")
        sleep(60)
