# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ketian"
__time__ = "Oct 2017"

from glob import glob
import os


def read_res_violation(result_name):

    print ("\nwe are analyzing {}".format(result_name))

    f = open(result_name, 'r')
    viloate = 'Violated'

    run_succ_identify = 'Collecting slicing Results'
    has_result = False

    for line in f.readlines():
        if run_succ_identify in line:
            has_result = True
            break
    has_result = True
    if not has_result:
        print ("no result runned out")
        return None

    violated_rules = []
    f = open(result_name, 'r')
    for line in f.readlines():
        line = line.strip()
        if viloate in line:
            #print (line)
            rule = line.lower().split(':')[0].split(' ')[-1]
            violated_rules.append(rule)

    print ("Violated rules as")
    print (violated_rules)
    return violated_rules

def get_results_from_a_dir(dire):
    start_dir = dire
    pattern = "*.txt"

    files = []
    for dir, _, _ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir, pattern)))

    return files


def run_analysis(dire):
    files = get_results_from_a_dir(dire)
    rules = list()
    for f in files:
        r = read_res_violation(f)
        rules.extend(r)


if __name__ == "__main__":
    dire = "/media/fbeyond/APPs/sazzCryp/NewApps/Result/"
    dire = "/media/fbeyond/APPs/sazzCryp/NewsApp_mid/Result/"
    #run_analysis(dire)
    f = "ranger.v2.log"
    read_res_violation(f)