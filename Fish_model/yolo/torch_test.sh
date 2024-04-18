#!/bin/sh

### -- specify queue --
#BSUB -q gpuv100

### -- set the job Name --
#BSUB -J Fish_model

### -- ask for number of cores (default: 1) min: 4 hvis GPU skal bruges--
#BSUB -n 4 

### -- specify that the cores MUST BE on a single host --
#BSUB -R "span[hosts=1]"

### -- Select the resources: 1 gpu in exclusive process mode --
#BSUB -gpu "num=1:mode=exclusive_process"

### -- set walltime limit: hh:mm --  maximum 24 hours for GPU-queues right now
#BSUB -W 0:30

### request 5GB of system-memory
#BSUB -R "rusage[mem=5GB]"

### -- set the email address --
##BSUB -u your_email_address

### -- send notification at start --
# BSUB -B

### -- send notification at completion--
#BSUB -N

### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --
#BSUB -o Fish_model.out
#BSUB -e Fish_model.err

source ~/venv_1/bin/activate
torchrun --standalone --nproc_per_node=1 train_HPC.py