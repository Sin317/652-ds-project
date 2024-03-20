import numpy as np
import pickle
from collections import defaultdict
from multiprocessing import Process, Pool
import sys
import os
from os import path
import csv
import pandas as pd

batchfile = '../../data/alibaba-trace-2017/batch_instance.csv'
outdirectory = './alibabatimeseries2017f/'

def main():
    print("started")
    for chunk in pd.read_csv(batchfile, chunksize=1000, index_col = False, names = ['starttime','endtime','job id','task id','machine id','status', 'sequence number','total sequence number','max cpu','avg cpu','max memory','avg memory']):
        chunk.fillna(0,inplace=True)
        for index, row in chunk.iterrows():
            if row['status']=='Terminated':
                directory_path = outdirectory+str(int(row['job id']))+"/"
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                f = open(directory_path+str(int(row['task id'])),"a+")
                f.write("%d,%d,%d,%d,%d,%s,%d,%d,%f,%f,%f,%f\n"%(row['starttime'],row['endtime'],row['job id'],row['task id'],row['machine id'],row['status'],row['sequence number'],row['total sequence number'],row['max cpu'],row['avg cpu'],row['max memory'],row['avg memory']))
                f.close()         

if __name__== "_main_":
    main()