# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:06:29 2021

@author: Lenovo
"""

"""

把txt文件转化为csv文件
"""
# -*-coding:utf-8 -*-

import csv

with open('D:/data/t_logp/08102508-3008/2700.csv', 'w+', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    # 读要转换的txt文件，文件每行各词间以字符分隔
    with open('D:/data/t_logp/08102508-3008/2700.txt', 'r', encoding='utf-8') as filein:
        for line in filein:
            line_list = line.strip('\n').split(' ')   #我这里的数据之间是以空格间隔的
            spamwriter.writerow(line_list)
