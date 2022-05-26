numNodes= "4"

blenderjb = ("#!/bin/bash\n\n"
"#CC -gcpit c2-standard-4\n\n"
"#Slurm HPC Scheduler\n\n"
"#SBATCH -N " + numNodes + "\n\n"
"#Shared FS is the same name specified in the CloudyCluster\n"
"#creation wizard when launching the cluster.\n"
"export SHARED_FS_NAME=/mnt/{sFSNAME} \n\n"
"#Blender Source is the directory where blender is installed\n"
"export BLENDER_SOURCE=/software/blender/3.10/\n\n"
"#Blender version for Scheduler\n"
"module add blender/3.10\n\n"
"cd $BLENDER_SOURCE\n"
"mpiexec blender -b $SHARED_FS_NAME/{sBlendDIR}/{sBlendFile} -o "
"$SHARED_FS_NAME'/{sBlendDIR}/frames/frame_#' -E CYCLES -F PNG -a &&\n"
"mpiexec printf '+' >> $SHARED_FS_NAME/{sBlendDIR}/blendDone.txt\n")

f = open("blender_render.txt", "w")
f.write(blenderjb)
f.close()

#open and read the file after the appending:
f = open("blender_render.txt", "r")
print(f.read()) 