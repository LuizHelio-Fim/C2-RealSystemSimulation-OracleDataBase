import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

# Corrigir as variáveis de ambiente - usar nomes de variáveis ao invés de valores
ORACLE_USER = os.getenv('ORACLE_USER', 'labdatabase')
ORACLE_PASS = os.getenv('ORACLE_PASS', 'lab@Database2025') 
ORACLE_DSN = os.getenv('ORACLE_DSN', 'localhost:1521/XEPDB1')
POOL_MIN = int(os.getenv('POOL_MIN', 1))
POOL_MAX = int(os.getenv('POOL_MAX', 5))

try:
    pool = oracledb.create_pool(user=ORACLE_USER,
                                password=ORACLE_PASS,
                                dsn=ORACLE_DSN,
                                min=POOL_MIN,
                                max=POOL_MAX,
                                increment=1,
                                encoding="UTF-8")
    print(f"Pool de conexões Oracle criado com sucesso: {ORACLE_DSN}")
except Exception as e:
    print(f"Erro ao criar pool de conexões Oracle: {e}")
    pool = None

def get_connection():
    """Obtém uma conexão do pool de conexões"""
    if pool is None:
        raise Exception("Pool de conexões não foi inicializado")
    try:
        return pool.acquire()
    except Exception as e:
        raise Exception(f"Erro ao obter conexão do pool: {e}")

def release_connection(conn):
    """Libera a conexão de volta para o pool"""
    if pool and conn:
        try:
            pool.release(conn)
        except Exception as e:
            print(f"Erro ao liberar conexão: {e}")

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