#!/bin/sh

#eosDir=/store/cmst3/user/nfoppian/ttbar365Wizard/yyxyev/
castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyxyev_o/ILD/REC/00005248/000/

#661 files

for ((job=1;job<3;job++));
  do
  echo "JOB "$job
  slcioFile="yyxyev_o_rec_5248_"${job}".slcio"
  #eosFile="yyxyev_o_"${job}".slcio"
  fileToStage=$castorDir$slcioFile
  nsls $fileToStage
  stager_qry -M $fileToStage
  stager_get -M $fileToStage
  # To copy the staged files on eos, issue the command
  # eos cp -r root://castorcms////castor/cern.ch/grid/ilc/prod/clic/365gev/yyxyev_o/ILD/REC/00005248/000/ /eos/cms/store/cmst3/user/nfoppian/ttbar365Wizard/yyxyev/
done
