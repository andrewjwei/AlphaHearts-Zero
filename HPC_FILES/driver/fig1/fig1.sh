#!/bin/bash

#SBATCH --job-name=csec_fig1
#SBATCH --output=driver/fig1/csec_fig1.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --partition=week
#SBATCH --time=7-00:00:00

source env/venv/bin/activate
python driver/fig1/fig1.py $1 $2