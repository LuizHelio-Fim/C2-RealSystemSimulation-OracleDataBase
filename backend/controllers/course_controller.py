from db.db_conn import get_connection, release_connection, next_seq_val

def create_course(name, carga_horaria_total):
    conn = get_connection()
    cur = conn.cursor()
    try:
        new_id = next_seq_val("seq_course", conn)
        sql = """
        INSERT INTO course (id, name, carga_horaria_total)
        VALUES (:id, :name, :carga_horaria_total)
        """
        cur.execute(sql, {
            'id': new_id,
            'name': name,
            'carga_horaria_total': carga_horaria_total
        })
        conn.commit()
        return new_id
    finally:
        cur.close()
        release_connection(conn)

def list_courses():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT id, name, carga_horaria_total FROM course"
        cur.execute(sql)
        courses = cur.fetchall()
        return [{'id': row[0], 'name': row[1], 'carga_horaria_total': row[2]} for row in courses]
    finally:
        cur.close()
        release_connection(conn)