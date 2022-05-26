import io
import paramiko
from paramiko import SSHClient
from scp import SCPClient

numNodes = "4" # change this to match instances

# changing model make sure to change all the parts that have the blend file in order to match
blenderjb = ("#!/bin/bash\n\n"
"#CC -gcpit c2-standard-4\n\n"
"#Slurm HPC Scheduler\n\n"
"#SBATCH -N " + numNodes + "\n\n"
"export SHARED_FS_NAME=/mnt/orangefs \n\n"
"#Uncomment this section for use with openMPI\n\n"
"module add openmpi/3.0.0\n\n"
"cd $SHARED_FS_NAME/blender/blenderjobs\n\n"
"mpiexec /software/blender/3.10/blender -b bouncingBall.blend -o $SHARED_FS_NAME/blender/frame_#### -E CYCLES -F png  -a \n\n")

f = open("blender_render.txt", "w")
f.write(blenderjb)
f.close()

#open and read the file after the appending:
f = open("blender_render.txt", "r")
print(f.read()) 

command = "df"

# Update the next three lines with your
# server's information

host = "35.196.90.221"
username = "ccqadmin" # change varable
password = "hackHPC9"  # set variable

# the belo section actually runs a command 
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

scp = SCPClient(client.get_transport())
scp.put('bouncingBall.blend', recursive=True, remote_path='/mnt/orangefs/blender/blenderjobs')
# Downloading files to the server
#scp.get('CommandWorks.txt')


_stdin, _stdout,_stderr = client.exec_command("cd /mnt/orangefs/blender/blenderjobs; ccqsub blender_render.txt;") 

print( _stdout.read().decode())

 #The below code will be were you place the ffmpeg all you have to do is uncomment anf place the ffmpeg command in place of "df"
#_stdin, _stdout,_stderr = client.exec_command("ccqstat") 
#print( _stdout.read().decode())
client.close()


