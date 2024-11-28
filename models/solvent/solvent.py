from ase.io import read, write
from ase import Atoms
import numpy as np
from tqdm import tqdm
from xtb.ase.calculator import XTB
from aseMolec import anaAtoms as aa

# read in list of configs
solvent_data = read('solvent.xyz', ':') 

# identify molecules and label molecular cluster
aa.wrap_molecs(solvent_data, prog=True)
write('solvent_molecules.xyz', solvent_data)

# add isolated atoms to the database
solvent_molecules_data = read('solvent_molecules.xyz', ':')
solvent_molecules_data = [Atoms('H'), Atoms('C'), Atoms('O')] + solvent_molecules_data
for at in solvent_molecules_data[:3]:
    at.info['config_type'] = 'IsolatedAtom'

# compute the energy and forces with XTB
xtb_calc = XTB(method="GFN2-xTB")
for at in tqdm(solvent_molecules_data):
    at.calc = xtb_calc
    at.info['energy_xtb'] = at.get_potential_energy()
    at.arrays['forces_xtb'] = at.get_forces()

print(solvent_molecules_data[13].info)
print(solvent_molecules_data[13].arrays)

# write('solvent_xtb.xyz', solvent_molecules_data) # save full result

# split data into train and test sets
# solvent_xtb_data = read('solvent_xtb.xyz', ':') 
write('solvent_xtb_train.xyz', solvent_molecules_data[:203]) # first 50 configs
write('solvent_xtb_test.xyz', solvent_molecules_data[-1000:]) # last 1000 configs

# train MACE model
import warnings
warnings.filterwarnings("ignore")
from mace.cli.run_train import main as mace_run_train_main
import sys
import logging

def train_mace(config_file_path):
    logging.getLogger().handlers.clear()
    sys.argv = ["program", "--config", config_file_path]
    mace_run_train_main()

train_mace("solvent_config.yml")

# remove checkpoints since they may cause errors on retraining a model with the same name but a different architecture
import glob
import os
for file in glob.glob("MACE_models/*.pt"):
    os.remove(file)