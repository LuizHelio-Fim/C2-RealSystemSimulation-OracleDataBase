from db.db_conn import get_connection, release_connection, next_seq_val
from datetime import datetime

def format_date_for_oracle(dt_str):
    """Convert date from 'DD/MM/YYYY' to 'YYYY-MM-DD' format or NULL."""
    if not dt_str:
        return 'NULL'
    try:
        datetime.strptime(dt_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("A data deve estar no formato 'YYYY-MM-DD'.")
    return dt_str

def create_student(matricula, nome, data_nasc=None, cpf=None, telefone=None, email=None, periodo=None, course_id=None, status_curso=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        new_id = next_seq_val("seq_student", conn)
        sql = """
        INSERT INTO student (id, matricula, cpf, nome, data_nasc, telefone, email, periodo, course_id, status_curso)
        VALUES (:id, :matricula, :cpf, :nome,
                CASE WHEN :data_nasc IS NULL THEN NULL ELSE TO_DATE(:data_nasc,'YYYY-MM-DD') END,
                :telefone, :email, :periodo, :course_id, :status_curso)
        """
        cur.execute(sql, {
            'id': new_id,
            'matricula': matricula,
            'cpf': cpf,
            'nome': nome,
            'data_nasc': format_date_for_oracle(data_nasc),
            'telefone': telefone,
            'email': email,
            'periodo': periodo,
            'course_id': course_id,
            'status_curso': status_curso
        })
        conn.commit()
        return new_id
    finally:
        cur.close()
        release_connection(conn)

def list_students():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT id, matricula, cpf, nome, TO_CHAR(data_nasc, 'YYYY-MM-DD'), telefone, email, periodo, course_id, status_curso FROM student"
        cur.execute(sql)
        rows = cur.fetchall()
        students = []
        for row in rows:
            students.append({
                'id': row[0],
                'matricula': row[1],
                'cpf': row[2],
                'nome': row[3],
                'data_nasc': row[4],
                'telefone': row[5],
                'email': row[6],
                'periodo': row[7],
                'course_id': row[8],
                'status_curso': row[9]
            })
        return students
    finally:
        cur.close()
        release_connection(conn)

def get_student_by_id(student_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT id, matricula, cpf, nome, TO_CHAR(data_nasc, 'YYYY-MM-DD'), telefone, email, periodo, course_id, status_curso FROM student WHERE id = :id"
        cur.execute(sql, {'id': student_id})
        row = cur.fetchone()
        if row:
            return {
                'id': row[0],
                'matricula': row[1],
                'cpf': row[2],
                'nome': row[3],
                'data_nasc': row[4],
                'telefone': row[5],
                'email': row[6],
                'periodo': row[7],
                'course_id': row[8],
                'status_curso': row[9]
            }
        return None
    finally:
        cur.close()
        release_connection(conn)

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(1) FROM grade_aluno where aluno_id = :id", {'id': student_id})
        cnt = cur.fetchone()[0]
        if cnt > 0:
            return False, "Aluno possui notas matricula e não pode ser excluído, remova-as antes."
        sql = "DELETE FROM student WHERE id = :id", {'id': student_id}
        cur.execute(sql, {'id': student_id})
        conn.commit()
        return cur.rowcount, None
    finally:
        cur.close()
        release_connection(conn)
