#!/bin/bash

#SBATCH --job-name=csec_fig2
#SBATCH --output=driver/fig2/csec_fig2.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --partition=day
#SBATCH --time=1-00:00:00

module load CUDA
module load cuDNN
source env/venv/bin/activate
python driver/fig2/fig2.py $1 $2 $3 $4 $5