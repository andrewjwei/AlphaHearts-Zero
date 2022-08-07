#!/bin/bash

#SBATCH --job-name=generate_networks
#SBATCH --output=driver/network/generate_networks.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --partition=gpu 
#SBATCH --time=6:00:00
#SBATCH --gpus=1

module load CUDA
module load cuDNN
source env/venv/bin/activate
python driver/network/run.py $1 $2 $3 $4
