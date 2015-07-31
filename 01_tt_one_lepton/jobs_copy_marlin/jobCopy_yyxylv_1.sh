#!/bin/sh

castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyxylv_o/ILD/REC/00005352/000/

#999 files

for ((job=1;job<3;job++));
  do
  echo "JOB "$job
  slcioFile="yyxylv_o_rec_5352_"${job}".slcio"
  fileToStage=$castorDir$slcioFile
  nsls $fileToStage
  stager_qry -M $fileToStage
  stager_get -M $fileToStage
done
