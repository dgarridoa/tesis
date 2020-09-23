#!/bin/bash

# load environment variables
set -a; . ../.env; set +a

# relevants paths
data_path="${CORPUS}"
files=$(find ${data_path} -name *.mm)
dir_to_save="${MODEL_PATH}"

# clean previous results
rm -rf $dir_to_save
mkdir $dir_to_save

# run hdp over each epoch
hdp="hdp/hdp/./hdp"
N=$(echo $files | wc -w)
for file in $files
do
    # get epoch
    epoch=$(echo $file| cut -d'_' -f 2| cut -d'.' -f 1)
    # path to save model results
    path_to_save="${dir_to_save}/model_${epoch}"
    mkdir $path_to_save
    # run hdp
    echo "***Step: ${epoch}/${N}***"
    $hdp --algorithm train --data $file --directory $path_to_save --save_lag -1 --random_seed 123 --max_iter $MAX_ITER --split_merge yes
done