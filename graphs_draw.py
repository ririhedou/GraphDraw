__author__ = "ketian"

import sys
sys.path.append('../')


import glob
import re
import collections
import operator

#iframe distributions in a website
iframes = {1: 174537, 2: 45573, 3: 16742, 4: 8090, 5: 4327, 6: 2941, 7: 2015, 8: 1744, 9: 1139, 10: 1092,
 11: 1374, 12: 793, 13: 559, 14: 395, 15: 389, 16: 608, 17: 355, 18: 287, 19: 234, 20: 309, 21: 462, 22: 149, 23: 169, 24: 68,
 25: 70, 26: 67, 27: 50, 28: 36, 29: 41, 30: 49, 31: 49, 32: 29, 33: 24, 34: 11, 35: 12, 36: 19, 37: 13, 38: 14, 39: 22, 40: 17,
 41: 15, 42: 19, 43: 11, 44: 6, 45: 12, 46: 10, 47: 6, 48: 6, 49: 4, 50: 9, 51: 9, 52: 5, 53: 4, 54: 3, 55: 4, 56: 2, 57: 4, 58: 4,
 59: 2, 60: 3, 61: 3, 62: 1, 64: 2, 65: 1, 66: 5, 67: 4, 69: 1, 70: 1, 72: 1, 73: 3, 74: 4, 76: 2, 77: 3, 78: 1, 79: 1, 82: 2, 86: 1,
87: 1, 88: 1, 89: 2, 90: 2, 91: 1, 94: 1, 98: 1, 101: 1, 102: 1, 104: 1, 109: 1, 114: 1, 119: 1, 125: 1, 135: 1, 142: 1, 143: 1, 144:
1, 146: 2, 152: 1, 162: 1, 172: 1, 173: 1, 180: 1, 191: 1, 198: 2, 200: 1, 204: 1, 210: 1, 214: 1, 228: 1, 258: 1, 271: 1, 283: 1, 336: 1}

scripts = {4: 58700, 3: 57505, 5: 54907, 6: 52645, 2: 51434, 7: 48545, 8: 44415, 1: 43459, 9: 41352, 10: 37520, 11: 32218,
           12: 29176, 13: 25758, 14: 22876, 15: 20223, 16: 18128, 17: 16047, 18: 14258, 19: 12836, 20: 11583, 21: 10407, 22: 9594,
           23: 8550, 24: 7333, 25: 6813, 26: 6259, 27: 5546, 28: 5135, 29: 4595, 30: 4123, 31: 3715, 32: 3314, 33: 2957, 34: 2796,
           35: 2470, 36: 2065, 37: 1974, 38: 1710, 39: 1609, 40: 1432, 41: 1284, 42: 1172, 43: 1042, 44: 957, 45: 852, 46: 717,
           47: 674, 48: 659, 49: 579, 50: 518, 51: 489, 52: 377, 53: 350, 54: 297, 55: 283, 56: 258, 57: 221, 58: 206, 59: 173, 60: 171,
           61: 157, 63: 138, 62: 135, 64: 130, 65: 113, 66: 111, 67: 82, 68: 75, 70: 68,
           71: 63, 69: 62, 72: 58, 76: 51, 74: 39, 79: 39, 75: 38, 98: 38, 99: 35, 77: 34, 102: 34, 103: 33, 93: 32, 73: 31, 97: 31, 78: 30, 100: 27, 95: 23, 101: 23, 106: 23,
           91: 22, 94: 22, 96: 22, 108: 22, 82: 20, 105: 20, 107: 19, 111: 19, 115: 19, 81: 18, 86: 18, 84: 17, 90: 17, 92: 17, 104: 17, 80: 16, 83: 16, 85: 16, 87: 16, 88: 16,
           109: 16, 110: 16, 116: 13, 112: 12, 114: 11, 89: 10, 113: 10, 176: 10, 117: 9, 170: 9, 172: 8, 180: 8, 121: 6, 173: 6, 175: 6, 182: 6, 118: 5, 119: 5, 123: 5, 169: 5,
           171: 5, 122: 4, 127: 4, 129: 4, 134: 4, 174: 4, 183: 4, 120: 3, 124: 3, 128: 3, 130: 3, 135: 3, 151: 3, 162: 3, 167: 3, 177: 3, 184: 3, 188: 3, 125: 2, 137: 2, 150: 2,
           152: 2, 161: 2, 166: 2, 280: 2, 131: 1, 133: 1, 1027: 1, 144: 1, 148: 1, 153: 1, 154: 1, 158: 1, 160: 1, 178: 1, 179: 1, 181: 1, 189: 1, 191: 1, 192: 1, 201: 1, 207: 1,
           208: 1, 211: 1, 214: 1, 216: 1, 218: 1, 221: 1, 232: 1, 233: 1, 238: 1, 256: 1, 257: 1, 266: 1, 272: 1, 275: 1, 276: 1, 279: 1, 282: 1, 297: 1, 299: 1, 308: 1, 1694: 1}

