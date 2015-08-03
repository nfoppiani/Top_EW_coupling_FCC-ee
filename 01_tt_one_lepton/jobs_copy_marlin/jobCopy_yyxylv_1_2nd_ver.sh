#!/bin/sh

# this program copies the yyvlyx_o_rec_5233_<number>.slcio files contained in castorDir in eos directory
# this program is issued prompting 'sh castorCopy.sh'
eosDir=/eos/cms/store/cmst3/user/nfoppian/ttbar365Wizard/yyxylv/000/
castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyxylv_o/ILD/REC/00005352/000/

for ((job=610;job<612;job++));
  do 
  echo "JOB "$job
  # writes JOB and the job number as the job is run
  slcioFile="yyxylv_o_rec_5352_"${job}".slcio"
  # assigns the progressive name of slcioFile
  fileToCopy=$castorDir$slcioFile
xrdcp root://castorcms//$fileToCopy root://eoscms/$eosDir
done
