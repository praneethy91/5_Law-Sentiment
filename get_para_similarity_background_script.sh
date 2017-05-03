#!/bin/bash
#
##SBATCH --nodes=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=12:00:00
#SBATCH --mem=90GB
#SBATCH --job-name=phrase_similarity
#SBATCH --mail-type=END
#SBATCH --mail-user=bsg348@nyu.edu
#SBATCH --output=abc.o

module purge
module load gensim/intel/python3.5/1.0.1
module load nltk/3.2.2
python3 get_para_word2vec.py