####################
#Validate External
Iframe_external_src = {1: 163670, 2: 35898, 3: 11910, 4: 5589, 5: 3019, 6: 2032, 7: 1366, 8: 1197, 10: 898, 9: 745, 11: 689, 12: 473, 13: 286, 15: 240, 16: 204, 14: 199, 20: 138, 18: 110, 17: 96, 21: 87, 22: 66, 19: 58, 23: 47, 24: 46, 25: 44, 26: 35, 30: 32, 29: 30, 27: 27, 28: 25, 36: 25, 32: 21, 33: 19, 38: 19, 31: 18, 37: 17, 35: 12, 34: 10, 39: 10, 40: 10, 42: 10, 51: 9, 43: 7, 44: 7, 45: 7, 50: 6, 48: 5, 41: 4, 46: 4, 49: 4, 52: 4, 58: 4, 47: 3, 54: 3, 55: 3, 66: 3, 67: 3, 73: 3, 76: 3, 53: 2, 56: 2, 57: 2, 60: 2, 64: 2, 65: 2, 74: 2, 77: 2, 198: 2, 59: 1, 62: 1, 68: 1, 72: 1, 79: 1, 86: 1, 87: 1, 90: 1, 91: 1, 94: 1, 98: 1, 102: 1, 108: 1, 119: 1, 125: 1, 142: 1, 143: 1, 144: 1, 152: 1, 162: 1, 168: 1, 173: 1, 191: 1, 193: 1, 204: 1, 210: 1, 214: 1, 228: 1, 258: 1, 271: 1, 283: 1, 336: 1}
Script_external_src = {1: 173041, 2: 117517, 3: 83562, 4: 57456, 5: 40000, 6: 27657, 7: 19423, 8: 13864, 9: 11442, 10: 9251, 11: 5848, 12: 4662, 13: 3373, 14: 2884, 15: 2251, 16: 1850, 17: 1451, 18: 1328, 19: 1115, 20: 1038, 21: 874, 22: 786, 23: 664, 24: 637, 25: 589, 26: 547, 28: 446, 27: 424, 29: 381, 30: 356, 31: 330, 32: 289, 33: 221, 34: 196, 35: 191, 37: 167, 36: 153, 38: 144, 40: 128, 39: 117, 43: 108, 41: 103, 42: 86, 45: 80, 49: 76, 44: 74, 48: 74, 47: 69, 46: 68, 50: 61, 54: 32, 53: 31, 52: 30, 55: 28, 60: 27, 51: 26, 56: 25, 57: 19, 58: 17, 59: 15, 62: 15, 65: 13, 66: 13, 71: 13, 61: 12, 67: 11, 64: 10, 69: 9, 74: 9, 79: 9, 68: 8, 73: 8, 75: 6, 115: 6, 63: 5, 72: 5, 77: 5, 76: 4, 80: 4, 86: 4, 92: 4, 101: 4, 102: 4, 116: 4, 82: 3, 89: 3, 99: 3, 105: 3, 70: 2, 83: 2, 90: 2, 93: 2, 95: 2, 97: 2, 100: 2, 109: 2, 111: 2, 78: 1, 81: 1, 85: 1, 87: 1, 91: 1, 96: 1, 98: 1, 103: 1, 104: 1, 106: 1, 108: 1, 110: 1, 112: 1, 113: 1, 114: 1, 117: 1, 122: 1, 128: 1, 136: 1, 149: 1, 151: 1, 154: 1, 162: 1, 166: 1, 173: 1, 188: 1, 222: 1, 248: 1, 262: 1}


