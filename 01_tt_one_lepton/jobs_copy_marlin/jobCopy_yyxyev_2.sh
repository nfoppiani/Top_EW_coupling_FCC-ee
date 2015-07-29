#!/bin/sh
#661 files
for ((job=1;job<662;job++));
  do 
  echo "JOB "$job 
  slcioFile="yyxyev_o_rec_5248_"${job}".slcio"
  eos cp -r root://castorcms////castor/cern.ch/grid/ilc/prod/clic/365gev/yyxyev_o/ILD/REC/00005248/000/$slcioFile /eos/cms/store/cmst3/user/nfoppian/ttbar365Wizard/yyxyev/
done
