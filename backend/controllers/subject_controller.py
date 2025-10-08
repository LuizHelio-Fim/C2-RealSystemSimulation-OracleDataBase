from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('subject', __name__)

@bp.route('/subjects', methods=['POST'])
def create_subject():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['id_materia', 'id_curso', 'periodo', 'nome', 'carga_horaria', 'media_aprovacao']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        id_materia = data.get("id_materia")
        id_curso = data.get("id_curso")
        periodo = data.get("periodo")
        nome = data.get("nome")
        carga_horaria = data.get("carga_horaria")
        media_aprovacao = data.get("media_aprovacao")

        try:
            # VULNERÁVEL: Verificar se o curso existe
            sql_check = "SELECT COUNT(1) FROM CURSO WHERE ID = " + str(id_curso)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Curso não encontrado'}), 404

            # VULNERÁVEL: Usando concatenação de strings
            sql = "INSERT INTO MATERIA (ID_MATERIA, ID_CURSO, PERIODO, NOME, CARGA_HORARIA, MEDIA_APROVACAO) VALUES (" + str(id_materia) + ", " + str(id_curso) + ", " + str(periodo) + ", '" + str(nome) + "', " + str(carga_horaria) + ", " + str(media_aprovacao) + ")"
            cur.execute(sql)
            conn.commit()
            return jsonify({'message': 'Matéria criada com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao criar matéria: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/subjects', methods=['GET'])
def list_subjects():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT m.ID_MATERIA, m.ID_CURSO, m.PERIODO, m.NOME, m.CARGA_HORARIA, m.MEDIA_APROVACAO, c.NOME as CURSO_NOME
        FROM MATERIA m
        JOIN CURSO c ON m.ID_CURSO = c.ID
        ORDER BY c.NOME, m.PERIODO, m.NOME
        """
        cur.execute(sql)
        rows = cur.fetchall()
        subjects = []
        for row in rows:
            subjects.append({
                'id_materia': row[0],
                'id_curso': row[1],
                'periodo': row[2],
                'nome': row[3],
                'carga_horaria': row[4],
                'media_aprovacao': row[5],
                'curso_nome': row[6]
            })
        return jsonify(subjects), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matérias: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/subjects/<int:subject_id>/<int:course_id>', methods=['GET'])
def get_subject_by_id(subject_id, course_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT m.ID_MATERIA, m.ID_CURSO, m.PERIODO, m.NOME, m.CARGA_HORARIA, m.MEDIA_APROVACAO, c.NOME as CURSO_NOME
        FROM MATERIA m
        JOIN CURSO c ON m.ID_CURSO = c.ID
        WHERE m.ID_MATERIA = """ + str(subject_id) + """ AND m.ID_CURSO = """ + str(course_id) + """
        """
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            subject = {
                'id_materia': row[0],
                'id_curso': row[1],
                'periodo': row[2],
                'nome': row[3],
                'carga_horaria': row[4],
                'media_aprovacao': row[5],
                'curso_nome': row[6]
            }
            return jsonify(subject), 200
        return jsonify({'error': 'Matéria não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar matéria: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/subjects/<int:subject_id>/<int:course_id>', methods=['PUT'])
def update_subject(subject_id, course_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # Verificar se a matéria existe
            cur.execute("SELECT COUNT(1) FROM MATERIA WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                       {'id_materia': subject_id, 'id_curso': course_id})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Matéria não encontrada'}), 404

            # Construir query de atualização dinamicamente
            update_fields = []
            params = {'id_materia': subject_id, 'id_curso': course_id}
            
            if 'periodo' in data:
                update_fields.append("PERIODO = :periodo")
                params['periodo'] = data['periodo']
            
            if 'nome' in data:
                update_fields.append("NOME = :nome")
                params['nome'] = data['nome']
                
            if 'carga_horaria' in data:
                update_fields.append("CARGA_HORARIA = :carga_horaria")
                params['carga_horaria'] = data['carga_horaria']
                
            if 'media_aprovacao' in data:
                update_fields.append("MEDIA_APROVACAO = :media_aprovacao")
                params['media_aprovacao'] = data['media_aprovacao']

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = f"UPDATE MATERIA SET {', '.join(update_fields)} WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso"
            cur.execute(sql, params)
            conn.commit()
            
            return jsonify({'message': 'Matéria atualizada com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar matéria: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/subjects/<int:subject_id>/<int:course_id>', methods=['DELETE'])
def delete_subject(subject_id, course_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se a matéria tem ofertas
        cur.execute("SELECT COUNT(1) FROM OFERTA WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                   {'id_materia': subject_id, 'id_curso': course_id})
        offer_count = cur.fetchone()[0]
        if offer_count > 0:
            return jsonify({'error': 'Não é possível excluir matéria com ofertas cadastradas'}), 400
        
        # Verificar se a matéria existe
        cur.execute("SELECT COUNT(1) FROM MATERIA WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                   {'id_materia': subject_id, 'id_curso': course_id})
        subject_exists = cur.fetchone()[0]
        if subject_exists == 0:
            return jsonify({'error': 'Matéria não encontrada'}), 404
        
        # VULNERÁVEL: Deletar matéria
        sql = "DELETE FROM MATERIA WHERE ID_MATERIA = " + str(subject_id) + " AND ID_CURSO = " + str(course_id)
        cur.execute(sql)
        conn.commit()
        return jsonify({'message': 'Matéria deletada com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar matéria: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/courses/<int:course_id>/subjects', methods=['GET'])
def get_subjects_by_course(course_id):
    """Buscar todas as matérias de um curso específico"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT m.ID_MATERIA, m.ID_CURSO, m.PERIODO, m.NOME, m.CARGA_HORARIA, m.MEDIA_APROVACAO, c.NOME as CURSO_NOME
        FROM MATERIA m
        JOIN CURSO c ON m.ID_CURSO = c.ID
        WHERE m.ID_CURSO = """ + str(course_id) + """
        ORDER BY m.PERIODO, m.NOME
        """
        cur.execute(sql)
        rows = cur.fetchall()
        subjects = []
        for row in rows:
            subjects.append({
                'id_materia': row[0],
                'id_curso': row[1],
                'periodo': row[2],
                'nome': row[3],
                'carga_horaria': row[4],
                'media_aprovacao': row[5],
                'curso_nome': row[6]
            })
        return jsonify(subjects), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matérias do curso: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