#########categories
static_iframe_dic = {u'blogs and personal sites': 7807, u'message boards and forums. malicious web sites': 1, u'social web - linkedin': 50, u'search engines and portals': 1712, u'organizational email': 6, u'streaming media': 20891, u'advertisements': 28098, u'online brokerage and trading': 264, u'dynamic content': 2338, u'personal network storage and backup': 4535, u'newly registered websites': 208, u'cultural institutions': 21, u'government': 694, u'web chat': 1239, u'peer-to-peer file sharing': 38, u'social networking': 4551, u'general email': 15, u'message boards and forums': 1653, u'web and email spam. parked domain': 1, u'prescribed medications': 1, u'real estate': 339, u'professional and worker organizations': 66, u'compromised websites. news and media': 9, u'educational materials': 656, u'service and philanthropic organizations': 91, u'job search': 133, u'reference materials': 9400, u'sex': 4834, u'advocacy groups. potentially unwanted software': 5, u'entertainment video': 63, u'message boards and forums. compromised websites': 1, u'political organizations': 13, u'entertainment': 805, u'adult content': 643, u'sport hunting and gun clubs': 5, u'adult material': 15, u'weapons': 13, u'health': 93, u'content delivery networks': 352, u'social and affiliation organizations': 8, u'social web - twitter': 1679, u'malicious web sites. business and economy': 3, u'internet auctions': 105, u'malicious web sites': 40, u'pay-to-surf': 86, u'information technology': 20024, u'educational video': 20, u'web and email spam': 9, u'games': 1163, u'streaming media. web and email spam': 2, u'malicious web sites. information technology': 4, u'compromised websites': 42, u'phishing and other frauds': 9, u'illegal or questionable': 34, u'web infrastructure': 157, u'web and email marketing': 489, u'web analytics': 108595, 'unknown': 1883, u'parked domain': 191, u'sports': 694, u'sports. compromised websites': 1, u'militancy and extremist': 8, u'hacking. compromised websites': 1, u'intolerance': 4, u'text and media messaging': 4, u'shopping': 2344, u'tasteless': 19, u'web hosting': 1559, u'financial data and services': 2162, u'computer security': 2, u'pro-life': 1, u'potentially unwanted software': 1, u'internet radio and tv': 1761, u'dynamic dns': 6, u'social web - facebook': 56846, u'social web - youtube': 106534, u'elevated exposure': 142, u'hacking': 46, u'gambling. compromised websites': 1, u'malicious web sites. sex': 6, u'nutrition': 5, u'malicious web sites. parked domain': 35, u'suspicious content': 69, u'malicious web sites. sports': 2, u'hobbies': 9, u'non-traditional religions': 51, u'business and economy': 5679, u'educational institutions': 149, u'personals and dating': 55, u'lingerie and swimsuit': 1, u'collaboration - office': 15, u'media file download': 688, u'traditional religions': 198, u'travel': 1179, u'surveillance': 28, u'gambling': 430, u'web collaboration': 24, u'application and software download': 324, u'uncategorized': 4528, u'news and media': 2785, u'hosted business applications': 1359, u'society and lifestyles': 489, u'streaming media. compromised websites': 3, u'advocacy groups': 5, u'alcohol and tobacco': 1, u'restaurants and dining': 14, u'web images': 22, u'gay or lesbian or bisexual interest': 6, u'vehicles': 514}
#dyanmic_ifram_dic = {u'blogs and personal sites': 6, u'professional and worker organizations': 2, u'compromised websites': 3, u'newly registered websites': 4, u'advertisements. compromised websites': 1, u'educational materials': 7, u'service and philanthropic organizations': 6, u'job search': 5, u'reference materials': 15, u'sex': 113, u'search engines and portals': 80, u'organizational email': 79, u'elevated exposure': 3, u'suspicious content': 3, u'business and economy': 399, u'educational institutions': 17, u'illegal or questionable': 2, u'web infrastructure': 4, u'web and email marketing': 8, u'social web - linkedin': 1, u'collaboration - office': 3, u'media file download': 7, u'traditional religions': 7, u'web analytics': 12, u'instant messaging': 2, u'entertainment': 22, u'personals and dating': 1, 'unknown': 114, u'travel': 48, u'streaming media': 63, 'advertisements': 3898, u'adult material': 1, u'sports': 14, u'weapons': 2, u'online brokerage and trading': 2, u'dynamic content': 40, u'health': 11, u'social and affiliation organizations': 1, u'gambling': 5, u'social web - twitter': 4, u'web collaboration': 2, u'application and software download': 5, u'internet auctions': 3, u'uncategorized': 189, u'nutrition': 1, u'text and media messaging': 2, u'alternative journals': 1, u'shopping': 95, u'cultural institutions': 1, u'government': 16, u'news and media': 56, u'web chat': 6, u'hosted business applications': 20, u'restaurants and dining': 1, u'society and lifestyles': 49, u'pay-to-surf': 2, u'web hosting': 11, u'financial data and services': 103, u'malicious web sites. parked domain': 1, u'alcohol and tobacco': 1, u'internet telephony': 1, u'social networking': 39, u'general email': 7, u'information technology': 455, u'educational video': 1, u'message boards and forums': 18, u'website translation': 14, u'internet radio and tv': 9, u'vehicles': 10, u'social web - facebook': 216, u'social web - youtube': 181, u'games': 16, u'real estate': 7, u'military': 1, u'hacking': 1, u'personal network storage and backup': 8, u'non-traditional religions': 3, u'adult content': 18, u'advocacy groups': 1}
dyanmic_ifram_dic = {u'newly registered websites': 4, u'blogs and personal sites': 3, u'compromised websites': 3, u'social web - linkedin': 1, u'suspicious content': 2, u'educational materials': 1, u'service and philanthropic organizations': 4, u'job search': 3, u'reference materials': 11, u'sex': 47, u'search engines and portals': 77, u'organizational email': 80, u'elevated exposure': 9, u'non-traditional religions': 1, u'business and economy': 365, u'educational institutions': 6, u'illegal or questionable': 2, u'web infrastructure': 6, u'web and email marketing': 8, u'media file download': 5, u'traditional religions': 2, u'web analytics': 12, u'entertainment': 14, 'unknown': 97, u'travel': 55, u'streaming media': 74, 'advertisements': 4741, u'adult material': 1, u'sports': 14, u'weapons': 1, u'online brokerage and trading': 2, u'dynamic content': 40, u'health': 5, u'gambling': 5, u'social web - twitter': 6, u'application and software download': 5, u'internet auctions': 6, u'uncategorized': 156, u'shopping': 73, u'instant messaging': 1, u'government': 3, u'news and media': 37, u'hosted business applications': 24, u'advertisements. compromised websites': 1, u'web chat': 7, u'society and lifestyles': 37, u'pay-to-surf': 2, u'web hosting': 10, u'financial data and services': 88, u'malicious web sites. parked domain': 2, u'social networking': 39, u'general email': 7, u'information technology': 461, u'educational video': 9, u'message boards and forums': 15, u'website translation': 38, u'internet radio and tv': 11, u'vehicles': 4, u'social web - facebook': 350, u'social web - youtube': 321, u'games': 16, u'real estate': 9, u'hacking': 2, u'personal network storage and backup': 12, u'adult content': 2}

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter
from matplotlib import ticker

