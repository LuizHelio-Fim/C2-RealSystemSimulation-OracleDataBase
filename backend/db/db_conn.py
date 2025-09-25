import oracledb
import os

def get_db_connection():
    """
    Establishes and returns a connection to the Oracle database using environment variables for configuration.
    
    Environment Variables:
    - DB_USER: Database username
    - DB_PASSWORD: Database password
    - DB_DSN: Data Source Name (DSN) for the database connection
    
    Returns:
        oracledb.Connection: A connection object to the Oracle database.
    """
    user = os.getenv('labdatabase')
    password = os.getenv('lab@Database2025')
    dsn = os.getenv('XEPDB1')

    if not all([user, password, dsn]):
        raise ValueError("As variaveis de configuração do ambiente não estão definidas corretamente.")

    connection = oracledb.connect(user=user, password=password, dsn=dsn)
    return connection