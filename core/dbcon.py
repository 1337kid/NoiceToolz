import os,psycopg2
from core.config import DB_USER,DB_HOST,DB_PASS,DB_PORT,DB_NAME

def get_db_connection():
    connection = psycopg2.connect(host=DB_HOST,port=DB_PORT,database=DB_NAME,user=DB_USER,password=DB_PASS)
    cursor = connection.cursor()
    return connection,cursor

def setup_db():
    conn,cur=get_db_connection()
    cur.execute(open("schema.sql", "r").read())
    conn.commit()
    conn.close()

def admin_db_select(table_name):
    conn,cur=get_db_connection()
    cur.execute(f'select id from {table_name}')
    data=cur.fetchall()
    conn.close()
    return data

def admin_db_remove(table_name,_id):
    conn,cur=get_db_connection()
    q="delete from {} where id = ".format(table_name,_id)
    cur.execute(q+'%s',(_id,))
    conn.commit()
    conn.close()