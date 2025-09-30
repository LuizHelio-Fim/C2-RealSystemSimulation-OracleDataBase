import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

ORACLE_USER = os.getenv('labdatabase')
ORACLE_PASS = os.getenv('lab@Database2025')
ORACLE_DSN = os.getenv('XEPDB1')
POOL_MIN = int(os.getenv('POOL_MIN', 1))
POOL_MAX = int(os.getenv('POOL_MAX', 5))

pool = oracledb.create_pool(user=ORACLE_USER,
                            password=ORACLE_PASS,
                            dsn=ORACLE_DSN,
                            min=POOL_MIN,
                            max=POOL_MAX,
                            increment=1,
                            encoding="UTF-8")

def get_connection():
    # Obtém uma conexão do pool de conexões
    return pool.acquire()

def release_connection(conn):
    # Libera a conexão de volta para o pool
    pool.release(conn)

def next_seq_val(sequence_name: str, conn=None):
    # Obtém o próximo valor de uma sequência
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True
    cur = conn.cursor()
    cur.execute(f"SELECT {sequence_name}.NEXTVAL FROM dual")
    val = cur.fetchone()[0]
    cur.close()
    if close_conn:
        release_connection(conn)
    return val