# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ketian"
__time__ = "Jan 2018"

from glob import glob
import os

def get_results_from_a_dir(dire):
    start_dir = dire
    pattern = "*.txt"

    files = []
    for dir, _, _ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir, pattern)))

    return files

def analyze_pacakge_from_rule_lines(lines):
    pkgs = list()
    #***Violated Rule 13: Untrused PRNG Found in <e.w.fw: int c()>
    for line in lines:
        if "Violated Rule 13" in line:
            pkg_name = line.split("<",1)[-1].split(":",1)[0]
            pkgs.append(pkg_name)

    pp = list()
    for i in pkgs:
        i = ".".join(i.split('.')[:2])
        pp.append(i)
    import collections
    ct = collections.Counter(pp)
    for i in ct.most_common(100):
        print (i)

def analyze_file(result_name):

    f = open(result_name, 'r')
    lines = [line.strip() for line in f.readlines()]

    if len(lines) < 10:
        #print (result_name, "no result")
        return list()

    violate = "Violated"
    violated_rules = list()

    rule_lines =list()
    for line in lines:
        if violate in line:
            # print (line)
            rule = line.lower().split(':')[0].split(' ')[-1]
            rule_lines.append(line)
            violated_rules.append(rule)

    #analyze_pacakge_from_rule_lines(rule_lines)
    print ("Violated rules as", result_name),
    print (violated_rules)
    return violated_rules



if __name__ == "__main__":
    path = "./res_sa/"
    path = "./apache"
    #t = analyze_file(path + "_media_fbeyond_APPs_sazzCryp_NewApps_COMICS_How_To_Draw_Comics_v1.0.6_apkpure.com.apk.txt")
    #print (t, len(t))


    fs = get_results_from_a_dir(path)
    print ("size of files we analyze", len(fs))
    rs = list()
    for f in fs:
        r = analyze_file(f)
        tmp = list()
        for t in r:
            tmp.append(t)
        rs.extend(tmp)
    print (rs)
