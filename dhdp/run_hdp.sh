#!/bin/bash

# relevants paths
data_path="../data/corpus/quarter/"
files=$(find ${data_path}corpus*.mm)
hdp="hdp/hdp/./hdp"
dir_to_save="results/hdp/quarter"
N=$(wc -w <<< $files)

# clean previous results
rm -rf $dir_to_save
mkdir $dir_to_save

# run hdp over each slice
for file in $files
do
    # get slice
    slice=$(echo $file| cut -d'_' -f 2| cut -d'.' -f 1)
    # path to save model results
    path_to_save="${dir_to_save}/model_${slice}"
    mkdir $path_to_save
    # run hdp
    echo "***Step: ${slice}/${N}***"
    $hdp --algorithm train --data $file --directory $path_to_save --save_lag -1 --random_seed 123 --max_iter 5000 --split_merge yes
done

