import mysql.connector
from mysql.connector import Error
import os
from io import BytesIO
from PIL import Image

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2312",
            database="intern_test",
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_employee_table():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee (
                    emp_id VARCHAR(50) PRIMARY KEY,
                    emp_name VARCHAR(100),
                    mobile_num VARCHAR(15),
                    email VARCHAR(100)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee_photos (
                    emp_id VARCHAR(50),
                    photo_1 LONGBLOB,
                    photo_2 LONGBLOB,
                    photo_3 LONGBLOB,
                    photo_4 LONGBLOB,
                    photo_5 LONGBLOB,
                    photo_6 LONGBLOB,
                    photo_7 LONGBLOB,
                    photo_8 LONGBLOB,
                    photo_9 LONGBLOB,
                    photo_10 LONGBLOB,
                    photo_11 LONGBLOB,
                    photo_12 LONGBLOB,
                    photo_13 LONGBLOB,
                    photo_14 LONGBLOB,
                    photo_15 LONGBLOB,
                    PRIMARY KEY (emp_id),
                    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    emp_id VARCHAR(50),
                    punch_in DATETIME,
                    punch_out DATETIME,
                    FOREIGN KEY (emp_id) REFERENCES employee (emp_id)
                )
            """)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error: {e}")

def image_storer(emp_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT id, emp_id, photo_1, photo_2, photo_3, photo_4, photo_5, photo_6, photo_7, photo_8, photo_9, photo_10, photo_11, photo_12, photo_13, photo_14, photo_15 FROM employee_photos where emp_ID =%s
                    """, (emp_id,))
    os.makedirs('stored_images', exist_ok=True)
    for row in cursor.fetchall():
        emp_id_1 = row[1]
        for i in range(2, 17):
            photo = row[i]
            if photo:
                image = Image.open(BytesIO(photo))
                image_path = f'stored_images/{emp_id_1}_photo_{i-1}.png'
                image.save(image_path)
                
create_employee_table()
