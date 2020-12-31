import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os

directory = './data'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file = os.path.join(directory, filename)
        print(file)
        data_obj = json.load(open(file, 'rt'))
        time = filename[7:filename.__len__()-5]
        print(time)
        year = time[:4]
        month = time[5:7]
        day = time[8:10]
        hour = time[11:13]
        minute = time[14:16]
        second = time[17:19]
        print("year:  {0}\n".format(year) + \
              "month: {0}\n".format(month) + \
              "day:   {0}\n".format(day) + \
              "hour:  {0}\n".format(hour) + \
              "minute:{0}\n".format(minute) + \
              "second:{0}\n".format(second))

    else:
        continue