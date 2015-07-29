#!/bin/sh

# I used this program to copy the tt_<number>.root files from the eosDir to the current directory
# the program must be launched with 'sh eosJobCopy.sh'

eosDir=/store/cmst3/user/pjanot/ttbar365Pythia/

for ((job=1;job<1000;job++));
  do 
  echo "JOB "$job 
  rootFile="tt_"${job}".root"
  fileToStage=$eosDir$rootFile
  nsls $fileToStage
  stager_qry -M $fileToStage
  cmsStage $fileToStage .
  # copies the files from eos to the current directory
  # cmsStage is the scp command from eos
done