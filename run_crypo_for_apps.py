# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ketian"
__time__ = "Oct 2017"


#CONFIGURATION

JAVA_HOME = "/usr/lib/jvm/java-8-openjdk-amd64/"
ANDROID_SDK_HOME = "/home/fbeyond/program/adt-bundle-linux-x86_64-20140702/sdk/platforms/"

import multiprocessing
import copy
from multiprocessing import Pool
import subprocess
import sys

# TODO multiprocess this process
def multiple_process_with_maximum_core(files,out_dir):

    assert isinstance(files,list)
    assert isinstance(out_dir,str)

    print ("[Stat]TOTALLY we analyze {} files".format(len(files)))

    args_list = []
    for i in files:
        args = dict()
        args['file_path'] = i
        args['out_dir'] = out_dir
        args_list.append(copy.deepcopy(args))
        del args

    n_core = multiprocessing.cpu_count()
    print ("[Stat]The cores we use is {}".format(n_core))

    pool = Pool(n_core)
    pool.map(run_the_app_with_absolute_path, args_list)
    pool.close()
    pool.join()


# TODO single process to do it
def single_process_with_maximum_core(files,out_dir):
    assert isinstance(files,list)
    assert isinstance(out_dir,str)

    print ("[Stat]TOTALLY we analyze {} files".format(len(files)))
    print ("The outpur is here", out_dir)

    args_list = []
    for i in files:
        args = dict()
        args['file_path'] = i
        args['out_dir'] = out_dir
        run_the_app_with_absolute_path(args)
        del args

    print ("Done")


def create_file_to_store_src(outDir, filename, lines):
    fname = outDir+filename.replace('/', '_') + ".txt"
    with open(fname, "wb") as f:
        for i in lines:
             f.write(i+'\n')
        f.flush()
        f.close()
    return


def run_the_app_with_absolute_path(args):
    apk_abs_path = args['file_path']
    out_dir = args['out_dir']

    if not out_dir:
        out_dir = './'

    check_jar = "/media/fbeyond/APPs/sazzCryp/program-analysis-soot/main/build/libs/main.jar"

    cmd = "timeout 6000 /usr/bin/java -jar " + check_jar + " \"apk\"" + " " + "\""+apk_abs_path+"\""

    print ("we are analyzing this file", apk_abs_path, "the output is located at", out_dir)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()

    lines = output.split('\n')
    c = 0
    valid_results = []
    for line in lines:
        line = line.strip()
        if line.startswith("Warning"):
            continue

        else:
            valid_results.append(line)
            c += 1
            c += 1

    if c == 0:
        print ("Not found")
    else:
        print ("we get the output!")
        create_file_to_store_src(out_dir, filename=apk_abs_path, lines=valid_results)

import os
from glob import glob


def get_apks_from_a_dir(dire):

    start_dir = dire
    pattern = "*.apk"

    files = []
    for dir, _, _ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir, pattern)))
    
    files = sorted(files)
    return files


#java -jar main/build/libs/main.jar "apk" "/media/fbeyond/APPs/sazzCryp/NewApps/AUTO/AutoGuard Dash Cam Blackbox_v6.2.4033_apkpure.com.apk"
# python run_crypo_for_apps.py /media/fbeyond/APPs/android6.0/apps/BOOKS_AND_REFERENCE/  /tmp
# python run_crypo_for_apps.py /media/fbeyond/APPs/sazzCryp/NewApps/AUTO/ /media/fbeyond/APPs/sazzCryp/NewApps/Result/

if __name__ == "__main__":
    #args = dict()
    #apk = "/media/fbeyond/APPs/android6.0/apps/BUSINESS/air.com.aes.apk"
    #args['file_path'] = apk
    #args['out_dir'] = None
    #run_the_app_with_absolute_path(args)
    dire = sys.argv[1]
    out = None
    try:
        out = sys.argv[2]
    except:
        out = None

    files = get_apks_from_a_dir(dire)

    #print (files)
    single_process_with_maximum_core(files=files, out_dir=out)
