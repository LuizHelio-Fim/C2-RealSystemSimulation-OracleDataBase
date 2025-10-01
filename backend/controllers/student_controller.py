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
            sql = """
            INSERT INTO student (id, matricula, cpf, nome, data_nasc, telefone, email, periodo, course_id, status_curso)
            VALUES (:id, :matricula, :cpf, :nome,
                    CASE WHEN :data_nasc IS NULL THEN NULL ELSE TO_DATE(:data_nasc,'YYYY-MM-DD') END,
                    :telefone, :email, :periodo, :course_id, :status_curso)
            """
            cur.execute(sql, {
                'id': new_id,
                'matricula': matricula,
                'cpf': cpf,
                'nome': nome,
                'data_nasc': formatted_date,
                'telefone': telefone,
                'email': email,
                'periodo': periodo,
                'course_id': course_id,
                'status_curso': status_curso
            })
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
        sql = "SELECT id, matricula, cpf, nome, TO_CHAR(data_nasc, 'YYYY-MM-DD'), telefone, email, periodo, course_id, status_curso FROM student ORDER BY nome"
        cur.execute(sql)
        rows = cur.fetchall()
        students = []
        for row in rows:
            students.append({
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
            # Verificar se o estudante existe
            cur.execute("SELECT COUNT(1) FROM student WHERE id = :id", {'id': student_id})
            if cur.fetchone()[0] == 0:
                return jsonify({'error': 'Estudante não encontrado'}), 404

            # Construir query de atualização dinamicamente
            update_fields = []
            params = {'id': student_id}
            
            if 'matricula' in data:
                update_fields.append("matricula = :matricula")
                params['matricula'] = data['matricula']
            
            if 'nome' in data:
                update_fields.append("nome = :nome")
                params['nome'] = data['nome']
                
            if 'cpf' in data:
                update_fields.append("cpf = :cpf")
                params['cpf'] = data['cpf']
                
            if 'data_nasc' in data:
                formatted_date = format_date_for_oracle(data['data_nasc']) if data['data_nasc'] else None
                if formatted_date:
                    update_fields.append("data_nasc = TO_DATE(:data_nasc,'YYYY-MM-DD')")
                    params['data_nasc'] = formatted_date
                else:
                    update_fields.append("data_nasc = NULL")
                    
            if 'telefone' in data:
                update_fields.append("telefone = :telefone")
                params['telefone'] = data['telefone']
                
            if 'email' in data:
                update_fields.append("email = :email")
                params['email'] = data['email']
                
            if 'periodo' in data:
                update_fields.append("periodo = :periodo")
                params['periodo'] = data['periodo']
                
            if 'course_id' in data:
                update_fields.append("course_id = :course_id")
                params['course_id'] = data['course_id']
                
            if 'status_curso' in data:
                update_fields.append("status_curso = :status_curso")
                params['status_curso'] = data['status_curso']

            if not update_fields:
                return jsonify({'error': 'Nenhum campo para atualizar foi fornecido'}), 400

            sql = f"UPDATE student SET {', '.join(update_fields)} WHERE id = :id"
            cur.execute(sql, params)
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
        sql = "SELECT id, matricula, cpf, nome, TO_CHAR(data_nasc, 'YYYY-MM-DD'), telefone, email, periodo, course_id, status_curso FROM student WHERE id = :id"
        cur.execute(sql, {'id': student_id})
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
        # Check if student has grades
        cur.execute("SELECT COUNT(1) FROM grade_aluno WHERE aluno_id = :id", {'id': student_id})
        cnt = cur.fetchone()[0]
        if cnt > 0:
            return jsonify({'error': 'Aluno possui notas matricula e não pode ser excluído, remova-as antes.'}), 400
        
        # Check if student exists
        cur.execute("SELECT COUNT(1) FROM student WHERE id = :id", {'id': student_id})
        student_exists = cur.fetchone()[0]
        if student_exists == 0:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Delete student
        sql = "DELETE FROM student WHERE id = :id"
        cur.execute(sql, {'id': student_id})
        conn.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Erro ao deletar estudante: {str(e)}'}), 500
    finally:
        cur.close()
        release_connection(conn)
