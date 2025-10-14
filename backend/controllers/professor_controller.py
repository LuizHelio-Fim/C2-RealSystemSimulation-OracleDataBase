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
            return jsonify({
                'success': False,
                'message': 'Dados JSON são obrigatórios'
            }), 400
        
        # Validar campos obrigatórios conforme schema do banco (NOT NULL)
        cpf = data.get('cpf')
        nome = data.get('nome')
        email = data.get('email')
        status = data.get('status')
        
        # Campos obrigatórios no banco PROFESSOR (CPF, NOME, EMAIL, STATUS são NOT NULL)
        if not all([cpf, nome, email, status]):
            return jsonify({
                'success': False,
                'message': 'Campos obrigatórios: cpf, nome, email, status'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # Campos opcionais
        data_nasc = data.get("data_nasc")
        telefone = data.get("telefone")

        try:
            # Formatar data se fornecida
            formatted_date = format_date_for_oracle(data_nasc) if data_nasc else None
            
            new_id = next_seq_val("PROFESSOR_ID_PROFESSOR_SEQ", conn)
            
            # VULNERÁVEL: Usando concatenação de strings
            data_part = "NULL" if formatted_date is None else "TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD')"
            telefone_part = "NULL" if telefone is None else "'" + str(telefone) + "'"
            
            sql = "INSERT INTO PROFESSORES (ID_PROFESSOR, CPF, NOME, DATA_NASC, TELEFONE, EMAIL, STATUS) VALUES (" + str(new_id) + ", '" + str(cpf) + "', '" + str(nome) + "', " + data_part + ", " + telefone_part + ", '" + str(email) + "', '" + str(status) + "')"
            
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Professor criado com sucesso',
                'data': {'id_professor': new_id}
            }), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar professor: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except ValueError as ve:
        return jsonify({
            'success': False,
            'message': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

@bp.route('/professors', methods=['GET'])
def list_professors():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # VULNERÁVEL: Usando concatenação de strings
        sql = "SELECT ID_PROFESSOR, CPF, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), TELEFONE, EMAIL, STATUS FROM PROFESSORES ORDER BY NOME"
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
        return jsonify({
            'success': True,
            'data': professors,
            'count': len(professors)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar professores: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/professors/<int:professor_id>', methods=['GET'])
def get_professor_by_id(professor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # VULNERÁVEL: Usando concatenação de strings
        sql = "SELECT ID_PROFESSOR, CPF, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), TELEFONE, EMAIL, STATUS FROM PROFESSORES WHERE ID_PROFESSOR = " + str(professor_id)
        cur.execute(sql)
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
            return jsonify({
                'success': True,
                'data': professor
            }), 200
        
        return jsonify({
            'success': False,
            'message': 'Professor não encontrado'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar professor: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/professors/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
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
            # VULNERÁVEL: Verificar se o professor existe
            sql_check = "SELECT COUNT(1) FROM PROFESSORES WHERE ID_PROFESSOR = " + str(professor_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Professor não encontrado'
                }), 404

            # VULNERÁVEL: Construir query de atualização dinamicamente
            update_parts = []
            
            if 'cpf' in data:
                cpf_val = "NULL" if data['cpf'] is None else "'" + str(data['cpf']) + "'"
                update_parts.append("CPF = " + cpf_val)
            
            if 'nome' in data:
                update_parts.append("NOME = '" + str(data['nome']) + "'")
                
            if 'data_nasc' in data:
                formatted_date = format_date_for_oracle(data['data_nasc']) if data['data_nasc'] else None
                if formatted_date:
                    update_parts.append("DATA_NASC = TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD')")
                else:
                    update_parts.append("DATA_NASC = NULL")
                    
            if 'telefone' in data:
                tel_val = "NULL" if data['telefone'] is None else "'" + str(data['telefone']) + "'"
                update_parts.append("TELEFONE = " + tel_val)
                
            if 'email' in data:
                update_parts.append("EMAIL = '" + str(data['email']) + "'")
                
            if 'status' in data:
                # STATUS é NOT NULL no banco, então deve ser fornecido e não pode ser vazio
                status_value = data['status']
                if status_value is None:
                    return jsonify({
                        'success': False,
                        'message': 'Campo status é obrigatório e não pode ser nulo'
                    }), 400
                
                # Converter para string e verificar se não está vazio
                status_str = str(status_value).strip()
                if not status_str:
                    return jsonify({
                        'success': False,
                        'message': 'Campo status é obrigatório e não pode estar vazio'
                    }), 400
                    
                update_parts.append("STATUS = '" + status_str + "'")

            if not update_parts:
                return jsonify({
                    'success': False,
                    'message': 'Nenhum campo para atualizar foi fornecido'
                }), 400

            sql = "UPDATE PROFESSORES SET " + ", ".join(update_parts) + " WHERE ID_PROFESSOR = " + str(professor_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Professor atualizado com sucesso'
            }), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar professor: {str(e)}'
            }), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except ValueError as ve:
        return jsonify({
            'success': False,
            'message': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500

@bp.route('/professors/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se professor possui ofertas (OFERTA.ID_PROFESSOR referencia PROFESSOR.ID_PROFESSOR)
        sql_check_offers = "SELECT COUNT(1) FROM OFERTAS WHERE ID_PROFESSOR = " + str(professor_id)
        cur.execute(sql_check_offers)
        offer_count = cur.fetchone()[0]
        if offer_count > 0:
            return jsonify({
                'success': False,
                'message': 'Professor possui ofertas cadastradas e não pode ser excluído. Remova-as antes.'
            }), 400
        
        # Verificar se o professor existe
        sql_exists = "SELECT COUNT(1) FROM PROFESSORES WHERE ID_PROFESSOR = " + str(professor_id)
        cur.execute(sql_exists)
        professor_exists = cur.fetchone()[0]
        if professor_exists == 0:
            return jsonify({
                'success': False,
                'message': 'Professor não encontrado'
            }), 404
        
        # VULNERÁVEL: Deletar professor
        sql = "DELETE FROM PROFESSORES WHERE ID_PROFESSOR = " + str(professor_id)
        cur.execute(sql)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Professor deletado com sucesso'
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar professor: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)
