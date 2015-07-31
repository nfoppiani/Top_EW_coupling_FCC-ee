#!/bin/sh

castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyvlyx_o/ILD/REC/00005233/000/

#999 files

for ((job=1;job<3;job++));
  do
  echo "JOB "$job
  slcioFile="yyvlyx_o_rec_5233_"${job}".slcio"
  fileToStage=$castorDir$slcioFile
  nsls $fileToStage
  stager_qry -M $fileToStage
  stager_get -M $fileToStage
done
