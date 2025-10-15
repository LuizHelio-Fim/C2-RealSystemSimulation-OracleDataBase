from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection

bp = Blueprint('subject', __name__)

@bp.route('/subjects', methods=['POST'])
def create_subject():
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON são obrigatórios'
            }), 400
        
        id_curso = data.get('id_curso')
        periodo = data.get('periodo')
        nome = data.get('nome')
        carga_horaria = data.get('carga_horaria')
        
        missing_fields = []
        if not id_curso or id_curso == '':
            missing_fields.append('id_curso')
        if periodo is None or periodo == '':
            missing_fields.append('periodo')
        if not nome or nome.strip() == '':
            missing_fields.append('nome')
        if carga_horaria is None or carga_horaria == '':
            missing_fields.append('carga_horaria')
            
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Campos obrigatórios ausentes: {", ".join(missing_fields)}'
            }), 400

        id_materia = data.get('id_materia')
        
        conn = get_connection()
        
        cur = conn.cursor()
        
        if not id_materia:
            cur.execute("SELECT NVL(MAX(ID_MATERIA), 0) + 1 FROM MATERIAS WHERE ID_CURSO = " + str(id_curso))
            id_materia = cur.fetchone()[0]

        try:
            sql_check = "SELECT COUNT(1) FROM CURSO WHERE ID = " + str(id_curso)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Curso não encontrado'
                }), 404

            sql = "INSERT INTO MATERIAS (ID_MATERIA, ID_CURSO, PERIODO, NOME, CARGA_HORARIA) VALUES (" + str(id_materia) + ", " + str(id_curso) + ", " + str(periodo) + ", '" + str(nome) + "', " + str(carga_horaria) + ")"
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Matéria criada com sucesso',
                'data': {'id_materia': id_materia, 'id_curso': id_curso}
            }), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar matéria: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

@bp.route('/subjects', methods=['GET'])
def list_subjects():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT m.ID_MATERIA, m.ID_CURSO, m.PERIODO, m.NOME, m.CARGA_HORARIA, c.NOME as CURSO_NOME FROM MATERIAS m JOIN CURSOS c ON m.ID_CURSO = c.ID ORDER BY c.NOME, m.PERIODO, m.NOME"
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
                'curso_nome': row[5]
            })
        return jsonify({
            'success': True,
            'data': subjects,
            'count': len(subjects)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar matérias: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/subjects/<int:subject_id>/<int:course_id>', methods=['GET'])
def get_subject_by_id(subject_id, course_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT m.ID_MATERIA, m.ID_CURSO, m.PERIODO, m.NOME, m.CARGA_HORARIA, c.NOME as CURSO_NOME
        FROM MATERIAS m
        JOIN CURSOS c ON m.ID_CURSO = c.ID
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
                'curso_nome': row[5]
            }
            return jsonify({
                'success': True,
                'data': subject
            }), 200
        return jsonify({
            'success': False,
            'message': 'Matéria não encontrada'
        }), 404
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
            cur.execute("SELECT COUNT(1) FROM MATERIAS WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                        {'id_materia': subject_id, 'id_curso': course_id})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Matéria não encontrada'}), 404

            update_fields = []
            params = {'id_materia': subject_id, 'id_curso': course_id}
            
            print(f"DEBUG - Dados recebidos: {data}")  # Log para debug
            
            if 'periodo' in data:
                try:
                    periodo_value = int(data['periodo']) if data['periodo'] else None
                    update_fields.append("PERIODO = :periodo")
                    params['periodo'] = periodo_value
                    print(f"DEBUG - Periodo convertido: {periodo_value}")
                except (ValueError, TypeError) as e:
                    return jsonify({'error': f'Período deve ser um número válido: {data["periodo"]}'}), 400
            
            if 'nome' in data:
                update_fields.append("NOME = :nome")
                params['nome'] = data['nome']
                print(f"DEBUG - Nome: {data['nome']}")
                
            if 'carga_horaria' in data:
                try:
                    carga_value = int(data['carga_horaria']) if data['carga_horaria'] else None
                    update_fields.append("CARGA_HORARIA = :carga_horaria")
                    params['carga_horaria'] = carga_value
                    print(f"DEBUG - Carga horária convertida: {carga_value}")
                except (ValueError, TypeError) as e:
                    return jsonify({'error': f'Carga horária deve ser um número válido: {data["carga_horaria"]}'}), 400
            
            if 'id_curso' in data:
                try:
                    id_curso_value = int(data['id_curso']) if data['id_curso'] else None
                    update_fields.append("ID_CURSO = :new_id_curso")
                    params['new_id_curso'] = id_curso_value
                    print(f"DEBUG - ID Curso convertido: {id_curso_value}")
                except (ValueError, TypeError) as e:
                    return jsonify({'error': f'ID do curso deve ser um número válido: {data["id_curso"]}'}), 400

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = f"UPDATE MATERIAS SET {', '.join(update_fields)} WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso"
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
        cur.execute("SELECT COUNT(1) FROM OFERTA WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                   {'id_materia': subject_id, 'id_curso': course_id})
        offer_count = cur.fetchone()[0]
        if offer_count > 0:
            return jsonify({'error': 'Não é possível excluir matéria com ofertas cadastradas'}), 400
        
        cur.execute("SELECT COUNT(1) FROM MATERIA WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                   {'id_materia': subject_id, 'id_curso': course_id})
        subject_exists = cur.fetchone()[0]
        if subject_exists == 0:
            return jsonify({'error': 'Matéria não encontrada'}), 404
        
        sql = "DELETE FROM MATERIAS WHERE ID_MATERIA = " + str(subject_id) + " AND ID_CURSO = " + str(course_id)
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
        SELECT m.ID_MATERIA, m.ID_CURSO, m.PERIODO, m.NOME, m.CARGA_HORARIA, c.NOME as CURSO_NOME
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
                'curso_nome': row[5]
            })
        return jsonify(subjects), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar matérias do curso: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
