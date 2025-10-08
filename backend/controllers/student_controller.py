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
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['matricula', 'nome', 'email', 'periodo', 'course_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400

        conn = get_connection()
        cur = conn.cursor()

        matricula = data.get("matricula")
        nome = data.get("nome")
        data_nasc = data.get("data_nasc")
        cpf = data.get("cpf")
        telefone = data.get("telefone")
        email = data.get("email")
        periodo = data.get("periodo")
        course_id = data.get("course_id")
        status_curso = data.get("status_curso")

        try:
            # Formatar data se fornecida
            formatted_date = format_date_for_oracle(data_nasc) if data_nasc else None
            
            new_id = next_seq_val("seq_student", conn)
            
            # VULNERÁVEL: Usando concatenação de strings
            data_part = "NULL" if formatted_date is None else "TO_DATE('" + str(formatted_date) + "','YYYY-MM-DD')"
            telefone_part = "NULL" if telefone is None else "'" + str(telefone) + "'"
            cpf_part = "NULL" if cpf is None else "'" + str(cpf) + "'"
            status_part = "NULL" if status_curso is None else "'" + str(status_curso) + "'"
            
            sql = "INSERT INTO ALUNO (MATRICULA, CPF, NOME, DATA_NASC, TELEFONE, EMAIL, PERIODO, ID_CURSO, STATUS_CURSO) VALUES (" + str(matricula) + ", " + cpf_part + ", '" + str(nome) + "', " + data_part + ", " + telefone_part + ", '" + str(email) + "', " + str(periodo) + ", " + str(course_id) + ", " + status_part + ")"
            
            cur.execute(sql)
            conn.commit()
            return jsonify({'id': new_id, 'message': 'Estudante criado com sucesso'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao criar estudante: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

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
        return jsonify(students), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar estudantes: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400

        conn = get_connection()
        cur = conn.cursor()

        try:
            # VULNERÁVEL: Verificar se o estudante existe
            sql_check = "SELECT COUNT(1) FROM ALUNO WHERE MATRICULA = " + str(student_id)
            cur.execute(sql_check)
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Estudante não encontrado'}), 404

            # VULNERÁVEL: Construir query de atualização dinamicamente
            update_parts = []
            
            if 'matricula' in data:
                update_parts.append("MATRICULA = " + str(data['matricula']))
            
            if 'nome' in data:
                update_parts.append("NOME = '" + str(data['nome']) + "'")
                
            if 'cpf' in data:
                cpf_val = "NULL" if data['cpf'] is None else "'" + str(data['cpf']) + "'"
                update_parts.append("CPF = " + cpf_val)
                
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
                
            if 'periodo' in data:
                update_parts.append("PERIODO = " + str(data['periodo']))
                
            if 'course_id' in data:
                update_parts.append("ID_CURSO = " + str(data['course_id']))
                
            if 'status_curso' in data:
                status_val = "NULL" if data['status_curso'] is None else "'" + str(data['status_curso']) + "'"
                update_parts.append("STATUS_CURSO = " + status_val)

            if not update_parts:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = "UPDATE ALUNO SET " + ", ".join(update_parts) + " WHERE MATRICULA = " + str(student_id)
            cur.execute(sql)
            conn.commit()
            
            return jsonify({'message': 'Estudante atualizado com sucesso'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Erro ao atualizar estudante: {str(e)}'}), 500
        finally:
            cur.close()
            release_connection(conn)
            
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

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
                'id': row[0],
                'matricula': row[1],
                'cpf': row[2],
                'nome': row[3],
                'data_nasc': row[4],
                'telefone': row[5],
                'email': row[6],
                'periodo': row[7],
                'course_id': row[8],
                'status_curso': row[9]
            }
            return jsonify(student), 200
        return jsonify({'error': 'Estudante não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar estudante: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)

@bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # VULNERÁVEL: Check if student has grades
        sql_check = "SELECT COUNT(1) FROM GRADE_ALUNO WHERE ID_ALUNO = " + str(student_id)
        cur.execute(sql_check)
        cnt = cur.fetchone()[0]
        if cnt > 0:
            return jsonify({'error': 'Aluno possui notas matricula e não pode ser excluído, remova-as antes.'}), 400
        
        # VULNERÁVEL: Check if student exists
        sql_exists = "SELECT COUNT(1) FROM ALUNO WHERE MATRICULA = " + str(student_id)
        cur.execute(sql_exists)
        student_exists = cur.fetchone()[0]
        if student_exists == 0:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # VULNERÁVEL: Delete student
        sql = "DELETE FROM ALUNO WHERE MATRICULA = " + str(student_id)
        cur.execute(sql)
        conn.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar estudante: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
