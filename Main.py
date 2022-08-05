import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from jinja2 import Template
from Secret import *
from Cell_Obj import CellObj


user_bs_name = input('Enter Name BS: ').replace(' ', '_')
user_standard = input('Enter LTE standart(1700, 2900, 3676): ').split(',')
user_subnetwork = input('Enter SubNetwork: ')
user_meid = input('Enter MEID: ')

query_all_cell = Template(open('template/SQL_All_Cell.txt').read()).render(bs_name=user_bs_name)
query_csfb = Template(open('template/SQL_csfb_ho.txt').read()).render(bs_name=user_bs_name.replace('_', ' '))

connect_rpdb = pyodbc.connect(rpdb_db)
df_all_cell = pd.read_sql(query_all_cell, connect_rpdb)
df_csfb = pd.read_sql(query_csfb, connect_rpdb)


for index, row in df_all_cell.iterrows():
    if row['Channel'] in user_standard:
        CellObj(row)

for index, row in df_all_cell.iterrows():
    for i in CellObj.lte_cell:
        if i.CoSectorName == row['Site_Name'] and i.Azimuth == row['Azimuth'] and i.CI != row['CI']:
            i.CoSectorCI = row['CI']
            i.CoSectorARFCN = row['Channel']

