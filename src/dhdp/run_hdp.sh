#!/bin/bash

# load environment variables
set -a; . ../.env; set +a

# clean previous results
rm -rf $MODEL_PATH
mkdir $MODEL_PATH

##### parallelizing hdp #####
hdp="hdp/hdp/./hdp"

# function to run hdp
hdp(){
    file=$1
    # get epoch
    epoch=$(echo $file| cut -d'_' -f 2| cut -d'.' -f 1)
    # path to save model results
    path_to_save="${MODEL_PATH}/model_${epoch}"
    mkdir $path_to_save
    # run hdp
    $hdp --algorithm train --data $file --directory $path_to_save --save_lag -1 --random_seed 123 --max_iter $MAX_ITER --gamma_a 1 --alpha_a 1 
}

# initialize a semaphore with a given number of tokens
open_sem(){
    mkfifo pipe-$$
    exec 3<>pipe-$$
    rm pipe-$$
    local i=$1
    for((;i>0;i--)); do
        printf %s 000 >&3
    done
}

# run the given command asynchronously and pop/push tokens
run_with_lock(){
    local x
    # this read waits until there is something to read
    read -u 3 -n 3 x && ((0==x)) || exit $x
    (
     ( "$@"; )
    # push the return code of the command to the semaphore
    printf '%.3d' $? >&3
    )&
}

# run code
open_sem $CORES
files=$(find $CORPUS -name *.mm)
for file in $files
do
    run_with_lock hdp $file
done 
