#!/bin/bash

# load environment variables
if [ -f "../.env" ]
then
	export $(cat ../.env | xargs)
fi

# relevants paths
data_path="${CORPUS}${EPOCH_TYPE}/"
files=$(find ${data_path}corpus*.mm)
hdp="hdp/hdp/./hdp"
dir_to_save="${RESULTS}hdp/${EPOCH_TYPE}"
N=$(wc -w <<< $files)

# clean previous results
rm -rf $dir_to_save
mkdir $dir_to_save

# run hdp over each epoch
for file in $files
do
    # get epoch
    epoch=$(echo $file| cut -d'_' -f 2| cut -d'.' -f 1)
    # path to save model results
    path_to_save="${dir_to_save}/model_${epoch}"
    mkdir $path_to_save
    # run hdp
    echo "***Step: ${epoch}/${N}***"
    $hdp --algorithm train --data $file --directory $path_to_save --save_lag -1 --random_seed 123 --max_iter 5000 --split_merge yes
done