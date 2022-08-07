csec_v3      contains the main code, including the hearts module, the Q-learning module, the self-play module, etc. It is primarily designed to work on the Zoo.
Environments contains the environment (csec) needed to run csec_v3. On the HPC, this environment is called (venv). But it is essentially the same environment.
HPC_FILES    contains the code needed to generate networks and exhibits on the HPC, as well as the important save files. However, the networks themselves are not saved as they take forever to run.
Paper        contains the final report paper as well as copies of the figures. The figures are all copies of figures generated in the HPC and saved.
example_nn   contains neural network (fc_100_perf) that is used for the example.
temp         is an empty folder. However, if you decide to call run/generate.py, it will fill up with generated networks
run          will run the demonstration. run/generate.py will generate copies of the neural network. run/demo.py will play against the neural network. Make sure you have the appropriate packages.