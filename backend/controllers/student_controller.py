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
        
        # Validar campos obrigatórios (matrícula será gerada automaticamente)
        nome = data.get('nome')
        cpf = data.get('cpf')
        email = data.get('email')
        periodo = data.get('periodo')
        id_curso = data.get('id_curso')  
        status_curso = data.get('status_curso')
        
        # Debug: log dos dados recebidos
        print(f"Dados recebidos: {data}")
        
        # Validação dos campos obrigatórios (exceto matrícula que será gerada)
        missing_fields = []
        if not nome or nome.strip() == '':
            missing_fields.append('nome')
        if not cpf or cpf.strip() == '':
            missing_fields.append('cpf')
        if not email or email.strip() == '':
            missing_fields.append('email')
        if periodo is None or periodo == '':
            missing_fields.append('periodo')
        if not id_curso or id_curso == '':
            missing_fields.append('id_curso')
        if not status_curso or status_curso.strip() == '':
            missing_fields.append('status_curso')
            
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Campos obrigatórios ausentes ou vazios: {", ".join(missing_fields)}'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # Campos opcionais
        data_nasc = data.get("data_nasc")
        telefone = data.get("telefone")

        try:
            # Gerar matrícula automaticamente: YYYYCCNN 
            # YYYY = Ano atual, CC = ID do curso (2 dígitos), NN = contador sequencial
            from datetime import datetime
            ano_atual = datetime.now().year
            
            # Formatar ID do curso com 2 dígitos (ex: 1 -> 01, 10 -> 10)
            curso_formatted = str(id_curso).zfill(2)
            
            # Buscar o próximo número sequencial para este curso neste ano
            cur.execute(f"""
                SELECT NVL(MAX(
                    CASE 
                        WHEN MATRICULA LIKE '{ano_atual}{curso_formatted}%' 
                        THEN TO_NUMBER(SUBSTR(MATRICULA, -2))
                        ELSE 0 
                    END
                ), 0) + 1 
                FROM ALUNO 
                WHERE ID_CURSO = {id_curso}
            """)
            proximo_numero = cur.fetchone()[0]
            
            # Formatar número sequencial com 2 dígitos (ex: 1 -> 01)
            numero_formatted = str(proximo_numero).zfill(2)
            
            # Gerar matrícula final: YYYYCCNN
            matricula = f"{ano_atual}{curso_formatted}{numero_formatted}"
            print(f"Matrícula gerada: {matricula}")
            
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
                try:
                    formatted_date = format_date_for_oracle(data_nasc) if data_nasc else None
                    if formatted_date:
                        update_parts.append("DATA_NASC = TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD')")
                    else:
                        update_parts.append("DATA_NASC = NULL")
                except ValueError as ve:
                    return jsonify({
                        'success': False,
                        'message': f'Erro ao atualizar estudante: {str(ve)}'
                    }), 400
                    
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
