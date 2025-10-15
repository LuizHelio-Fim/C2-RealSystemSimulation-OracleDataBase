from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val

bp = Blueprint('offer', __name__)

@bp.route('/offers', methods=['POST'])
def create_offer():
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON são obrigatórios'
            }), 400
        
        ano = data.get('ano')
        semestre = data.get('semestre')
        id_materia = data.get('id_materia')
        id_curso = data.get('id_curso')
        id_professor = data.get('id_professor')
        
        if not all([ano, semestre, id_materia, id_curso, id_professor]):
            return jsonify({
                'success': False,
                'message': 'Campos obrigatórios: ano, semestre, id_materia, id_curso, id_professor'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            sql_check_materia = "SELECT COUNT(1) FROM MATERIAS WHERE ID_MATERIA = " + str(id_materia) + " AND ID_CURSO = " + str(id_curso)
            cur.execute(sql_check_materia)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Matéria não encontrada'
                }), 404

            sql_check_professor = "SELECT COUNT(1) FROM PROFESSORES WHERE ID_PROFESSOR = " + str(id_professor)
            cur.execute(sql_check_professor)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Professor não encontrado'
                }), 404

            new_id = next_seq_val("OFERTA_ID_SEQ", conn)
            sql = "INSERT INTO OFERTAS (ID, ANO, SEMESTRE, ID_MATERIA, ID_CURSO, ID_PROFESSOR) VALUES (" + str(new_id) + ", " + str(ano) + ", " + str(semestre) + ", " + str(id_materia) + ", " + str(id_curso) + ", " + str(id_professor) + ")"
            
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Oferta criada com sucesso',
                'data': {'id': new_id}
            }), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar oferta: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

@bp.route('/offers', methods=['GET'])
def list_offers():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT o.ID, o.ANO, o.SEMESTRE, o.ID_MATERIA, o.ID_CURSO, o.ID_PROFESSOR, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME FROM OFERTAS o JOIN MATERIAS m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO JOIN CURSOS c ON o.ID_CURSO = c.ID JOIN PROFESSORES p ON o.ID_PROFESSOR = p.ID_PROFESSOR ORDER BY o.ANO DESC, o.SEMESTRE DESC, c.NOME, m.NOME"
        cur.execute(sql)
        rows = cur.fetchall()
        offers = []
        for row in rows:
            offers.append({
                'id': row[0],
                'ano': row[1],
                'semestre': row[2],
                'id_materia': row[3],
                'id_curso': row[4],
                'id_professor': row[5],
                'materia_nome': row[6],
                'curso_nome': row[7],
                'professor_nome': row[8]
            })
        return jsonify({
            'success': True,
            'data': offers,
            'count': len(offers)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar ofertas: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer_by_id(offer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT o.ID, o.ANO, o.SEMESTRE, o.ID_MATERIA, o.ID_CURSO, o.ID_PROFESSOR, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME FROM OFERTAS o JOIN MATERIAS m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO JOIN CURSOS c ON o.ID_CURSO = c.ID JOIN PROFESSORES p ON o.ID_PROFESSOR = p.ID_PROFESSOR WHERE o.ID = :offer_id"
        cur.execute(sql)
        row = cur.fetchone()
        
        if row:
            offer = {
                'id': row[0],
                'ano': row[1],
                'semestre': row[2],
                'id_materia': row[3],
                'id_curso': row[4],
                'id_professor': row[5],
                'materia_nome': row[6],
                'curso_nome': row[7],
                'professor_nome': row[8]
            }
            return jsonify({
                'success': True,
                'data': offer
            }), 200
        
        return jsonify({
            'success': False,
            'message': 'Oferta não encontrada'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar oferta: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
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
            sql_check = "SELECT COUNT(1) FROM OFERTA WHERE ID = " + str(offer_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Oferta não encontrada'
                }), 404

            update_parts = []
            
            if 'ano' in data:
                update_parts.append("ANO = " + str(data['ano']))
            
            if 'semestre' in data:
                update_parts.append("SEMESTRE = " + str(data['semestre']))
                
            if 'id_professor' in data:
                sql_check_professor = "SELECT COUNT(1) FROM PROFESSOR WHERE ID_PROFESSOR = " + str(data['id_professor'])
                cur.execute(sql_check_professor)
                if cur.fetchone()[0] == 0:
                    return jsonify({
                        'success': False,
                        'message': 'Professor não encontrado'
                    }), 404
                update_parts.append("ID_PROFESSOR = " + str(data['id_professor']))

            if 'id_materia' in data and 'id_curso' in data:
                sql_check_materia = "SELECT COUNT(1) FROM MATERIA WHERE ID_MATERIA = " + str(data['id_materia']) + " AND ID_CURSO = " + str(data['id_curso'])
                cur.execute(sql_check_materia)
                if cur.fetchone()[0] == 0:
                    return jsonify({
                        'success': False,
                        'message': 'Matéria não encontrada'
                    }), 404
                update_parts.append("ID_MATERIA = " + str(data['id_materia']))
                update_parts.append("ID_CURSO = " + str(data['id_curso']))

            if not update_parts:
                return jsonify({
                    'success': False,
                    'message': 'Nenhum campo para atualizar foi fornecido'
                }), 400

            sql = "UPDATE OFERTAS SET " + ", ".join(update_parts) + " WHERE ID = " + str(offer_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Oferta atualizada com sucesso'
            }), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar oferta: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

@bp.route('/offers/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_check_grades = "SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_OFERTA = " + str(offer_id)
        cur.execute(sql_check_grades)
        enrollment_count = cur.fetchone()[0]
        if enrollment_count > 0:
            return jsonify({
                'success': False,
                'message': 'Oferta possui alunos matriculados e não pode ser excluída. Remova-os antes.'
            }), 400
        
        sql_check_exists = "SELECT COUNT(1) FROM OFERTA WHERE ID = " + str(offer_id)
        cur.execute(sql_check_exists)
        offer_exists = cur.fetchone()[0]
        if offer_exists == 0:
            return jsonify({
                'success': False,
                'message': 'Oferta não encontrada'
            }), 404
        
        sql = "DELETE FROM OFERTAS WHERE ID = " + str(offer_id)
        cur.execute(sql)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Oferta deletada com sucesso'
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar oferta: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/semester/<int:year>/<int:semester>', methods=['GET'])
def get_offers_by_semester(year, semester):
    """Buscar todas as ofertas de um semestre específico"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT o.ID, o.ANO, o.SEMESTRE, o.ID_MATERIA, o.ID_CURSO, o.ID_PROFESSOR, m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME FROM OFERTA o JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO JOIN CURSO c ON o.ID_CURSO = c.ID JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR WHERE o.ANO = " + str(year) + " AND o.SEMESTRE = " + str(semester) + " ORDER BY c.NOME, m.NOME"
        cur.execute(sql)
        rows = cur.fetchall()
        offers = []
        for row in rows:
            offers.append({
                'id': row[0],
                'ano': row[1],
                'semestre': row[2],
                'id_materia': row[3],
                'id_curso': row[4],
                'id_professor': row[5],
                'materia_nome': row[6],
                'curso_nome': row[7],
                'professor_nome': row[8]
            })
        return jsonify({
            'success': True,
            'data': offers,
            'count': len(offers)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar ofertas do semestre: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)
