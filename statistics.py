# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ketian"
__time__ = "Oct 2017"



flow = 'low_app_summary.txt'
ftop = 'top_app_summary.txt'

import io
import ast




def statistics_low(fname):
    category = ['AUTO', 'BEAUTY', 'BOOK_AND_REFRENCE', 'BUSINESS', 'COMICS']
    out = {i:[] for i in category}

    f = io.open(fname, mode="r", encoding="utf-8")

    cate = ''
    res = ''
    for line in f.readlines():
        line = line.strip()
        #print (line)
        if line.startswith('we are analyzing'):
            for c in category:
                if c in line:
                    cate = c
                    break

        if line.startswith('no result'):
            res = 'fail'

        if line.startswith('['):
            res = ast.literal_eval(line)

        if len(line) == 0:
            out[cate].append(res)

    #print (res)
    out[cate].append(res)

    #print (out)
    for i in out:
        print ('LOW',i,len(out[i]))

    return out


def statistics_top(fname):
    category = ['AUTO', 'BEAUTY', 'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS']
    out = {i:[] for i in category}

    f = io.open(fname, mode="r", encoding="utf-8")

    cate = ''
    res = ''
    for line in f.readlines():
        line = line.strip()
        #print (line)
        if line.startswith('we are analyzing'):
            for c in category:
                if c in line:
                    cate = c
                    break

        if line.startswith('no result'):
            res = 'fail'

        if line.startswith('['):
            res = ast.literal_eval(line)

        if len(line) == 0:
            out[cate].append(res)

    #print (res)
    out[cate].append(res)

    #print (out)
    for i in out:
        print ('TOP', i, len(out[i]))

    return out


import collections
import numpy as np

def analyze_dict(adict):

    total = []
    average = []
    for i in adict:
        fail = 0
        suc = 0

        l = adict[i]
        alist = list()
        nums = list()
        run_out = 0

        for j in l:
            if j == 'fail':
                fail += 1
            else:
                suc += 1
                tmp = list()
                for t in j:
                    if not 'a' in t:
                        tmp.append(t)
                alist.extend(list(tmp))
                nums.append(len(tmp))
                run_out += 1


        ct = collections.Counter(alist)

        print ("frequent run for ",i, len(alist))
        for j,t in ct.most_common(3):
            print (j, t, float(ct[j])/len(alist))

        print (i, 'SUC', suc, 'FAIL', fail)
        print (i, np.mean(nums), np.var(nums))
        average.append(np.mean(nums))
        total.extend(list(alist))

    print ('a', average)
    '''
    cct = collections.Counter(total)
    print ('final',cct)
    tt = 0
    for i in cct:
        tt += cct[i]
    print ('total', tt)

    t = ['2', '13', '7', '3', '6', '1', 'others']
    t_dic = {i:0 for i in t}

    for i in cct:
        if i in t:
            t_dic[i] = cct[i]
        else:
            t_dic['others'] += cct[i]

    
    for j in t_dic:
        t_dic[j] = float(t_dic[j]+0.0)/tt

    res = []
    for key in t:
        res.append(t_dic[key])

    print ('',res)
    '''


if __name__ == "__main__":
    low = statistics_low(flow)
    top = statistics_top(ftop)

    #print ('LOW')
    #analyze_dict(low)


    print ('TOP')
    analyze_dict(top)