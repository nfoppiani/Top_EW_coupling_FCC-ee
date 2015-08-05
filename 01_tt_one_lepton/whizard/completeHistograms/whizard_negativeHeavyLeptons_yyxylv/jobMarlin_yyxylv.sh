#!/bin/sh

eosDir1=/store/cmst3/user/nfoppian/ttbar365Wizard/yyxylv/000/
eosDir2=/store/cmst3/user/tpajero/ttbar365Whizard/yyxylv/000/

# 999 files (from 1 to 999)
# 411 files (from 1000 to 1410)

# missing from 804
# missing 1367, 1368

for ((job=1;job<2;job++));
  do
  echo "JOB "$job
  name="yyxylv_wizard_o_"${job}
  slcioFilename="yyxylv_o_rec_5352_"${job}".slcio"
  ntupleFilename="yyxylv_o_"${job}".root"
  logFilename="log_"${job}".txt"
  echo $slcioFilename

  sed -e "s/==FILENAME==/${slcioFilename}/" steer.xml > tmp_steer
#Start to write the script
  cat > job_${name}.sh << EOF
#!/bin/sh
# . /cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-07/init_ilcsoft.sh
cmsStage $eosDir1$slcioFilename .
cp /afs/cern.ch/user/t/tpajero/work/public/firstExample/clic_ild_cdr500.gear .
cp -r /afs/cern.ch/user/t/tpajero/work/public/firstExample/lcfiweights .
cp -r /afs/cern.ch/user/t/tpajero/work/public/firstExample/vtxprob .
# Write the steering.xml file to be run in batch
cat > TEST_steering.xml << "EOF"
EOF

# Ajoute the temporary steering file to the steering file
  cat  tmp_steer>> job_${name}.sh

# Close the steering file
  echo "EOF" >> job_${name}.sh
  cat >> job_${name}.sh << EOF
# Execute the steering file
Marlin TEST_steering.xml >& log

# Copy the ntuple and the log file on disk
cmsStage -f ntuple.root $eosDir2$ntupleFilename
cmsStage -f log $eosDir2$logFilename

EOF
  chmod 755 job_${name}.sh
  bsub -q 1nh -J $name $PWD/job_${name}.sh

done