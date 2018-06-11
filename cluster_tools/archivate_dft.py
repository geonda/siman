"""
archivate_dft.py by Aksyonov Dmitry, Skoltech, Moscow

1. rsync home directory to backup storage
2. remove all auxilary DFT files from home directory for finished calculations
"""
import sys
import subprocess, datetime, os, glob
# print sys.argv
# sys.path.append('/usr/lib64/python2.7/site-packages/numpy')
# import numpy as np

BACKUP_STORAGE = '/storage/amg/aksenov/'
RETURN_DIRS_COMMAND = """squeue -o '%o' | awk -F / '{$(NF--)} {gsub(/\s+/,FS)};  $0 '""" # queue specific command that return directories of active calculations
AUX_FILES_TEMPL = ['*CHG*', '*DOS*', '*WAV*', '*run.xml*', '*AEC*', '*OSZ*', '*POT*'] # template for auxilary files to remove

def runBash(cmd, env = None, detached = False):
    """Input - string; Executes Bash commands and returns stdout
    Need: import subprocess
    """
    if detached:
        stdout = None
        stderr = None
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT

    # printlog('running in BASH:', cmd)
    my_env = os.environ.copy()
    # my_env["PATH"] = "/opt/local/bin:/opt/local/sbin:" + my_env["PATH"]
    p = subprocess.Popen(cmd, 
        # executable='/bin/bash', 
        shell=True, stdout=stdout, stderr = stderr, stdin = None, env = my_env)
    # print (cmd)
    # print 'Bash output is\n'+out
    # print ( str(out, 'utf-8') ) 
    out = ''
    try:
        out = p.stdout.read().strip()

        out = str(out, 'utf-8')
    except:
        pass

    return out  #This is the stdout from the shell command



with open('arhivate_dft.log', 'a') as f:

    """1. Archivate files with rsync"""
    f.write("\nStart rsync at "+str(datetime.datetime.now())+'\n')
    # out = runBash('rsync -r LiCoO2 '+ BACKUP_STORAGE)
    out = runBash('rsync -r * .'+ BACKUP_STORAGE)
    f.write('rsync out: '+out+'\n')
    f.write("Finished rsync at "+str(datetime.datetime.now())+'\n')



    """2. Remove aux files with find from inactive dirs"""
    active_directories = []
    out = runBash(RETURN_DIRS_COMMAND)
    # print(out)
    active_directories = out.splitlines()[1:]

    curpath = sys.path[0]

    active_directories = [d.replace(curpath+'/', '').split('/')[0] for d in active_directories]

    # print(active_directories)
    dirs = filter(os.path.isdir, os.listdir(curpath)) # return list of directories in current folder
    # print(dirs)
    for d in dirs:
        if d in active_directories:
            continue

        for tem in AUX_FILES_TEMPL:
            out = runBash('find '+d+' -name '+tem+' -delete' )
            f.write('find out: '+out+'\n')

            # print(out)