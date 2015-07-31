#!/bin/sh

castorDir=/castor/cern.ch/grid/ilc/prod/clic/365gev/yyvlyx_o/ILD/REC/00005233/001/

#ultimo file 1418

for ((job=1000;job<1003;job++));
  do
  echo "JOB "$job
  slcioFile="yyvlyx_o_rec_5233_"${job}".slcio"
  fileToStage=$castorDir$slcioFile
  nsls $fileToStage
  stager_qry -M $fileToStage
  stager_get -M $fileToStage
done
