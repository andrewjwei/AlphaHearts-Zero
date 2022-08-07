#!/bin/bash

#SBATCH --job-name=csec_fig0
#SBATCH --output=driver/fig0/csec_fig0.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --partition=day
#SBATCH --time=1-00:00:00

source env/venv/bin/activate
if [ $1 == "--mcts" ]; then
    echo "Running optimal MCTS iteration checker"
    python driver/fig0/fig0b.py
    exit 0
elif [ $1 == "--pimc" ]; then
    echo "Running optimal PIMC determinization checker"
    python driver/fig0/fig0.py
    exit 0
elif [ $1 == "--expl" ]; then
    echo "Running optimal exploration constant checker"
    python driver/fig0/fig0a.py
    exit 0
else
    echo "Invalid Input: must specify --pimc for finding optimal PIMC or --mcts for finding optimal MCTS"
    exit 0
fi