def count_unique_urls(dic):
    c = 0
    for i in dic:
        c += dic[i]
    print (c)

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(100 * y))
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'

def cum_curve(iframes,scripts,name="ok.png"):

    #iframes = scripts

    def get_x_y_cumy(data):
        keys = sorted(data.keys())
        x, y = [], []
        for i in keys:
            x.append(i)
            y.append(data[i])

        X = x[:]
        Y = y[:]
        sum_y = sum(y)
        y = [(i+0.0)/sum_y for i in y ]
        cum_y = np.cumsum(y).astype("float32")
        return (X,y, cum_y)

    #normalise to a percentage
    (X,Y, cum_y) = get_x_y_cumy(iframes)
    (X1,Y1, cum_y1) = get_x_y_cumy(scripts)

    for i in range(len(X1)):
        print (X1[i],Y1[i],cum_y1[i])

    fig = plt.figure(figsize=(5,7))
    ax = fig.add_subplot(111)

    plt.tick_params(axis='both', which='major', labelsize=15)

    ax.semilogx(X,cum_y, 'go-', label="Iframe", linewidth=10.0)
    ax.semilogx(X1,cum_y1, 'r--', label="Script", linewidth=10.0)

    plt.xlim(0, 1100)
    plt.grid(linestyle='dotted')

    formatter = FuncFormatter(to_percent)

    plt.gca().yaxis.set_major_formatter(formatter)
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))


    plt.legend(loc="lower right", prop={'size': 15})

    #plt.xlabel("External Sources (by URL)", fontsize=15)
    plt.ylabel("CDF Alexa Top 1M", fontsize=15)

    #plt.show()
    plt.tight_layout()
    plt.savefig(name, dpi=fig.dpi)

