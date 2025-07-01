import pandas as pd
import mysql.connector
from mysql.connector import Error

def upload_df_to_mysql(hostname, port, username, password, database, table_name, df, create_table_sql):
    try:
        connection = mysql.connector.connect(
            host=hostname, 
            database=database, 
            user=username, 
            password=password, 
            port=port
        )
        if connection.is_connected():
            print(f"Connected to MySQL Server version {connection.get_server_info()}")
            cursor = connection.cursor()
            
            # Drop table if exists
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Dropped table {table_name} if it existed.")
            
            # Create table
            cursor.execute(create_table_sql)
            print(f"Created table {table_name}.")
            
            # Prepare insert statement
            cols = ", ".join(df.columns)
            placeholders = ", ".join(["%s"] * len(df.columns))
            insert_sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
            
            # Convert DataFrame to list of tuples
            values = [tuple(row) for row in df.values]
            
            # Insert data
            cursor.executemany(insert_sql, values)
            connection.commit()
            print(f"Inserted {cursor.rowcount} rows into {table_name}.")
            
    except Error as e:
        print("Error while connecting or operating on MySQL:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def need_to_name(config):
    host = config['mysql']['host']
    port = config['mysql']['port']
    username = config['mysql']['username']
    password = config['mysql']['password']
    database = config['mysql']['database']

    ccl_file_path = config['fec_data_files'][0]['file']
    ccl_columns = config['fec_data_files'][0]['columns']
    ccl_table_name = config['fec_data_files'][0]['table_name']

    # Read file without header; assign columns from config
    ccl_df = pd.read_csv(ccl_file_path, sep='|', header=None)
    ccl_df.columns = ccl_columns

    # Convert all columns to string (optional, depends on your data)
    ccl_df = ccl_df.astype(str)

    # Create table SQL
    ccl_create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {ccl_table_name} (
            {', '.join([f"`{col}` VARCHAR(255)" for col in ccl_columns])}
        )
    """

    upload_df_to_mysql(host, port, username, password, database, ccl_table_name, ccl_df, ccl_create_table_sql)

    cm_file_path = config['fec_data_files'][1]['file']
    cm_columns = config['fec_data_files'][1]['columns']
    cm_table_name = config['fec_data_files'][1]['table_name']

    # Read file without header; assign columns from config
    cm_df = pd.read_csv(cm_file_path, sep='|', header=None)
    cm_df.columns = cm_columns

    # Convert all columns to string (optional, depends on your data)
    cm_df = cm_df.astype(str)


    # Create table SQL
    cm_create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {cm_table_name} (
            {', '.join([f"`{col}` VARCHAR(255)" for col in cm_columns])}
        )
    """

    upload_df_to_mysql(host, port, username, password, database, cm_table_name, cm_df, cm_create_table_sql)