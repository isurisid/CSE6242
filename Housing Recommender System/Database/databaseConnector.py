from distutils.command.config import config
import psycopg2
from configparser import ConfigParser
from sqlalchemy import create_engine
import pandas as pd 


def initialize_config():
    global db_info
    config=ConfigParser()
    config.read("DBSettings.ini")
    db_info=config['DBCredentials']

def connect_to_db():
    conn_string = db_info['db_url']
    db = create_engine(conn_string)
    conn = db.connect()
    return conn

def add_df_to_db(conn):
    conn_string = db_info['db_url']
    df = pd.read_csv("../ML/rp/data/v2-HousingRecommenderFinalDataset.csv")
    df.to_sql('public."CountyData"', con=conn, if_exists='replace',index=False)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    return conn
'''
def connect_to_db():
    conn=psycopg2.connect(database=db_info['db_name'],user=db_info['user'],password=db_info['password'],host=db_info['host'],port=db_info['port'])
    return conn
'''

initialize_config()
conn=connect_to_db()
conn=add_df_to_db(conn)
cursor = conn.cursor()
  
sql1 = '''select * from public."CountyData" limit 10;'''
cursor.execute(sql1)
for i in cursor.fetchall():
    print(i)
conn.close()

#cursor=conn.cursor()
#cursor.execute('Select * from public."CountyData" limit 10')
#print(cursor.description)