from ase.io import read, write
import numpy as np
import sys
import logging
import warnings
import glob
import os
warnings.filterwarnings("ignore")

# read in list of configs
water_bulk_data = read('data/water_bulk.xyz', ':') 

# split data into train and test sets
write('data/water_bulk_train.xyz', water_bulk_data[:800]) # first 20 configs
write('data/water_bulk_test.xyz', water_bulk_data[-200:]) # last 25 configs

from mace.cli.run_train import main as mace_run_train_main

def train_mace(config_file_path):
    logging.getLogger().handlers.clear()
    sys.argv = ["program", "--config", config_file_path]
    mace_run_train_main()

# train_mace("config/water_bulk_config.yml")

# remove checkpoints since they may cause errors on retraining a model with the same name but a different architecture
for file in glob.glob("MACE_models/*.pt"):
    os.remove(file)

os.makedirs("tests/", exist_ok=True)

from mace.cli.eval_mu_alpha import main as mace_eval_mu_alpha_main

def eval_mu_alpha(configs, model, output, device='cuda', batch_size='4'):
    sys.argv = ["program", "--configs", configs, "--model", model, "--output", output, "--device", device, "--batch_size", batch_size, "--default_dtype", "float64"]
    mace_eval_mu_alpha_main()

# evaluate dielectrics for the training set
# eval_mu_alpha(
#     configs="data/water_bulk_train.xyz",
#     model="MACE_models/water_bulk_MACE_dipole_pol.model",
#     output="water_bulk_train.xyz"
# )

# evaluate dielectrics for the test set
# eval_mu_alpha(
#     configs="data/water_bulk_test.xyz",
#     model="MACE_models/water_bulk_MACE_dipole_pol.model",
#     output="tests/water_bulk_test.xyz"
# )

from aseMolec import extAtoms as ea
dft_mu = np.matrix(ea.get_prop(water_bulk_data, 'info', 'REF_dipole', peratom=False))
with open('DATA_mu.txt','wb') as f:
    for line in dft_mu:
        np.savetxt(f, line)

dft_alpha = np.matrix(ea.get_prop(water_bulk_data, 'info', 'REF_polarizability', peratom=False))
with open('DATA_alpha.txt','wb') as f:
    for line in dft_alpha:
        np.savetxt(f, line)