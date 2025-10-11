from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val

bp = Blueprint('course', __name__)

@bp.route('/courses', methods=['POST'])
def create_course():
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON são obrigatórios'
            }), 400
        
        # Validar campos obrigatórios conforme schema do banco (todos são NOT NULL)
        nome = data.get('nome')
        carga_horaria_total = data.get('carga_horaria_total')
        
        # Todos estes campos são NOT NULL no banco CURSO
        if not all([nome, carga_horaria_total]):
            return jsonify({
                'success': False,
                'message': 'Campos obrigatórios: nome, carga_horaria_total'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            new_id = next_seq_val("CURSO_ID_SEQ", conn)
            # VULNERÁVEL: Usando concatenação de strings
            sql = "INSERT INTO CURSO (ID, NOME, CARGA_HORARIA_TOTAL) VALUES (" + str(new_id) + ", '" + str(nome) + "', " + str(carga_horaria_total) + ")"
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Curso criado com sucesso',
                'data': {'id': new_id}
            }), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar curso: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

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
        return jsonify({
            'success': True,
            'data': courses,
            'count': len(courses)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar cursos: {str(e)}'
        }), 500
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
            return jsonify({
                'success': True,
                'data': course
            }), 200
        
        return jsonify({
            'success': False,
            'message': 'Curso não encontrado'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar curso: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON são obrigatórios'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # VULNERÁVEL: Verificar se o curso existe
            sql_check = "SELECT COUNT(1) FROM CURSO WHERE ID = " + str(course_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Curso não encontrado'
                }), 404

            # VULNERÁVEL: Construir query de atualização dinamicamente
            update_parts = []
            
            if 'nome' in data and data['nome'] is not None and str(data['nome']).strip() != '':
                # Escape aspas simples para evitar SQL injection
                nome_escaped = str(data['nome']).replace("'", "''")
                update_parts.append("NOME = '" + nome_escaped + "'")
            
            if 'carga_horaria_total' in data:
                carga_value = data['carga_horaria_total']
                
                # Se o valor for None ou string vazia, pular este campo
                if carga_value is None or (isinstance(carga_value, str) and carga_value.strip() == ''):
                    pass  # Não incluir este campo na atualização
                else:
                    # Validar se é um número
                    try:
                        carga_horaria = float(carga_value)
                        if carga_horaria < 0:
                            return jsonify({
                                'success': False,
                                'message': 'Carga horária deve ser um número positivo'
                            }), 400
                        update_parts.append("CARGA_HORARIA_TOTAL = " + str(carga_horaria))
                    except (ValueError, TypeError):
                        return jsonify({
                            'success': False,
                            'message': f'Carga horária deve ser um número válido. Valor fornecido: {carga_value}'
                        }), 400

            if not update_parts:
                return jsonify({
                    'success': False,
                    'message': 'Nenhum campo válido para atualizar foi fornecido'
                }), 400

            sql = "UPDATE CURSO SET " + ", ".join(update_parts) + " WHERE ID = " + str(course_id)
            print(f"SQL gerado: {sql}")  # Debug
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Curso atualizado com sucesso'
            }), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar curso: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

@bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se existem alunos matriculados no curso
        sql_check_students = "SELECT COUNT(1) FROM ALUNO WHERE ID_CURSO = " + str(course_id)
        cur.execute(sql_check_students)
        student_count = cur.fetchone()[0]
        if student_count > 0:
            return jsonify({
                'success': False,
                'message': 'Curso possui alunos matriculados e não pode ser excluído. Remova-os antes.'
            }), 400
        
        # Verificar se existem matérias no curso
        sql_check_subjects = "SELECT COUNT(1) FROM MATERIA WHERE ID_CURSO = " + str(course_id)
        cur.execute(sql_check_subjects)
        subject_count = cur.fetchone()[0]
        if subject_count > 0:
            return jsonify({
                'success': False,
                'message': 'Curso possui matérias cadastradas e não pode ser excluído. Remova-as antes.'
            }), 400
        
        # Verificar se o curso existe
        sql_check_exists = "SELECT COUNT(1) FROM CURSO WHERE ID = " + str(course_id)
        cur.execute(sql_check_exists)
        course_exists = cur.fetchone()[0]
        if course_exists == 0:
            return jsonify({
                'success': False,
                'message': 'Curso não encontrado'
            }), 404
        
        # Deletar curso
        sql = "DELETE FROM CURSO WHERE ID = " + str(course_id)
        cur.execute(sql)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Curso deletado com sucesso'
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar curso: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)