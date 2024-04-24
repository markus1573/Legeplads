#!/bin/sh

### -- specify queue --
#BSUB -q gpuv100

### -- set the job Name --
#BSUB -J Fish_model

### -- ask for number of cores (default: 1) min: 4 hvis GPU skal bruges--
#BSUB -n 8 

### -- specify that the cores MUST BE on a single host --
#BSUB -R "span[hosts=1]"

### -- Select the resources: 1 gpu in exclusive process mode --
#BSUB -gpu "num=1:mode=exclusive_process"

### -- set walltime limit: hh:mm --  maximum 24 hours for GPU-queues right now
#BSUB -W 0:30

### request 5GB of system-memory
#BSUB -R "rusage[mem=3GB]"

### -- set the email address --
##BSUB -u your_email_address

### -- send notification at start --
# BSUB -B

### -- send notification at completion--
#BSUB -N

### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --
#BSUB -oo Fish_model.out
#BSUB -eo Fish_model.err

source ~/venv_1/bin/activate
torchrun --standalone --nproc_per_node=1 train.py --name 300_hpc --imgsz 640 --epochs 300 --data fish_data.yaml --weights yolov5s.pt --single-cls --noautoanchor --noplots
