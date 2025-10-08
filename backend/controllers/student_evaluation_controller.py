from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('student_evaluation', __name__)

@bp.route('/student-evaluations', methods=['POST'])
def create_student_evaluation():
    """Cadastrar nota de um aluno em uma avaliação"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['id_avaliacao', 'id_aluno', 'nota']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        id_avaliacao = data.get("id_avaliacao")
        id_aluno = data.get("id_aluno")
        nota = data.get("nota")

        try:
            # Verificar se a avaliação existe
            cur.execute("SELECT COUNT(1) FROM AVALIACAO WHERE ID = " + str(id_avaliacao))
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Avaliação não encontrada'}), 404

            # Verificar se o aluno existe
            cur.execute("SELECT COUNT(1) FROM ALUNO WHERE MATRICULA = " + str(id_aluno))
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Aluno não encontrado'}), 404

            # Verificar se o aluno está matriculado na oferta da avaliação
            cur.execute("SELECT COUNT(1) FROM GRADE_ALUNO ga JOIN AVALIACAO a ON ga.ID_OFERTA = a.ID_OFERTA WHERE ga.ID_ALUNO = " + str(id_aluno) + " AND a.ID = " + str(id_avaliacao))
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Aluno não está matriculado na oferta desta avaliação'}), 400

            # Verificar se já existe nota para esta avaliação
            cur.execute("SELECT COUNT(1) FROM AVALIACAO_ALUNO WHERE ID_AVALIACAO = " + str(id_avaliacao) + " AND ID_ALUNO = " + str(id_aluno))
            if cur.fetchone()[0] > 0:
                return jsonify({'error': 'Já existe nota cadastrada para este aluno nesta avaliação'}), 400

            sql = "INSERT INTO AVALIACAO_ALUNO (ID_AVALIACAO, ID_ALUNO, NOTA) VALUES (" + str(id_avaliacao) + ", " + str(id_aluno) + ", " + str(nota) + ")"
            cur.execute(sql)
            conn.commit()
            return jsonify({'message': 'Nota cadastrada com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao cadastrar nota: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/student-evaluations', methods=['GET'])
def list_student_evaluations():
    """Listar todas as notas de avaliações"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT aa.ID_AVALIACAO, aa.ID_ALUNO, aa.NOTA,
               a.TIPO as AVALIACAO_TIPO, a.PESO as AVALIACAO_PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD') as AVALIACAO_DATA,
               al.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME,
               p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE
        FROM AVALIACAO_ALUNO aa
        JOIN AVALIACAO a ON aa.ID_AVALIACAO = a.ID
        JOIN ALUNO al ON aa.ID_ALUNO = al.MATRICULA
        JOIN OFERTA o ON a.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        ORDER BY al.NOME, a.DATA, a.TIPO
        """
        cur.execute(sql)
        rows = cur.fetchall()
        student_evaluations = []
        for row in rows:
            student_evaluations.append({
                'id_avaliacao': row[0],
                'id_aluno': row[1],
                'nota': row[2],
                'avaliacao_tipo': row[3],
                'avaliacao_peso': row[4],
                'avaliacao_data': row[5],
                'aluno_nome': row[6],
                'materia_nome': row[7],
                'curso_nome': row[8],
                'professor_nome': row[9],
                'ano': row[10],
                'semestre': row[11]
            })
        return jsonify(student_evaluations), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar notas: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/student-evaluations/<int:evaluation_id>/<int:student_id>', methods=['GET'])
def get_student_evaluation(evaluation_id, student_id):
    """Buscar nota específica de um aluno em uma avaliação"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT aa.ID_AVALIACAO, aa.ID_ALUNO, aa.NOTA, a.TIPO as AVALIACAO_TIPO, a.PESO as AVALIACAO_PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD') as AVALIACAO_DATA, al.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE FROM AVALIACAO_ALUNO aa JOIN AVALIACAO a ON aa.ID_AVALIACAO = a.ID JOIN ALUNO al ON aa.ID_ALUNO = al.MATRICULA JOIN OFERTA o ON a.ID_OFERTA = o.ID JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO JOIN CURSO c ON o.ID_CURSO = c.ID JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR WHERE aa.ID_AVALIACAO = " + str(evaluation_id) + " AND aa.ID_ALUNO = " + str(student_id)
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            student_evaluation = {
                'id_avaliacao': row[0],
                'id_aluno': row[1],
                'nota': row[2],
                'avaliacao_tipo': row[3],
                'avaliacao_peso': row[4],
                'avaliacao_data': row[5],
                'aluno_nome': row[6],
                'materia_nome': row[7],
                'curso_nome': row[8],
                'professor_nome': row[9],
                'ano': row[10],
                'semestre': row[11]
            }
            return jsonify(student_evaluation), 200
        return jsonify({'error': 'Nota não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar nota: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/student-evaluations/<int:evaluation_id>/<int:student_id>', methods=['PUT'])
def update_student_evaluation(evaluation_id, student_id):
    """Atualizar nota de um aluno"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        if 'nota' not in data:
            return jsonify({'error': 'Campo nota é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # Verificar se a nota existe
            cur.execute("SELECT COUNT(1) FROM AVALIACAO_ALUNO WHERE ID_AVALIACAO = " + str(evaluation_id) + " AND ID_ALUNO = " + str(student_id))
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Nota não encontrada'}), 404

            sql = "UPDATE AVALIACAO_ALUNO SET NOTA = " + str(data['nota']) + " WHERE ID_AVALIACAO = " + str(evaluation_id) + " AND ID_ALUNO = " + str(student_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({'message': 'Nota atualizada com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar nota: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/student-evaluations/<int:evaluation_id>/<int:student_id>', methods=['DELETE'])
def delete_student_evaluation(evaluation_id, student_id):
    """Deletar nota de um aluno"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se a nota existe
        cur.execute("SELECT COUNT(1) FROM AVALIACAO_ALUNO WHERE ID_AVALIACAO = " + str(evaluation_id) + " AND ID_ALUNO = " + str(student_id))
        evaluation_exists = cur.fetchone()[0]
        if evaluation_exists == 0:
            return jsonify({'error': 'Nota não encontrada'}), 404
        
        # Deletar nota
        sql = "DELETE FROM AVALIACAO_ALUNO WHERE ID_AVALIACAO = " + str(evaluation_id) + " AND ID_ALUNO = " + str(student_id)
        cur.execute(sql)
        conn.commit()
        return jsonify({'message': 'Nota deletada com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar nota: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/students/<int:student_id>/evaluations', methods=['GET'])
def get_student_evaluations_by_student(student_id):
    """Buscar todas as notas de um aluno"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT aa.ID_AVALIACAO, aa.ID_ALUNO, aa.NOTA, a.TIPO as AVALIACAO_TIPO, a.PESO as AVALIACAO_PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD') as AVALIACAO_DATA, al.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE FROM AVALIACAO_ALUNO aa JOIN AVALIACAO a ON aa.ID_AVALIACAO = a.ID JOIN ALUNO al ON aa.ID_ALUNO = al.MATRICULA JOIN OFERTA o ON a.ID_OFERTA = o.ID JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO JOIN CURSO c ON o.ID_CURSO = c.ID JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR WHERE aa.ID_ALUNO = " + str(student_id) + " ORDER BY o.ANO DESC, o.SEMESTRE DESC, m.NOME, a.DATA"
        cur.execute(sql)
        rows = cur.fetchall()
        student_evaluations = []
        for row in rows:
            student_evaluations.append({
                'id_avaliacao': row[0],
                'id_aluno': row[1],
                'nota': row[2],
                'avaliacao_tipo': row[3],
                'avaliacao_peso': row[4],
                'avaliacao_data': row[5],
                'aluno_nome': row[6],
                'materia_nome': row[7],
                'curso_nome': row[8],
                'professor_nome': row[9],
                'ano': row[10],
                'semestre': row[11]
            })
        return jsonify(student_evaluations), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar notas do aluno: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/evaluations/<int:evaluation_id>/students', methods=['GET'])
def get_evaluation_students(evaluation_id):
    """Buscar todas as notas de uma avaliação"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT aa.ID_AVALIACAO, aa.ID_ALUNO, aa.NOTA, a.TIPO as AVALIACAO_TIPO, a.PESO as AVALIACAO_PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD') as AVALIACAO_DATA, al.NOME as ALUNO_NOME, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME, o.ANO, o.SEMESTRE FROM AVALIACAO_ALUNO aa JOIN AVALIACAO a ON aa.ID_AVALIACAO = a.ID JOIN ALUNO al ON aa.ID_ALUNO = al.MATRICULA JOIN OFERTA o ON a.ID_OFERTA = o.ID JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO JOIN CURSO c ON o.ID_CURSO = c.ID JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR WHERE aa.ID_AVALIACAO = " + str(evaluation_id) + " ORDER BY al.NOME"
        cur.execute(sql)
        rows = cur.fetchall()
        student_evaluations = []
        for row in rows:
            student_evaluations.append({
                'id_avaliacao': row[0],
                'id_aluno': row[1],
                'nota': row[2],
                'avaliacao_tipo': row[3],
                'avaliacao_peso': row[4],
                'avaliacao_data': row[5],
                'aluno_nome': row[6],
                'materia_nome': row[7],
                'curso_nome': row[8],
                'professor_nome': row[9],
                'ano': row[10],
                'semestre': row[11]
            })
        return jsonify(student_evaluations), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar notas da avaliação: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
