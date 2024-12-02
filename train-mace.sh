#!/bin/bash -l

# Batch script to run a GPU job under SGE.

# Request a number of GPU cards, in this case 2 (the maximum)
#$ -l gpu=2

# Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=01:00:00

# Request 1 gigabyte of RAM (must be an integer followed by M, G, or T)
#$ -l mem=30G

# Request 15 gigabyte of TMPDIR space (default is 10 GB)
#$ -l tmpfs=15G

# Set the name of the job.
#$ -N GPU-MACE-Test

# Set the working directory to somewhere in your scratch space.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/uccabaa/Scratch/repositories/mace/models/BaTiO3

#$ -P Free
#$ -A UCL_chemM_Butler

# load the cuda module (in case you are running a CUDA program)
module unload compilers mpi
module unload gcc-libs
module load compilers/gnu/10.2.0
module load python
module load git
module load cuda/11.2.0/gnu-10.2.0
source ~/.bashrc
conda activate mace_env

git checkout 'mu_alpha'

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Run the application - the line below is just a random example.
mace_run_train \
    --name="BaTiO3_MACE_dipole_pol" \
    --train_file="data/BaTiO3_train.xyz" \
    --test_file="data/BaTiO3_test.xyz" \
    --valid_fraction=0.05 \
    --model="AtomicDielectricMACE" \
    --model_dir="MACE_models" \
    --log_dir="MACE_models" \
    --checkpoints_dir="MACE_models" \
    --results_dir="MACE_models" \
    --E0s="average" \
    --num_channels=32 \
    --max_L=2 \
    --r_max=5.0 \
    --loss="dipole" \
    --dipole_weight=1.0 \
    --polarizability_weight=1.0 \
    --dipole_key="REF_dipole"  \
    --polarizability_key="REF_polarizability" \
    --weight_decay=5e-10 \
    --clip_grad=1.0 \
    --batch_size=64 \
    --valid_batch_size=64 \
    --max_num_epochs=100 \
    --eval_interval=1 \
    --ema \
    --error_table='DipoleRMSE' \
    --default_dtype="float64"\
    --device=cuda \
    --seed=123 \
    --restart_latest \
    --save_cpu \
    --compute_polarizability

mace_eval_mu_alpha \
  --configs="data/BaTiO3.xyz" \
  --model="MACE_models/BaTiO3_MACE_dipole_pol.model" \
  --output="BaTiO3.xyz" \
  --device=cuda \
  --batch_size=10

# 10. Preferably, tar-up (archive) all output files onto the shared scratch area
# tar zcvf $HOME/Scratch/files_from_job_$JOB_ID.tar.gz $TMPDIR

# Make sure you have given enough time for the copy to complete!
