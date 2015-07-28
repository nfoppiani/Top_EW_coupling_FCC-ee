#!/bin/sh

eosDir=/store/cmst3/user/pjanot/ttbar365Pythia/

for ((job=1;job<3;job++));
  do
  #echo "JOB "$job
  name="ttbarPythia_"${job}
  slcioFilename="tt_rec_5485_"${job}".slcio"
  ntupleFilename="tt_"${job}".root"
  logFilename="log_"${job}".txt"
  echo $slcioFilename

  sed -e "s/==FILENAME==/${slcioFilename}/" steer.xml > tmp_steer
#Start to write the script
  cat > job_${name}.sh << EOF
#!/bin/sh
# . /cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-07/init_ilcsoft.sh
cmsStage $eosDir$slcioFilename .
cp /afs/cern.ch/user/p/pjanot/public/forNicoloAndTommaso/clic_ild_cdr500.gear .
cp -r /afs/cern.ch/user/p/pjanot/public/forNicoloAndTommaso/lcfiweights .
cp -r /afs/cern.ch/user/p/pjanot/public/forNicoloAndTommaso/vtxprob .
# Write the steering.xml file to be run in batch
cat > TEST_steering.xml << "EOF"
EOF

#Ajoute the temporary steering file to the steering file
  cat  tmp_steer>> job_${name}.sh

# Close the steering file
  echo "EOF" >> job_${name}.sh
  cat >> job_${name}.sh << EOF
# Execute the steering file
Marlin TEST_steering.xml >& log

# Copy the ntuple and the log file on disk
cmsStage -f ntuple.root $eosDir$ntupleFilename
cmsStage -f log $eosDir$logFilename

EOF
  chmod 755 job_${name}.sh
  bsub -q 1nh -J $name $PWD/job_${name}.sh


done
