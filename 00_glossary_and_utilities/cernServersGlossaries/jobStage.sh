#!/bin/sh

# this program copies the tt_rec_5485_<number>.slcio files contained in castorDir from tape to disk (mantaining them in the same directory)
# this program is issued prompting 'sh jobCopy.sh'
# eosDir=/store/cmst3/user/pjanot/ttbar365Pythia/
castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/tt/ILD/REC/00005485/000/

for ((job=1;job<3;job++));
  do 
  echo "JOB "$job
  # writes JOB and the job number as the job is run
  slcioFile="tt_rec_5485_"${job}".slcio"
  # assigns the progressive name of slcioFile
  eosFile="tt_"${job}".slcio"
  fileToStage=$castorDir$slcioFile
  # stage = pick from tape and put on disk
  nsls $fileToStage
  # it is ls command on castor?
  stager_qry -M $fileToStage
  # checks if the command has already been submitted?
  stager_get -M $fileToStage
  # stager_get -M copies the tape file on disk

  # To copy the staged files on eos, issue the command
  # eos cp -r root://castorcms///castor/cern.ch/grid/ilc/prod/clic/365gev/tt/ILD/REC/00005485/000/ /eos/cms/store/cmst3/user/pjanot/ttbar365Pythia/

done