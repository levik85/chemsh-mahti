#!/bin/bash --login
# ChemShell SLURM batch script

echo "Node list is" $SLURM_NODELIST

export OMP_NUM_THREADS=1

# some things that might be useful
echo
echo SLURM parameters:
echo
echo SLURM_JOBID         = $SLURM_JOBID
echo SLURM_JOB_NODELIST  = $SLURM_JOB_NODELIST
echo SLURM_NNODES        = $SLURM_NNODES
echo SLURMTMPDIR         = $SLURMTMPDIR
echo SLURM_ARRAYID       = $SLURM_ARRAYID
echo SLURM_ARRAY_JOB_ID  = $SLURM_ARRAY_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

NPROCS=`srun --nodes=${SLURM_NNODES} bash -c 'hostname' | wc -l`

echo
echo ChemShell runtime parameters:
echo
echo working directory = $SLURM_SUBMIT_DIR
echo PYTHONPATH        = $PYTHONPATH
echo NPROCS            = $NPROCS
echo WRAPPER           = $CHEMSH_WRAPPER
echo EXEC              = $CHEMSH_EXEC
echo NWORKGROUPS       = $CHEMSH_NWORKGROUPS
echo INPUT             = $CHEMSH_INPUT
echo OUTPUT            = $CHEMSH_OUTPUT

module load netlib-scalapack
ulimit -s unlimited


# use srun preferably to use the allocated resources in a job step
echo $CHEMSH_WRAPPER srun -n $CHEMSH_NPROCS $CHEMSH_EXEC -nwg $CHEMSH_NWORKGROUPS $CHEMSH_INPUT \> $CHEMSH_OUTPUT
#$CHEMSH_WRAPPER mpirun -n $CHEMSH_NPROCS $CHEMSH_EXEC -nwg $CHEMSH_NWORKGROUPS $CHEMSH_INPUT > $CHEMSH_OUTPUT
$CHEMSH_WRAPPER srun -n $CHEMSH_NPROCS $CHEMSH_EXEC -nwg $CHEMSH_NWORKGROUPS $CHEMSH_INPUT > $CHEMSH_OUTPUT