def draw_pie_char(sizes,labels, colors=None):
    # Data to plot
    if not colors:
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','lightgrey','violet']

    colors = colors[:len(sizes)]
    explode = [0.1]+[0]*(len(sizes)-1)  # explode 1st slice

    import matplotlib as mpl
    plt.gca().axis("equal")
    mpl.rcParams['font.size'] = 20
    # Plot labels=labels,
    plt.pie(sizes, explode=explode,  colors=colors, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def char_static_dict(d):
    c = 0
    new_d = collections.defaultdict(int)

    #merge social web
    for i in d:
        if 'social web' in i:
            new_d['social web'] += d[i]
        else:
            new_d[i] = d[i]
        c += d[i]

    print (c)
    accu = 0
    accu_num = 0
    #sorted_x = sorted(new_d.items(), key=operator.itemgetter(1), reverse=True)

    sizes = []
    percents = []
    labels = []
    t = [u'web analytics', 'social web', u'streaming media', u'advertisements', u'business and economy',
         u'information technology']

    for i in t:
        name, count = i, new_d[i]
        percent = (count+0.0)/c
        accu += percent
        accu_num += count
        print (name,count,percent)
        sizes.append(count)
        labels.append(name)
        percents.append(percent)

    print ('others', c-accu_num,1-accu)
    sizes.append(c-accu_num)
    labels.append('others')
    percents.append(1-accu)

    draw_pie_char(sizes,labels)

    print (labels)
    print (percents)

    return None


def draw_new_pie():

    import matplotlib.pyplot as plt
    import numpy as np

    l =[u'Web', 'Social', u'Media', u'AD', u'Business',
     u'IT', 'others']
    s =[0.26041279486632246, 0.39593439981199535, 0.05009699983933277, 0.0673795175666829, 0.01361834579903168,
     0.04801791799257094, 0.16454002412406388]
    d =[0.0016096579476861167, 0.0909456740442656, 0.009926224010731052, 0.6359490274983233, 0.04896042924211938,
     0.06183769282360831, 0.1507712944332663]

    from matplotlib import rc, pyplot as plt

    # GENERAL STYLE SETTINGS
    font = {'size': 15}
    rc('font', **font)
    rc("figure", facecolor="white")
    rc('axes', edgecolor='darkgray')

    plt.gca().axis("equal")

    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgrey', 'violet', 'red']

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))


    axes[0].pie(s, labels= l,  colors=colors, autopct='%1.1f%%', shadow=True, startangle=0, pctdistance=0.85, radius=1.2)
    axes[1].pie(d, labels= l, colors=colors, autopct='%1.1f%%', shadow=True, startangle=0, pctdistance=0.85, radius=1.2)
    axes[0].set_title('Offline',)
    axes[1].set_title('Online', loc='center')
    #axes[1].legend(l, bbox_to_anchor=(0.5, 0.1), ncol=2, fontsize=15)
    plt.subplots_adjust(wspace=0.4)

    fig.savefig('your_file.png')  # Or whichever format you'd like
    plt.show()


