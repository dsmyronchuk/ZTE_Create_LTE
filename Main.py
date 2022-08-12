import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from jinja2 import Template
from Secret import *
from Cell_Obj import CellObj


user_bs_name = input('Enter Name BS: ').replace(' ', '_')
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


for index, row in df_all_cell.iterrows():
    if str(row['Channel']) in user_standard:
        CellObj(row, dct_standard, user_bs_type)


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

#for i in CellObj.lte_cell:
#    for k, v in i.__dict__.items():
#        print(k, v)
#    print()

temp_parametr = Template(open('template/LTE_parametr.txt').read())
file_parametr = temp_parametr.render(SubNetwork=user_subnetwork,
                                     MEID=user_meid,
                                     list_cell=CellObj.lte_cell)


file = open('file_render_tst.txt', 'w')
file.write(file_parametr)

