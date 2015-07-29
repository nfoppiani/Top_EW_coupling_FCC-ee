#!/bin/sh

#eosDir=/store/cmst3/user/nfoppian/ttbar365Wizard/yyveyx/
castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyveyx_o/ILD/REC/00005251/000/

#672 files

for ((job=1;job<3;job++));
  do
  echo "JOB "$job
  slcioFile="yyveyx_o_rec_5251_"${job}".slcio"
  #eosFile="yyveyx_o_"${job}".slcio"
  fileToStage=$castorDir$slcioFile
  nsls $fileToStage
  stager_qry -M $fileToStage
  stager_get -M $fileToStage
  # To copy the staged files on eos, issue the command
  # eos cp -r root://castorcms////castor/cern.ch/grid/ilc/prod/clic/365gev/yyveyx_o/ILD/REC/00005251/000/ /eos/cms/store/cmst3/user/nfoppian/ttbar365Wizard/yyveyx/
done