def graph_better_draw():

    l =['2', '13', '7', '3', '6', '1', 'others']

    #low
    d = [0.404, 0.256, 0.084, 0.07333333333333333, 0.05733333333333333, 0.056, 0.06933333333333333]

    #top
    s = [0.5117801047120419, 0.22643979057591623, 0.049738219895287955, 0.051047120418848166, 0.05235602094240838, 0.03534031413612566, 0.07329842931937172]

    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgrey', 'violet', 'orange']
    patterns = ('', '/', 'x', '\\', '.', '', '//')

    import numpy as np
    import matplotlib.pyplot as plt

    people = ('LOW','TOP')
    segments = 7

    # generate some multi-dimensional data & arbitrary labels
    data = []
    for i in range(7):
        data.append((d[i], s[i]))

    y_pos = np.arange(len(people))

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(111)

    patch_handles = []
    left = np.zeros(len(people))  # left alignment of data starts at zero
    for i, d in enumerate(data):
        patch_handles.append(ax.barh(y_pos, d, color=colors[i % len(colors)], align='center',
                             left=left,
                             hatch=patterns[i]))
        # accumulate the left-hand offsets
        left += d


    ax.set_yticks(y_pos)
    ax.set_yticklabels(people, size=20)
    #ax.set_xlabel('Distance')

    plt.legend(patch_handles, l,loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=4, prop={'size': 20})
    #plt.show()
    fig.savefig('par', bbox_inches='tight')

def draw_bar():
    '''
    ('COMICS', 'SUC', 13, 'FAIL', 7)
    ('COMICS', 9.384615384615385, 144.23668639053253)
    ('AUTO', 'SUC', 14, 'FAIL', 6)
    ('AUTO', 9.9285714285714288, 55.637755102040828)
    ('BUSINESS', 'SUC', 18, 'FAIL', 2)
    ('BUSINESS', 13.555555555555555, 207.13580246913577)
    ('BOOKS_AND_REFERENCE', 'SUC', 13, 'FAIL', 7)
    ('BOOKS_AND_REFERENCE', 8.7692307692307701, 46.946745562130175)
    ('BEAUTY', 'SUC', 17, 'FAIL', 3)
    ('BEAUTY', 8.5294117647058822, 67.072664359861591)
    :return:
    '''
    N = 5
    top = [9.384615384615385, 9.9285714285714288, 13.555555555555555, 8.7692307692307701, 8.5294117647058822]
    low = [12.875, 6.416666666666667, 9.8666666666666671, 11.222222222222221, 11.0]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, top, width, color='lightskyblue', hatch="/")

    rects2 = ax.bar(ind + width, low, width, color='y', hatch='\\')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Average Count', size=15)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('COMICS', 'AUTO', 'BUSINESS', 'BOOK', 'BEAUTY'), size=15)

    ax.legend((rects1[0], rects2[0]), ('Top', 'Low'), prop={'size': 15})
    fig.savefig('num_of_rule', bbox_inches='tight')


