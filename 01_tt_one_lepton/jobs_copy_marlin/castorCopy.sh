#!/bin/sh

# this program copies the yyvlyx_o_rec_5233_<number>.slcio files contained in castorDir in eos directory
# this program is issued prompting 'sh castorCopy.sh'
eosDir=/eos/cms/store/cmst3/user/tpajero/ttbar365Wizard/yyvlyx/000/
castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyvlyx_o/ILD/REC/00005233/000/

for ((job=77;job<78;job++));
  do 
  echo "JOB "$job
  # writes JOB and the job number as the job is run
  slcioFile="yyvlyx_o_rec_5233_"${job}".slcio"
  # assigns the progressive name of slcioFile
  fileToCopy=$castorDir$slcioFile
xrdcp root://castorcms//$fileToCopy root://eoscms/$eosDir
done

# DOES NOT WORK! PRINTS: DOES NOT KNOW COMMAND EOS