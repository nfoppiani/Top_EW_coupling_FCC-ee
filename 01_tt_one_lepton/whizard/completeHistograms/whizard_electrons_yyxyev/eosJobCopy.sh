#!/bin/sh

# I used this program to copy the tt_<number>.root files from the eosDir to the current directory
# the program must be launched with 'sh eosJobCopy.sh'

eosDir=/store/cmst3/user/tpajero/ttbar365Wizard/yyxyev/

# 661 files (from 1 to 661)
# 98 does not exist!

for ((job=1;job<2;job++));
  do 
  echo "JOB "$job 
  rootFile="yyxyev_o_"${job}".root"
  fileToStage=$eosDir$rootFile
  # nsls $fileToStage
  # stager_qry -M $fileToStage
  cmsStage $fileToStage .
  # copies the files from eos to the current directory
  # cmsStage is the scp command from eos
done