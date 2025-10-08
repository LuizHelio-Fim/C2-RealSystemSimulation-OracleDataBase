from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val

bp = Blueprint('course', __name__)

@bp.route('/courses', methods=['POST'])
def create_course():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['nome', 'carga_horaria_total']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        nome = data.get("nome")
        carga_horaria_total = data.get("carga_horaria_total")

        try:
            new_id = next_seq_val("CURSO_SEQ", conn)
            # VULNERÁVEL: Usando concatenação de strings
            sql = "INSERT INTO CURSO (ID, NOME, CARGA_HORARIA_TOTAL) VALUES (" + str(new_id) + ", '" + str(nome) + "', " + str(carga_horaria_total) + ")"
            cur.execute(sql)
            conn.commit()
            return jsonify({'id': new_id, 'message': 'Curso criado com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao criar curso: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/courses', methods=['GET'])
def list_courses():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT ID, NOME, CARGA_HORARIA_TOTAL FROM CURSO ORDER BY NOME"
        cur.execute(sql)
        rows = cur.fetchall()
        courses = []
        for row in rows:
            courses.append({
                'id': row[0],
                'nome': row[1],
                'carga_horaria_total': row[2]
            })
        return jsonify(courses), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar cursos: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # VULNERÁVEL: Usando concatenação de strings
        sql = "SELECT ID, NOME, CARGA_HORARIA_TOTAL FROM CURSO WHERE ID = " + str(course_id)
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            course = {
                'id': row[0],
                'nome': row[1],
                'carga_horaria_total': row[2]
            }
            return jsonify(course), 200
        return jsonify({'error': 'Curso não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar curso: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # VULNERÁVEL: Verificar se o curso existe
            sql_check = "SELECT COUNT(1) FROM CURSO WHERE ID = " + str(course_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Curso não encontrado'}), 404

            # VULNERÁVEL: Construir query de atualização dinamicamente
            update_parts = []
            
            if 'nome' in data:
                update_parts.append("NOME = '" + str(data['nome']) + "'")
            
            if 'carga_horaria_total' in data:
                update_parts.append("CARGA_HORARIA_TOTAL = " + str(data['carga_horaria_total']))

            if not update_parts:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = "UPDATE CURSO SET " + ", ".join(update_parts) + " WHERE ID = " + str(course_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({'message': 'Curso atualizado com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar curso: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # VULNERÁVEL: Verificar se existem alunos matriculados no curso
        sql_check_students = "SELECT COUNT(1) FROM ALUNO WHERE ID_CURSO = " + str(course_id)
        cur.execute(sql_check_students)
        student_count = cur.fetchone()[0]
        if student_count > 0:
            return jsonify({'error': 'Não é possível excluir curso com alunos matriculados'}), 400
        
        # VULNERÁVEL: Verificar se existem matérias no curso
        sql_check_subjects = "SELECT COUNT(1) FROM MATERIA WHERE ID_CURSO = " + str(course_id)
        cur.execute(sql_check_subjects)
        subject_count = cur.fetchone()[0]
        if subject_count > 0:
            return jsonify({'error': 'Não é possível excluir curso com matérias cadastradas'}), 400
        
        # VULNERÁVEL: Verificar se o curso existe
        sql_check_exists = "SELECT COUNT(1) FROM CURSO WHERE ID = " + str(course_id)
        cur.execute(sql_check_exists)
        course_exists = cur.fetchone()[0]
        if course_exists == 0:
            return jsonify({'error': 'Curso não encontrado'}), 404
        
        # VULNERÁVEL: Deletar curso
        sql = "DELETE FROM CURSO WHERE ID = " + str(course_id)
        cur.execute(sql)
        conn.commit()
        return jsonify({'message': 'Curso deletado com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar curso: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)