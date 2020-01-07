# *_*coding:utf-8 *_*
import os
import csv
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

data_cloud_url = 'G:\\data\\cloud'
data_rain_url = 'G:\\data\\rain'
tb_start = len('3B-HHR-E.MS.MRG.3IMERG.20160701-S')
nc_start = len('NC_H08_20160701_')
cloud_months = os.listdir(data_cloud_url)
rain_years = os.listdir(data_rain_url)

cross_time_list = ['0300', '0330', '0400', '0430', '0500', '0530', '0600', '0630', '0700', '0730']
cities_dict = {'成都': [36.650001525878906, 104.05000305175781], '兰州': [36.04999923706055, 103.44999694824219],
               '广州': [23.25, 113.1500015258789], '北京': [39.94999694824219, 116.44999694824219],
               '上海': [30.44999885559082, 121.05000305175781]}

f_cd_cloud = open(file='data/cloud/cd_cloud.csv', mode='w+')
f_lz_cloud = open(file='data/cloud/lz_cloud.csv', mode='w+')
f_gz_cloud = open(file='data/cloud/gz_cloud.csv', mode='w+')
f_bj_cloud = open(file='data/cloud/bj_cloud.csv', mode='w+')
f_sh_cloud = open(file='data/cloud/sh_cloud.csv', mode='w+')

writer_cd_cloud = csv.writer(f_cd_cloud)
writer_lz_cloud = csv.writer(f_lz_cloud)
writer_gz_cloud = csv.writer(f_gz_cloud)
writer_bj_cloud = csv.writer(f_bj_cloud)
writer_sh_cloud = csv.writer(f_sh_cloud)

f_cloud_csv_dict = {'成都': writer_cd_cloud, '兰州': writer_lz_cloud, '广州': writer_gz_cloud, '北京': writer_bj_cloud,
                    '上海': writer_sh_cloud}

for ms in cloud_months:
    days = os.listdir(os.path.join(data_cloud_url, ms))
    for ds in days:
        hours = os.listdir(os.path.join(os.path.join(data_cloud_url, ms), ds))
        for hs in hours[3:8]:
            dir_hs = os.path.join(os.path.join(os.path.join(data_cloud_url, ms), ds), hs)
            for root, dirs, files in os.walk(dir_hs):
                for file in files:
                    nc_file = os.path.join(root, file)
                    nc_time = file[nc_start:nc_start + 4]

                    if not nc_time in cross_time_list:
                        continue

                    print('正在处理 {} ....'.format(nc_file))

                    dataset_NC: Dataset = Dataset(filename=nc_file, mode='r')
                    variables_NC: OrderedDict = dataset_NC.variables

                    latitude_NC = np.array(variables_NC['latitude'])

                    longitude_NC = np.array(variables_NC['longitude'])

                    for city in cities_dict.keys():
                        point = cities_dict[city]
                        index_la = np.argwhere(latitude_NC == point[0])
                        index_lo = np.argwhere(longitude_NC == point[1])
                        index_la = index_la[0][0]
                        index_lo = index_lo[0][0]

                        if not index_la.size == 0 and not index_lo.size == 0:
                            clot_NC = np.array(variables_NC['CLOT'])[index_lo][index_la]

                            cltt_NC = np.array(variables_NC['CLTT'])[index_lo][index_la]

                            clth_NC = np.array(variables_NC['CLTH'])[index_lo][index_la]

                            cler_NC = np.array(variables_NC['CLER_23'])[index_lo][index_la]

                            csv_writer = f_cloud_csv_dict[city]

                            csv_writer.writerow(
                                [clot_NC.tolist(), cltt_NC.tolist(), clth_NC.tolist(), cler_NC.tolist()])
f_sh_cloud.close()
f_sh_cloud.close()
f_sh_cloud.close()
f_sh_cloud.close()
f_sh_cloud.close()