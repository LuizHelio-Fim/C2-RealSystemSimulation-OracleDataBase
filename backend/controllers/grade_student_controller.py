from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('grade_student', __name__)

def refresh_grade_student_table():
    """Atualiza completamente a tabela GRADE_ALUNO com todas as matrículas dos alunos"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Limpar a tabela atual (será repovoada)
        cur.execute("DELETE FROM GRADE_ALUNO")
        
        # Buscar todos os alunos e todas as ofertas para criar as matrículas
        # Aqui vamos assumir que um aluno se matricula em ofertas do seu curso
        sql_students_offers = """
        SELECT DISTINCT a.MATRICULA, o.ID as ID_OFERTA, a.STATUS_CURSO
        FROM ALUNO a
        CROSS JOIN OFERTA o
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        WHERE a.COURSE_ID = m.ID_CURSO
        """
        
        cur.execute(sql_students_offers)
        enrollments = cur.fetchall()
        
        # Para cada combinação aluno-oferta, inserir a matrícula
        for student_id, offer_id, student_status in enrollments:
            
            # Inserir na tabela GRADE_ALUNO (sem MEDIA_FINAL)
            insert_sql = """
            INSERT INTO GRADE_ALUNO (ID_ALUNO, ID_OFERTA, STATUS) 
            VALUES (""" + str(student_id) + """, """ + str(offer_id) + """, '""" + str(student_status) + """')
            """
            cur.execute(insert_sql)
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar tabela GRADE_ALUNO: {str(e)}")
        return False
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/enrollments/refresh', methods=['POST'])
def refresh_enrollments():
    """Endpoint para forçar a atualização da tabela GRADE_ALUNO"""
    try:
        success = refresh_grade_student_table()
        if success:
            return jsonify({'message': 'Tabela GRADE_ALUNO atualizada com sucesso'}), 200
        else:
            return jsonify({'error': 'Erro ao atualizar tabela GRADE_ALUNO'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/enrollments', methods=['GET'])
def list_enrollments():
    """Listar todas as matrículas (auto-populadas)"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT ga.ID_ALUNO as MATRICULA, ga.ID_OFERTA, ga.STATUS,
               a.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
               p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE
        FROM GRADE_ALUNO ga
        JOIN ALUNO a ON ga.ID_ALUNO = a.MATRICULA
        JOIN OFERTA o ON ga.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        ORDER BY a.NOME, o.ANO DESC, o.SEMESTRE DESC, m.NOME
        """
        cur.execute(sql)
        rows = cur.fetchall()
        enrollments = []
        for row in rows:
            enrollments.append({
                'matricula': row[0],  # Changed from id_aluno to matricula
                'id_oferta': row[1],
                'status': row[2],
                'aluno_nome': row[3],
                'materia_nome': row[4],
                'curso_nome': row[5],
                'professor_nome': row[6],
                'ano': row[7],
                'semestre': row[8]
            })
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matrículas: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/enrollments/<int:student_id>/<int:offer_id>', methods=['GET'])
def get_enrollment(student_id, offer_id):
    """Buscar matrícula específica"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT ga.ID_ALUNO as MATRICULA, ga.ID_OFERTA, ga.STATUS,
               a.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
               p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE
        FROM GRADE_ALUNO ga
        JOIN ALUNO a ON ga.ID_ALUNO = a.MATRICULA
        JOIN OFERTA o ON ga.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE ga.ID_ALUNO = """ + str(student_id) + """ AND ga.ID_OFERTA = """ + str(offer_id) + """
        """
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            enrollment = {
                'matricula': row[0],  # Changed from id_aluno to matricula
                'id_oferta': row[1],
                'status': row[2],
                'aluno_nome': row[3],
                'materia_nome': row[4],
                'curso_nome': row[5],
                'professor_nome': row[6],
                'ano': row[7],
                'semestre': row[8]
            }
            return jsonify(enrollment), 200
        return jsonify({'error': 'Matrícula não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar matrícula: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

# Note: UPDATE and DELETE methods removed since Grade_Aluno is now auto-populated
# Status comes from Student table and Media_Final is automatically calculated

@bp.route('/students/<int:student_id>/enrollments', methods=['GET'])
def get_student_enrollments(student_id):
    """Buscar todas as matrículas de um aluno"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT ga.ID_ALUNO as MATRICULA, ga.ID_OFERTA, ga.STATUS,
               a.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
               p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE
        FROM GRADE_ALUNO ga
        JOIN ALUNO a ON ga.ID_ALUNO = a.MATRICULA
        JOIN OFERTA o ON ga.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE ga.ID_ALUNO = """ + str(student_id) + """
        ORDER BY o.ANO DESC, o.SEMESTRE DESC, m.NOME
        """
        cur.execute(sql)
        rows = cur.fetchall()
        enrollments = []
        for row in rows:
            enrollments.append({
                'matricula': row[0],  # Changed from id_aluno to matricula
                'id_oferta': row[1],
                'status': row[2],
                'aluno_nome': row[3],
                'materia_nome': row[4],
                'curso_nome': row[5],
                'professor_nome': row[6],
                'ano': row[7],
                'semestre': row[8]
            })
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matrículas do aluno: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/<int:offer_id>/enrollments', methods=['GET'])
def get_offer_enrollments(offer_id):
    """Buscar todas as matrículas de uma oferta"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT ga.ID_ALUNO as MATRICULA, ga.ID_OFERTA, ga.STATUS,
               a.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
               p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE
        FROM GRADE_ALUNO ga
        JOIN ALUNO a ON ga.ID_ALUNO = a.MATRICULA
        JOIN OFERTA o ON ga.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE ga.ID_OFERTA = """ + str(offer_id) + """
        ORDER BY a.NOME
        """
        cur.execute(sql)
        rows = cur.fetchall()
        enrollments = []
        for row in rows:
            enrollments.append({
                'matricula': row[0],  # Changed from id_aluno to matricula
                'id_oferta': row[1],
                'status': row[2],
                'aluno_nome': row[3],
                'materia_nome': row[4],
                'curso_nome': row[5],
                'professor_nome': row[6],
                'ano': row[7],
                'semestre': row[8]
            })
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matrículas da oferta: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
