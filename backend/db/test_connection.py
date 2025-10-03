from db_conn import get_connection, release_connection

try:
    conn = get_connection()
    print("✅ Conexão estabelecida com sucesso!")
    cur = conn.cursor()
    cur.execute("SELECT SYSDATE FROM dual")
    print("Data no Oracle:", cur.fetchone()[0])
    cur.close()
    release_connection(conn)
except Exception as e:
    print("❌ Erro ao conectar:", e)
