from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val
from datetime import datetime

bp = Blueprint('professor', __name__)

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

@bp.route('/professors', methods=['POST'])
def create_professor():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['cpf', 'nome', 'data_nasc', 'email', 'status']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        cpf = data.get("cpf")
        nome = data.get("nome")
        data_nasc = data.get("data_nasc")
        telefone = data.get("telefone")
        email = data.get("email")
        status = data.get("status")

        try:
            # Formatar data se fornecida
            formatted_date = format_date_for_oracle(data_nasc)
            
            new_id = next_seq_val("PROFESSOR_SEQ", conn)
            
            # VULNERÁVEL: Usando concatenação de strings
            telefone_part = "NULL" if telefone is None else "'" + str(telefone) + "'"
            
            sql = "INSERT INTO PROFESSOR (ID_PROFESSOR, CPF, NOME, DATA_NASC, TELEFONE, EMAIL, STATUS) VALUES (" + str(new_id) + ", '" + str(cpf) + "', '" + str(nome) + "', TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD'), " + telefone_part + ", '" + str(email) + "', '" + str(status) + "')"
            
            cur.execute(sql)
            conn.commit()
            return jsonify({'id': new_id, 'message': 'Professor criado com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao criar professor: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/professors', methods=['GET'])
def list_professors():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT ID_PROFESSOR, CPF, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), TELEFONE, EMAIL, STATUS FROM PROFESSOR ORDER BY NOME"
        cur.execute(sql)
        rows = cur.fetchall()
        professors = []
        for row in rows:
            professors.append({
                'id_professor': row[0],
                'cpf': row[1],
                'nome': row[2],
                'data_nasc': row[3],
                'telefone': row[4],
                'email': row[5],
                'status': row[6]
            })
        return jsonify(professors), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar professores: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/professors/<int:professor_id>', methods=['GET'])
def get_professor_by_id(professor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT ID_PROFESSOR, CPF, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), TELEFONE, EMAIL, STATUS FROM PROFESSOR WHERE ID_PROFESSOR = :id"
        cur.execute(sql, {'id': professor_id})
        row = cur.fetchone()
        if row:
            professor = {
                'id_professor': row[0],
                'cpf': row[1],
                'nome': row[2],
                'data_nasc': row[3],
                'telefone': row[4],
                'email': row[5],
                'status': row[6]
            }
            return jsonify(professor), 200
        return jsonify({'error': 'Professor não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar professor: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/professors/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # Verificar se o professor existe
            cur.execute("SELECT COUNT(1) FROM PROFESSOR WHERE ID_PROFESSOR = :id", {'id': professor_id})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Professor não encontrado'}), 404

            # Construir query de atualização dinamicamente
            update_fields = []
            params = {'id': professor_id}
            
            if 'cpf' in data:
                update_fields.append("CPF = :cpf")
                params['cpf'] = data['cpf']
            
            if 'nome' in data:
                update_fields.append("NOME = :nome")
                params['nome'] = data['nome']
                
            if 'data_nasc' in data:
                formatted_date = format_date_for_oracle(data['data_nasc']) if data['data_nasc'] else None
                if formatted_date:
                    update_fields.append("DATA_NASC = TO_DATE(:data_nasc,'YYYY-MM-DD')")
                    params['data_nasc'] = formatted_date
                else:
                    update_fields.append("DATA_NASC = NULL")
                    
            if 'telefone' in data:
                update_fields.append("TELEFONE = :telefone")
                params['telefone'] = data['telefone']
                
            if 'email' in data:
                update_fields.append("EMAIL = :email")
                params['email'] = data['email']
                
            if 'status' in data:
                update_fields.append("STATUS = :status")
                params['status'] = data['status']

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = f"UPDATE PROFESSOR SET {', '.join(update_fields)} WHERE ID_PROFESSOR = :id"
            cur.execute(sql, params)
            conn.commit()
            
            return jsonify({'message': 'Professor atualizado com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar professor: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/professors/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se o professor tem ofertas
        cur.execute("SELECT COUNT(1) FROM OFERTA WHERE ID_PROFESSOR = :id", {'id': professor_id})
        offer_count = cur.fetchone()[0]
        if offer_count > 0:
            return jsonify({'error': 'Não é possível excluir professor com ofertas cadastradas'}), 400
        
        # Verificar se o professor existe
        cur.execute("SELECT COUNT(1) FROM PROFESSOR WHERE ID_PROFESSOR = :id", {'id': professor_id})
        professor_exists = cur.fetchone()[0]
        if professor_exists == 0:
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        # Deletar professor
        sql = "DELETE FROM PROFESSOR WHERE ID_PROFESSOR = :id"
        cur.execute(sql, {'id': professor_id})
        conn.commit()
        return jsonify({'message': 'Professor deletado com sucesso'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar professor: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
