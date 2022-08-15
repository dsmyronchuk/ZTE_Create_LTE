import pandas as pd
import pyodbc
import os
import datetime
from jinja2 import Template
from Secret import *
from Cell_Obj import CellObj


user_bs_name = input('Enter Name BS: ').replace(' ', '_')
user_choice = input('Enter type of work (Create, Create_transfer, parameter): ')
user_standard = input('Enter LTE standart(1700, 2900, 3676): ').replace(' ', '').split(',')
user_bs_type = input('Enter type BS (GL City; GL Rural; GUL City; GUL Rural): ')
user_subnetwork = input('Enter SubNetwork: ')
user_meid = input('Enter MEID: ')


dct_standard = {}
for i in user_standard:
    standard_mhz = input(f'Enter bandwidth for frequency {i}: ')
    dct_standard[i] = standard_mhz

query_all_cell = Template(open('template/SQL_All_Cell.txt').read()).render(bs_name=user_bs_name)
query_csfb = Template(open('template/SQL_csfb_ho.txt').read()).render(bs_name=user_bs_name.replace('_', ' '))

connect_rpdb = pyodbc.connect(rpdb_db)
df_all_cell = pd.read_sql(query_all_cell, connect_rpdb)
df_csfb = pd.read_sql(query_csfb, connect_rpdb)


if user_choice.lower() != 'parameter':      # Если нужно создать не только параметры
    print("EquipmentFunction input format: 51=1,4; 52=1,4")


for index, row in df_all_cell.iterrows():
    if str(row['Channel']) in user_standard:
        CellObj(row, dct_standard, user_bs_type, user_choice)


for index, row in df_all_cell.iterrows():
    for i in CellObj.lte_cell:
        if i.CoSectorName == row['Site Name'] and i.Azimuth == row['Azimuth'] and i.CI != row['CI']:
            i.CoSectorCI = row['CI']
            i.csfb_arfcn.append(row['Channel'])       # start ARFCN

for index, row in df_csfb.iterrows():
    for i in CellObj.lte_cell:
        if i.CoSectorCI == row['Cell_ID'] and row['Target BCCH'] not in i.csfb_arfcn:
            i.csfb_arfcn.append(row['Target BCCH'])

CellObj.correct_arfcn_list()

# Рендер и запить скриптов в файлы
path_folder = f'C://Python/ZTE_LTE/{user_bs_name[:11]} {datetime.datetime.now().date()}'
os.mkdir(path_folder)

temp_parameter = Template(open('template/LTE_parameter.txt').read())
rend_parameter = temp_parameter.render(SubNetwork=user_subnetwork,
                                       MEID=user_meid,
                                       list_cell=CellObj.lte_cell)

file_parameter = open(f'{path_folder}/Parameter_{user_bs_name[:11]}.txt', 'w')
file_parameter.write(rend_parameter)


if user_choice.lower() != 'parameter':
    temp_cell = Template(open('template/Create LTE Cell.txt').read())
    rend_cell = temp_cell.render(SubNetwork=user_subnetwork,
                                 MEID=user_meid,
                                 list_cell=CellObj.lte_cell)
    file_cell = open(f'{path_folder}/Create_LTE__{user_bs_name[:11]}.txt', 'w')
    file_cell.write(rend_cell)

