from flask import Blueprint, request, jsonify
from db.db_conn import get_connection, release_connection, next_seq_val
from datetime import datetime

bp = Blueprint('student', __name__)

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
    return dt_str

@bp.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados JSON são obrigatórios'
            }), 400
        
        # Validar campos obrigatórios conforme schema do banco (CPF e STATUS_CURSO são NOT NULL)
        matricula = data.get('matricula')
        nome = data.get('nome')
        cpf = data.get('cpf')
        email = data.get('email')
        periodo = data.get('periodo')
        id_curso = data.get('id_curso')
        status_curso = data.get('status_curso')
        
        # Todos estes campos são NOT NULL no banco ALUNO
        if not all([matricula, nome, cpf, email, periodo, id_curso, status_curso]):
            return jsonify({
                'success': False,
                'message': 'Campos obrigatórios: matricula, nome, cpf, email, periodo, id_curso, status_curso'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # Campos opcionais
        data_nasc = data.get("data_nasc")
        telefone = data.get("telefone")

        try:
            # Formatar data se fornecida
            formatted_date = format_date_for_oracle(data_nasc) if data_nasc else None
            
            data_part = "NULL" if formatted_date is None else "TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD')"
            telefone_part = "NULL" if telefone is None else "'" + str(telefone) + "'"
            
            # CPF e STATUS_CURSO são obrigatórios, não podem ser NULL
            sql = "INSERT INTO ALUNO (MATRICULA, CPF, NOME, DATA_NASC, TELEFONE, EMAIL, PERIODO, ID_CURSO, STATUS_CURSO) VALUES (" + str(matricula) + ", '" + str(cpf) + "', '" + str(nome) + "', " + data_part + ", " + telefone_part + ", '" + str(email) + "', " + str(periodo) + ", " + str(id_curso) + ", '" + str(status_curso) + "')"
            
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Estudante criado com sucesso',
                'data': {'matricula': matricula}
            }), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar estudante: {str(e)}'
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

@bp.route('/students', methods=['GET'])
def list_students():
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "SELECT MATRICULA, CPF, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), TELEFONE, EMAIL, PERIODO, ID_CURSO, STATUS_CURSO FROM ALUNO ORDER BY NOME"
        cur.execute(sql)
        rows = cur.fetchall()
        students = []
        for row in rows:
            students.append({
                'matricula': row[0],
                'cpf': row[1],
                'nome': row[2],
                'data_nasc': row[3],
                'telefone': row[4],
                'email': row[5],
                'periodo': row[6],
                'id_curso': row[7],
                'status_curso': row[8]
            })
        return jsonify({
            'success': True,
            'data': students,
            'count': len(students)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar estudantes: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # VULNERÁVEL: Usando concatenação de strings
        sql = "SELECT MATRICULA, CPF, NOME, TO_CHAR(DATA_NASC, 'YYYY-MM-DD'), TELEFONE, EMAIL, PERIODO, ID_CURSO, STATUS_CURSO FROM ALUNO WHERE MATRICULA = " + str(student_id)
        cur.execute(sql)
        row = cur.fetchone()
        
        if row:
            student = {
                'matricula': row[0],
                'cpf': row[1],
                'nome': row[2],
                'data_nasc': row[3],
                'telefone': row[4],
                'email': row[5],
                'periodo': row[6],
                'id_curso': row[7],
                'status_curso': row[8]
            }
            return jsonify({
                'success': True,
                'data': student
            }), 200
        
        return jsonify({
            'success': False,
            'message': 'Estudante não encontrado'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar estudante: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
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
            # VULNERÁVEL: Verificar se o estudante existe
            sql_check = "SELECT COUNT(1) FROM ALUNO WHERE MATRICULA = " + str(student_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({
                    'success': False,
                    'message': 'Estudante não encontrado'
                }), 404

            # VULNERÁVEL: Construir query de atualização dinamicamente
            update_parts = []
            
            if 'matricula' in data:
                update_parts.append("MATRICULA = " + str(data['matricula']))
            
            if 'nome' in data:
                update_parts.append("NOME = '" + str(data['nome']) + "'")
                
            if 'cpf' in data:
                cpf_val = "NULL" if data['cpf'] is None else "'" + str(data['cpf']) + "'"
                update_parts.append("CPF = " + cpf_val)
                
            # Aceitar ambos os formatos de data
            data_nasc = data.get('data_nasc') or data.get('data_nascimento')
            if data_nasc is not None:
                formatted_date = format_date_for_oracle(data_nasc) if data_nasc else None
                if formatted_date:
                    update_parts.append("DATA_NASC = TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD')")
                else:
                    update_parts.append("DATA_NASC = NULL")
                    
            if 'telefone' in data:
                tel_val = "NULL" if data['telefone'] is None else "'" + str(data['telefone']) + "'"
                update_parts.append("TELEFONE = " + tel_val)
                
            if 'email' in data:
                update_parts.append("EMAIL = '" + str(data['email']) + "'")
                
            if 'periodo' in data:
                update_parts.append("PERIODO = " + str(data['periodo']))
                
            # Aceitar ambos os formatos
            id_curso = data.get('id_curso') or data.get('course_id')
            if id_curso is not None:
                update_parts.append("ID_CURSO = " + str(id_curso))
                
            if 'status_curso' in data:
                status_val = "NULL" if data['status_curso'] is None else "'" + str(data['status_curso']) + "'"
                update_parts.append("STATUS_CURSO = " + status_val)

            if not update_parts:
                return jsonify({
                    'success': False,
                    'message': 'Nenhum campo para atualizar foi fornecido'
                }), 400

            sql = "UPDATE ALUNO SET " + ", ".join(update_parts) + " WHERE MATRICULA = " + str(student_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Estudante atualizado com sucesso'
            }), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar estudante: {str(e)}'
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

@bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verificar se aluno possui matrículas (GRADE_ALUNO.ID_ALUNO referencia ALUNO.MATRICULA)
        sql_check = "SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_ALUNO = " + str(student_id)
        cur.execute(sql_check)
        cnt = cur.fetchone()[0]
        if cnt > 0:
            return jsonify({
                'success': False,
                'message': 'Aluno possui matrículas e não pode ser excluído. Remova-as antes.'
            }), 400
        
        # Verificar se aluno possui notas (AVALIACAO_ALUNO.ID_ALUNO referencia ALUNO.MATRICULA)
        sql_check_grades = "SELECT COUNT(1) FROM AVALIACAO_ALUNO WHERE ID_ALUNO = " + str(student_id)
        cur.execute(sql_check_grades)
        grade_cnt = cur.fetchone()[0]
        if grade_cnt > 0:
            return jsonify({
                'success': False,
                'message': 'Aluno possui notas registradas e não pode ser excluído. Remova-as antes.'
            }), 400
        
        # VULNERÁVEL: Check if student exists
        sql_exists = "SELECT COUNT(1) FROM ALUNO WHERE MATRICULA = " + str(student_id)
        cur.execute(sql_exists)
        student_exists = cur.fetchone()[0]
        if student_exists == 0:
            return jsonify({
                'success': False,
                'message': 'Estudante não encontrado'
            }), 404
        
        # VULNERÁVEL: Delete student
        sql = "DELETE FROM ALUNO WHERE MATRICULA = " + str(student_id)
        cur.execute(sql)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Estudante deletado com sucesso'
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro ao deletar estudante: {str(e)}'
        }), 500
    finally:
        cur.close()
        release_connection(conn)
