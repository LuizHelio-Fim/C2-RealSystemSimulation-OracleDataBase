from db.db_conn import get_db_connection

def get_next_student_id(conn):
    """
    Retrieves the next available student ID by finding the current maximum ID in the students table and adding one.
    
    Returns:
        int: The next available student ID.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT seq_student_id.NEXTVAL FROM dual")
        next_id = cursor.fetchone()[0]
        return next_id
    finally:
        cursor.close()
        connection.close()

def insert_student(matricula, nome, data_nasc, telefone, email):
    """
    Inserts a new student record into the students table.
    
    Args:
        matricula (str): The matricula of the student.
        nome (str): The name of the student.
        data_nasc (str): The birth date of the student.
        telefone (str): The phone number of the student.
        email (str): The email address of the student.

    Returns:
        int: The ID of the newly inserted student.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        student_id = get_next_student_id(connection)
        cursor.execute(
            "INSERT INTO students (id, matricula, nome, data_nasc, telefone, email) VALUES (:id, :matricula, :nome, :data_nasc, :telefone, :email)",
            id=student_id, matricula=matricula, nome=nome, data_nasc=data_nasc, telefone=telefone, email=email
        )
        connection.commit()
        return student_id
    finally:
        cursor.close()
        connection.close()

def list_students():
    """
    Retrieves all student records from the students table.
    
    Returns:
        list of dict: A list of dictionaries, each representing a student record.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT id, matricula, nome, data_nasc, telefone, email FROM students ORDER BY nome")
        rows = cursor.fetchall()
        students = []
        for row in rows:
            students.append({
                'id': row[0],
                'matricula': row[1],
                'nome': row[2],
                'data_nasc': row[3],
                'telefone': row[4],
                'email': row[5]
            })
        return students
    finally:
        cursor.close()
        connection.close()

def delete_student(student_id):
    """
    Deletes a student record from the students table based on the provided student ID.
    
    Args:
        student_id (int): The ID of the student to be deleted.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(1) FROM GRADE_ALUNO WHERE aluno_id = :id", id=student_id)
    cnt = cursor.fetchone()[0]
    if cnt > 0:
        cursor.close()
        connection.close()
        raise ValueError("Aluno possui notas cadastradas, não pode ser excluído.")
    try:
        cursor.execute("DELETE FROM students WHERE id = :id", id=student_id)
        connection.commit()
    finally:
        cursor.close()
        connection.close()