def plot():
    l = [7, 6, 1, 10, 4, 6, 3, 32, 0, 3, 0, 5, 4, 1, 4, 5, 4, 2, 9, 4, 0, 22, 12, 73, 0, 13, 9, 0, 6, 0, 2, 74, 3, 12, 73, 12, 0, 6, 10, 13, 6, 2, 4, 5, 0, 8, 6, 6, 13, 5, 7, 2, 0, 73, 2, 13, 10, 2, 13, 1, 12, 11, 7, 10, 0, 7, 4, 5, 15, 25, 0, 13, 10, 12, 11, 5, 0, 4, 9, 0, 8, 0, 7, 7, 7, 2, 12, 5, 3, 3, 1, 4, 0, 7, 0, 4, 5, 6, 1, 2]
    _min = min(l)
    _max = max(l)
    import collections
    ct = collections.defaultdict(int)
    for i in l:
        ct[i] += 1
    X,Y =[],[]
    for i in range(_min,_max+1,1):

        X.append(i)
        Y.append(ct[i])

    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(X, Y, width, color='r')

    plt.ylabel('Counter')
    plt.xlabel('Number of rules violated by one app')
    plt.show()


def draw_bar_graph(l):
    violated_rules = list()
    for i in l:
        try:
            t = int(i)
        except:
            rg = ['3a','8a','9a','10a','11a', '14a']
            if i in rg:
                violated_rules.append(i)
            print ("we encount {}".format(i))

    print (violated_rules)
    import collections

    counter = collections.Counter(violated_rules)

    X = counter.keys()
    X.sort()
    Y = list()
    for x in X:
        Y.append(counter[x])

    print (X, Y)

    import numpy as np
    import matplotlib.pyplot as plt

    from matplotlib.ticker import MaxNLocator

    #ax = plt.figure().gca()

    N = len(X)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, Y, width, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Count')
    ax.set_title('Apache Violated Rules end with a')
    ax.set_xticks(ind)
    ax.set_xticklabels(X)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend("violated rules")

    plt.show()

