from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val
from datetime import datetime

bp = Blueprint('evaluation', __name__)

def format_date_for_oracle(dt_str):
    """Convert date from various formats to 'YYYY-MM-DD' or return None for NULL."""
    if not dt_str or dt_str.strip() == '':
        return None
    try:
        # Try YYYY-MM-DD format first
        datetime.strptime(dt_str, '%Y-%m-%d')
        return dt_str
    except ValueError:
        try:
            # Try DD/MM/YYYY format
            dt = datetime.strptime(dt_str, '%d/%m/%Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            raise ValueError("A data deve estar no formato 'YYYY-MM-DD' ou 'DD/MM/YYYY'.")

@bp.route('/evaluations', methods=['POST'])
def create_evaluation():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['tipo', 'peso', 'data', 'id_oferta']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        tipo = data.get("tipo")
        peso = data.get("peso")
        data_avaliacao = data.get("data")
        id_oferta = data.get("id_oferta")

        try:
            # Verificar se a oferta existe
            # VULNERÁVEL: Verificar se a oferta existe
            sql_check_oferta = "SELECT COUNT(1) FROM OFERTA WHERE ID = " + str(id_oferta)
            cur.execute(sql_check_oferta)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Oferta não encontrada'}), 404

            # Formatar data
            formatted_date = format_date_for_oracle(data_avaliacao)
            
            new_id = next_seq_val("AVALIACAO_SEQ", conn)
            sql = """
            INSERT INTO AVALIACAO (ID, TIPO, PESO, DATA, ID_OFERTA)
            VALUES (:id, :tipo, :peso, TO_DATE(:data,'YYYY-MM-DD'), :id_oferta)
            """
            cur.execute(sql, {
                'id': new_id,
                'tipo': tipo,
                'peso': peso,
                'data': formatted_date,
                'id_oferta': id_oferta
            })
            conn.commit()
            return jsonify({'id': new_id, 'message': 'Avaliação criada com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao criar avaliação: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/evaluations', methods=['GET'])
def list_evaluations():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT a.ID, a.TIPO, a.PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD'), a.ID_OFERTA,
               m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME,
               o.ANO, o.SEMESTRE
        FROM AVALIACAO a
        JOIN OFERTA o ON a.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        ORDER BY a.DATA DESC, c.NOME, m.NOME
        """
        cur.execute(sql)
        rows = cur.fetchall()
        evaluations = []
        for row in rows:
            evaluations.append({
                'id': row[0],
                'tipo': row[1],
                'peso': row[2],
                'data': row[3],
                'id_oferta': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
            })
        return jsonify(evaluations), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar avaliações: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/evaluations/<int:evaluation_id>', methods=['GET'])
def get_evaluation_by_id(evaluation_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT a.ID, a.TIPO, a.PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD'), a.ID_OFERTA,
               m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME,
               o.ANO, o.SEMESTRE
        FROM AVALIACAO a
        JOIN OFERTA o ON a.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE a.ID = """ + str(evaluation_id) + """
        """
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            evaluation = {
                'id': row[0],
                'tipo': row[1],
                'peso': row[2],
                'data': row[3],
                'id_oferta': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
            }
            return jsonify(evaluation), 200
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar avaliação: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/evaluations/<int:evaluation_id>', methods=['PUT'])
def update_evaluation(evaluation_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # Verificar se a avaliação existe
            cur.execute("SELECT COUNT(1) FROM AVALIACAO WHERE ID = :id", {'id': evaluation_id})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Avaliação não encontrada'}), 404

            # Construir query de atualização dinamicamente
            update_fields = []
            params = {'id': evaluation_id}
            
            if 'tipo' in data:
                update_fields.append("TIPO = :tipo")
                params['tipo'] = data['tipo']
            
            if 'peso' in data:
                update_fields.append("PESO = :peso")
                params['peso'] = data['peso']
                
            if 'data' in data:
                formatted_date = format_date_for_oracle(data['data']) if data['data'] else None
                if formatted_date:
                    update_fields.append("DATA = TO_DATE(:data,'YYYY-MM-DD')")
                    params['data'] = formatted_date
                else:
                    update_fields.append("DATA = NULL")

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = f"UPDATE AVALIACAO SET {', '.join(update_fields)} WHERE ID = :id"
            cur.execute(sql, params)
            conn.commit()
            
            return jsonify({'message': 'Avaliação atualizada com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar avaliação: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/evaluations/<int:evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se a avaliação tem notas de alunos
        cur.execute("SELECT COUNT(1) FROM AVALIACAO_ALUNO WHERE ID_AVALIACAO = :id", {'id': evaluation_id})
        student_evaluation_count = cur.fetchone()[0]
        if student_evaluation_count > 0:
            return jsonify({'error': 'Não é possível excluir avaliação com notas de alunos cadastradas'}), 400
        
        # Verificar se a avaliação existe
        cur.execute("SELECT COUNT(1) FROM AVALIACAO WHERE ID = :id", {'id': evaluation_id})
        evaluation_exists = cur.fetchone()[0]
        if evaluation_exists == 0:
            return jsonify({'error': 'Avaliação não encontrada'}), 404
        
        # Deletar avaliação
        sql = "DELETE FROM AVALIACAO WHERE ID = :id"
        cur.execute(sql, {'id': evaluation_id})
        conn.commit()
        return jsonify({'message': 'Avaliação deletada com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar avaliação: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/offers/<int:offer_id>/evaluations', methods=['GET'])
def get_evaluations_by_offer(offer_id):
    """Buscar todas as avaliações de uma oferta específica"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = """
        SELECT a.ID, a.TIPO, a.PESO, TO_CHAR(a.DATA, 'YYYY-MM-DD'), a.ID_OFERTA,
               m.NOME as MATERIA_NOME, c.NOME as CURSO_NOME, p.NOME as PROFESSOR_NOME,
               o.ANO, o.SEMESTRE
        FROM AVALIACAO a
        JOIN OFERTA o ON a.ID_OFERTA = o.ID
        JOIN MATERIA m ON o.ID_MATERIA = m.ID_MATERIA AND o.ID_CURSO = m.ID_CURSO
        JOIN CURSO c ON o.ID_CURSO = c.ID
        JOIN PROFESSOR p ON o.ID_PROFESSOR = p.ID_PROFESSOR
        WHERE a.ID_OFERTA = :id_oferta
        ORDER BY a.DATA
        """
        cur.execute(sql, {'id_oferta': offer_id})
        rows = cur.fetchall()
        evaluations = []
        for row in rows:
            evaluations.append({
                'id': row[0],
                'tipo': row[1],
                'peso': row[2],
                'data': row[3],
                'id_oferta': row[4],
                'materia_nome': row[5],
                'curso_nome': row[6],
                'professor_nome': row[7],
                'ano': row[8],
                'semestre': row[9]
            })
        return jsonify(evaluations), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar avaliações da oferta: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
