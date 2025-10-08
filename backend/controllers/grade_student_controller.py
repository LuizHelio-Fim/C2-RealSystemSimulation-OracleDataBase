from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('grade_student', __name__)

@bp.route('/enrollments', methods=['POST'])
def enroll_student():
    """Matricular aluno em uma oferta"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['id_aluno', 'id_oferta', 'status']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        id_aluno = data.get("id_aluno")
        id_oferta = data.get("id_oferta")
        status = data.get("status")
        media_final = data.get("media_final")

        try:
            # Verificar se o aluno existe
            # VULNERÁVEL: Verificar se aluno existe
            sql_check_aluno = "SELECT COUNT(1) FROM ALUNO WHERE MATRICULA = " + str(id_aluno)
            cur.execute(sql_check_aluno)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Aluno não encontrado'}), 404

            # Verificar se a oferta existe
            # VULNERÁVEL: Verificar se oferta existe
            sql_check_oferta = "SELECT COUNT(1) FROM OFERTA WHERE ID = " + str(id_oferta)
            cur.execute(sql_check_oferta)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Oferta não encontrada'}), 404

            # Verificar se já existe matrícula
            cur.execute("SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_ALUNO = " + str(id_aluno) + " AND ID_OFERTA = " + str(id_oferta))
            if cur.fetchone()[0] > 0:
                return jsonify({'error': 'Aluno já está matriculado nesta oferta'}), 400

            sql = "INSERT INTO GRADE_ALUNO (ID_ALUNO, ID_OFERTA, STATUS, MEDIA_FINAL) VALUES (" + str(id_aluno) + ", " + str(id_oferta) + ", '" + str(status) + "', " + str(media_final) + ")"
            cur.execute(sql)
            conn.commit()
            return jsonify({'message': 'Aluno matriculado com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao matricular aluno: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/enrollments', methods=['GET'])
def list_enrollments():
    """Listar todas as matrículas"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT ga.ID_ALUNO, ga.ID_OFERTA, ga.STATUS, ga.MEDIA_FINAL,
               a.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
               p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE
        FROM GRADE_ALUNO ga
        JOIN ALUNO a ON ga.ID_ALUNO = a.MATRICULA
        JOIN OFERTA o ON ga.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        ORDER BY a.NOME, o.ANO DESC, o.SEMESTRE DESC
        """
        cur.execute(sql)
        rows = cur.fetchall()
        enrollments = []
        for row in rows:
            enrollments.append({
                'id_aluno': row[0],
                'id_oferta': row[1],
                'status': row[2],
                'media_final': row[3],
                'aluno_nome': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
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
        SELECT ga.ID_ALUNO, ga.ID_OFERTA, ga.STATUS, ga.MEDIA_FINAL,
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
                'id_aluno': row[0],
                'id_oferta': row[1],
                'status': row[2],
                'media_final': row[3],
                'aluno_nome': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
            }
            return jsonify(enrollment), 200
        return jsonify({'error': 'Matrícula não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar matrícula: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/enrollments/<int:student_id>/<int:offer_id>', methods=['PUT'])
def update_enrollment(student_id, offer_id):
    """Atualizar matrícula (status e média final)"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # Verificar se a matrícula existe
            cur.execute("SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_ALUNO = " + str(student_id) + " AND ID_OFERTA = " + str(offer_id))
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Matrícula não encontrada'}), 404

            # Construir query de atualização dinamicamente
            update_fields = []
            
            if 'status' in data:
                update_fields.append("STATUS = '" + str(data['status']) + "'")
            
            if 'media_final' in data:
                update_fields.append("MEDIA_FINAL = " + str(data['media_final']))

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = "UPDATE GRADE_ALUNO SET " + ', '.join(update_fields) + " WHERE ID_ALUNO = " + str(student_id) + " AND ID_OFERTA = " + str(offer_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({'message': 'Matrícula atualizada com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar matrícula: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/enrollments/<int:student_id>/<int:offer_id>', methods=['DELETE'])
def delete_enrollment(student_id, offer_id):
    """Cancelar matrícula"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se existem notas para esta matrícula
        cur.execute("SELECT COUNT(1) FROM AVALIACAO_ALUNO aa JOIN AVALIACAO a ON aa.ID_AVALIACAO = a.ID WHERE aa.ID_ALUNO = " + str(student_id) + " AND a.ID_OFERTA = " + str(offer_id))
        grade_count = cur.fetchone()[0]
        if grade_count > 0:
            return jsonify({'error': 'Não é possível cancelar matrícula com notas cadastradas'}), 400

        # Verificar se a matrícula existe
        cur.execute("SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_ALUNO = " + str(student_id) + " AND ID_OFERTA = " + str(offer_id))
        enrollment_exists = cur.fetchone()[0]
        if enrollment_exists == 0:
            return jsonify({'error': 'Matrícula não encontrada'}), 404
        
        # VULNERÁVEL: Deletar matrícula
        sql = "DELETE FROM GRADE_ALUNO WHERE ID_ALUNO = " + str(student_id) + " AND ID_OFERTA = " + str(offer_id)
        cur.execute(sql)
        conn.commit()
        return jsonify({'message': 'Matrícula cancelada com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao cancelar matrícula: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/students/<int:student_id>/enrollments', methods=['GET'])
def get_student_enrollments(student_id):
    """Buscar todas as matrículas de um aluno"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT ga.ID_ALUNO, ga.ID_OFERTA, ga.STATUS, ga.MEDIA_FINAL,
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
                'id_aluno': row[0],
                'id_oferta': row[1],
                'status': row[2],
                'media_final': row[3],
                'aluno_nome': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
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
        SELECT ga.ID_ALUNO, ga.ID_OFERTA, ga.STATUS, ga.MEDIA_FINAL,
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
                'id_aluno': row[0],
                'id_oferta': row[1],
                'status': row[2],
                'media_final': row[3],
                'aluno_nome': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
            })
        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matrículas da oferta: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