if __name__ == "__main__":

    l = ['13', '13', '13', '13', '13', '13', '2', '2a', '7a', '1', '1a', '13', '13', '2', '2a', '3', '3a', '10', '10a', '7a', '13', '13', '13', '13', '13', '13', '12', '12', '2', '2a', '3', '3a', '7', '7a', '13', '13', '13', '13', '13', '13', '13', '13', '12', '2', '2a', '1', '13', '13', '1a', '13', '13', '13', '13', '13', '13', '12', '12', '12', '12', '12', '12', '12', '12', '12', '12', '4', '4', '4', '4', '4', '4', '4', '6', '6', '6', '6', '6', '6', '2', '2a', '3', '3a', '10', '10a', '7a', '12', '4', '2', '2a', '13', '13', '13', '2', '2a', '7', '7a', '1', '13', '13', '13', '2', '7a', '13', '13', '13', '2', '13', '13', '12', '4', '2', '13', '13', '13', '13', '13', '2', '7a', '13', '13', '13', '13', '13', '13', '12', '4', '2', '2a', '7a', '13', '13', '13', '13', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2', '2a', '3', '3a', '10', '10a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '12', '2', '2a', '3a', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2', '2a', '10', '7a', '1', '1a', '13', '13', '13', '13', '13', '4', '4', '6', '2', '2a', '3', '3a', '10', '10a', '11', '7a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2a', '7', '7a', '13', '2', '2a', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '12', '6', '2', '2a', '3', '3a', '10', '10a', '7', '7a', '13', '4', '2', '3a', '7a', '1', '13', '13', '13', '13', '13', '12', '12', '4', '6', '2', '2a', '3a', '7', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2', '2a', '3', '10', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '12', '2', '2a', '3', '3a', '10a', '7', '7a', '1', '1a', '13', '13', '2', '2a', '3', '3a', '10', '10a', '7a', '1', '1a', '13', '13', '13', '13', '12', '12', '12', '2', '2a', '3', '7a', '1', '1a', '13', '13', '12', '12', '12', '12', '12', '2', '2a', '3', '3a', '10', '10a', '14', '7', '7a', '13', '13', '13', '13', '13', '2a', '7', '13', '2', '2a', '13', '13', '13', '2', '7a', '13', '13', '12', '12', '2', '2a', '1', '1a', '13', '13', '12', '12', '12', '2', '2a', '3', '13', '13', '13', '12', '2', '2a', '7', '13', '13', '13', '13', '13', '2', '2a', '7a', '13', '13', '13', '13', '13', '13', '13', '12', '12', '12', '4', '6', '2', '1a', '13', '13', '2', '2a', '3', '3a', '10', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '2', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2', '2a', '10', '7a', '12', '2', '2a', '7a', '1', '1a', '13', '13', '13', '13', '13', '12', '12', '4', '6', '2', '2a', '3a', '9', '5', '13', '13', '13', '13', '13', '13', '13', '12', '12', '2', '2a', '7a', '13', '2', '2a', '7a', '1a', '13', '13', '13', '13', '13', '12', '12', '12', '4', '6', '2', '2a', '3', '3a', '10', '10a', '2', '7a', '13', '13', '12', '12', '12', '12', '12', '6', '6', '6', '2', '2a', '3a', '5', '13', '13', '13', '12', '12', '12', '4', '6', '2', '2a', '14', '7', '7a', '13', '13', '13', '13', '13', '13', '2', '2a', '7a', '1a', '13', '13', '13', '12', '12', '12', '4', '4', '6', '2', '2a', '14a', '1a', '13', '13', '12', '2', '2a', '3', '3a', '10', '7', '7a', '13', '13', '13', '2', '2a', '13', '13', '12', '4', '2', '1', '13', '13', '12', '12', '12', '12', '12', '4', '4', '4', '6', '2', '2a', '14', '14a', '7', '7a', '1', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '12', '12', '4', '2', '2a', '3', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '12', '12', '2', '2a', '13', '13', '13', '13', '13', '13', '13', '4', '6', '2', '2a', '3a', '7a', '1', '13', '13', '13', '13', '12', '4', '4', '6', '2', '3', '3a', '7', '7a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2', '7a', '1', '1a', '12', '2', '2a', '3', '7a', '13', '13', '13', '13', '13', '13', '13', '13', '2', '2a', '13', '12', '12', '12', '4', '6', '2', '7', '7a', '13', '13', '12', '12', '4', '2', '2a', '7', '7a', '13', '13', '13', '13', '12', '12', '2', '2a', '7a', '13', '13', '13', '13', '12', '2', '2a', '7', '7a', '12', '2', '7a', '1a', '13', '13', '13', '13', '13', '13', '13', '13', '12', '2', '2a', '3', '3a', '10', '10a', '7a', '1a', '13', '13', '2', '3', '3a', '10', '10a', '13', '12', '2', '2a', '13', '12', '2', '2a', '7a', '13', '13', '12', '2', '2a', '7', '7a', '13', '13', '13', '13', '12', '12', '2', '2a', '1', '1a', '12', '2', '2a', '3', '7a', '13', '13', '13', '13', '12', '1', '1a', '13', '13', '2', '2a', '3', '3a', '10', '10a', '7a', '13', '2a', '13', '2']
    l = ['1', '1a', '2', '2a', '3', '3a', '14', '1a', '2a', '3a', '1', '1a', '3', '3a', '7a', '9', '9a', '8', '8a', '13', '13', '13', '14a', '7a', '1a', '13', '13', '2', '3', '3a', '10a', '1', '1a', '13', '13', '9', '8', '1', '3', '1a', '2', '10a', '14', '14a', '1a', '2', '3', '3a', '10', '10a', '6', '7', '7a', '4', '4', '12', '12', '12', '13', '13', '13', '1', '1a', '2', '2a', '3', '3a', '10a', '7', '7a', '7', '7a', '7', '7a', '1a', '2', '3a', '10a', '1a', '2a', '7a', '2a', '5', '7a', '1a', '13', '13', '2', '3', '3a', '10a', '1', '2', '14', '14a', '7a', '1a', '2', '10a', '14', '14a', '1a', '10', '1', '1a', '2', '2a', '3', '3a', '10', '10a', '13', '2', '2a', '3a', '1a', '5', '5', '1a', '13', '13', '7a', '1', '1a', '2', '3', '3a', '14', '14a', '7a', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '13', '2', '2a', '3', '3a', '1', '1a', '2', '3', '3a', '14', '14a', '7a', '1a', '13', '13', '7a']

    draw_bar_graph(l)
    #plot()