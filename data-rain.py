# *_*coding:utf-8 *_*
#

import csv
import os

import numpy as np
from netCDF4 import Dataset, OrderedDict

'''
Note:

email: modianorserver@gmail.com
QQ:    345563121

If you have any questions, 
you can contact me through the above methods.

36.650001525878906N，104.05000305175781E（成都）
36.04999923706055N，103.44999694824219E（兰州）
23.25N，113.1500015258789E（广州）
39.94999694824219N，116.44999694824219E（北京）
30.44999885559082N，121.05000305175781E（上海）

After some calculations .... I got it
cross_time_list = ['0300', '0330', '0400', '0430', '0500', '0530', '0600', '0630', '0700', '0730']
point_dict = {'成都':[36.650001525878906,104.05000305175781],'兰州':[36.04999923706055,103.44999694824219],'广州':[23.25,113.35000610351562],'北京':[39.94999694824219,116.44999694824219],'上海':[30.44999885559082N,121.05000305175781]}
'''

data_rain_url = 'G:\\data\\rain'
tb_time_start = len('3B-HHR-E.MS.MRG.3IMERG.20160701-S')
tb_year_month_day_start = len('3B-HHR-E.MS.MRG.3IMERG.')
rain_years = os.listdir(data_rain_url)

cross_time_list = ['0300', '0330', '0400', '0430', '0500', '0530', '0600', '0630', '0700', '0730']

f_cd_rain = open(file='data/rain/cd_rain.csv', mode='w+')
f_lz_rain = open(file='data/rain/lz_rain.csv', mode='w+')
f_gz_rain = open(file='data/rain/gz_rain.csv', mode='w+')
f_bj_rain = open(file='data/rain/bj_rain.csv', mode='w+')
f_sh_rain = open(file='data/rain/sh_rain.csv', mode='w+')

writer_cd_rain = csv.writer(f_cd_rain)
writer_lz_rain = csv.writer(f_lz_rain)
writer_gz_rain = csv.writer(f_gz_rain)
writer_bj_rain = csv.writer(f_bj_rain)
writer_sh_rain = csv.writer(f_sh_rain)

cities_dict = {'成都': [36.650001525878906, 104.05000305175781], '兰州': [36.04999923706055, 103.44999694824219],
               '广州': [23.25, 113.1500015258789], '北京': [39.95000076293945, 116.44999694824219],
               '上海': [30.450000762939453, 121.05000305175781]}
f_rain_csv_dict = {'成都': writer_cd_rain, '兰州': writer_lz_rain, '广州': writer_gz_rain, '北京': writer_bj_rain,
                   '上海': writer_sh_rain}

for year in rain_years:
    dir_ys = os.path.join(data_rain_url, year)
    for root, dirs, files in os.walk(dir_ys):
        for file in files:
            tb_file = os.path.join(root, file)
            tb_time = file[tb_time_start:tb_time_start + 4]
            if not tb_time in cross_time_list:
                continue

            print('正在处理 {} ....'.format(tb_file))
            dataset_3B: Dataset = Dataset(filename=tb_file, mode='r')

            variables_3B: OrderedDict = dataset_3B.variables

            latitude_3B = np.array(variables_3B['lat'])
            longitude_3B = np.array(variables_3B['lon'])
            for city in cities_dict:
                point = cities_dict[city]
                index_la = np.argwhere(latitude_3B == point[0])
                index_lo = np.argwhere(longitude_3B == point[1])
                if not index_la.size == 0 and not index_lo.size == 0:
                    precipitationCal_3B = np.array(variables_3B['precipitationCal'])[index_lo[0][0]][
                        index_la[0][0]]  # (1800, 3600)
                    csv_writer = f_rain_csv_dict[city]
                    csv_writer.writerow([precipitationCal_3B.tolist()])
f_cd_rain.close()
f_lz_rain.close()
f_gz_rain.close()
f_bj_rain.close()
f_sh_rain.close()
