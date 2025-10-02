from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val

bp = Blueprint('offer', __name__)

@bp.route('/offers', methods=['POST'])
def create_offer():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['ano', 'semestre', 'id_materia', 'id_curso', 'id_professor']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        ano = data.get("ano")
        semestre = data.get("semestre")
        id_materia = data.get("id_materia")
        id_curso = data.get("id_curso")
        id_professor = data.get("id_professor")

        try:
            # Verificar se a matéria existe
            cur.execute("SELECT COUNT(1) FROM MATERIA WHERE ID_MATERIA = :id_materia AND ID_CURSO = :id_curso", 
                       {'id_materia': id_materia, 'id_curso': id_curso})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Matéria não encontrada'}), 404

            # Verificar se o professor existe
            cur.execute("SELECT COUNT(1) FROM PROFESSOR WHERE ID_PROFESSOR = :id_professor", 
                       {'id_professor': id_professor})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Professor não encontrado'}), 404

            new_id = next_seq_val("OFERTA_SEQ", conn)
            sql = """
            INSERT INTO OFERTA (ID, ANO, SEMESTRE, ID_MATERIA, ID_CURSO, ID_PROFESSOR)
            VALUES (:id, :ano, :semestre, :id_materia, :id_curso, :id_professor)
            """
            cur.execute(sql, {
                'id': new_id,
                'ano': ano,
                'semestre': semestre,
                'id_materia': id_materia,
                'id_curso': id_curso,
                'id_professor': id_professor
            })
            conn.commit()
            return jsonify({'id': new_id, 'message': 'Oferta criada com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao criar oferta: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/offers', methods=['GET'])
def list_offers():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT o.ID, o.ANO, o.SEMESTRE, o.ID_MATERIA, o.ID_CURSO, o.ID_PROFESSOR,
               m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME
        FROM OFERTA o
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        ORDER BY o.ANO DESC, o.SEMESTRE DESC, c.NOME, m.NOME
        """
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
        return jsonify(offers), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar ofertas: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer_by_id(offer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT o.ID, o.ANO, o.SEMESTRE, o.ID_MATERIA, o.ID_CURSO, o.ID_PROFESSOR,
               m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME
        FROM OFERTA o
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE o.ID = """ + str(offer_id) + """
        """
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
            return jsonify(offer), 200
        return jsonify({'error': 'Oferta não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar oferta: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # Verificar se a oferta existe
            # VULNERÁVEL: Verificar se a oferta existe
            sql_check = "SELECT COUNT(1) FROM OFERTA WHERE ID = " + str(offer_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Oferta não encontrada'}), 404

            # Construir query de atualização dinamicamente
            update_fields = []
            params = {'id': offer_id}
            
            if 'ano' in data:
                update_fields.append("ANO = :ano")
                params['ano'] = data['ano']
            
            if 'semestre' in data:
                update_fields.append("SEMESTRE = :semestre")
                params['semestre'] = data['semestre']
                
            if 'id_professor' in data:
                # Verificar se o professor existe
                cur.execute("SELECT COUNT(1) FROM PROFESSOR WHERE ID_PROFESSOR = :id_professor", 
                           {'id_professor': data['id_professor']})
                if cur.fetchone()[0] == 0:
                    return jsonify({'error': 'Professor não encontrado'}), 404
                update_fields.append("ID_PROFESSOR = :id_professor")
                params['id_professor'] = data['id_professor']

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = f"UPDATE OFERTA SET {', '.join(update_fields)} WHERE ID = :id"
            cur.execute(sql, params)
            conn.commit()
            
            return jsonify({'message': 'Oferta atualizada com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar oferta: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/offers/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se a oferta tem avaliações
        # VULNERÁVEL: Verificar se existem avaliações
        sql_check_eval = "SELECT COUNT(1) FROM AVALIACAO WHERE ID_OFERTA = " + str(offer_id)
        cur.execute(sql_check_eval)
        evaluation_count = cur.fetchone()[0]
        if evaluation_count > 0:
            return jsonify({'error': 'Não é possível excluir oferta com avaliações cadastradas'}), 400
        
        # Verificar se a oferta tem matrículas de alunos
        # VULNERÁVEL: Verificar se existem matrículas
        sql_check_grades = "SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_OFERTA = " + str(offer_id)
        cur.execute(sql_check_grades)
        enrollment_count = cur.fetchone()[0]
        if enrollment_count > 0:
            return jsonify({'error': 'Não é possível excluir oferta com alunos matriculados'}), 400
        
        # Verificar se a oferta existe
        # VULNERÁVEL: Verificar se a oferta existe antes de deletar
        sql_check_exists = "SELECT COUNT(1) FROM OFERTA WHERE ID = " + str(offer_id)
        cur.execute(sql_check_exists)
        offer_exists = cur.fetchone()[0]
        if offer_exists == 0:
            return jsonify({'error': 'Oferta não encontrada'}), 404
        
        # VULNERÁVEL: Deletar oferta
        sql = "DELETE FROM OFERTA WHERE ID = " + str(offer_id)
        cur.execute(sql)
        conn.commit()
        return jsonify({'message': 'Oferta deletada com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar oferta: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/semester/<int:year>/<int:semester>', methods=['GET'])
def get_offers_by_semester(year, semester):
    """Buscar todas as ofertas de um semestre específico"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT o.ID, o.ANO, o.SEMESTRE, o.ID_MATERIA, o.ID_CURSO, o.ID_PROFESSOR,
               m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME
        FROM OFERTA o
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE o.ANO = """ + str(year) + """ AND o.SEMESTRE = """ + str(semester) + """
        ORDER BY c.NOME, m.NOME
        """
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
        return jsonify(offers), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar ofertas do semestre: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
