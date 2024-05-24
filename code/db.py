import pymysql
import datetime

# Establishing connection to the database
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="MyConnection",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Creating a cursor object
cursor = conn.cursor()

# Defining the data to be inserted
data_to_insert = [
    (2, "Kaka", "Kenneth", "2023-12-06", "kennethjanoras@gmail.com", "2023-12-17 17:06:14", "2023-12-28 18:48:51"),
    (3, "Hassan", "Radzni", "2023-12-19", "radzni@gmail.com", "2023-12-28 18:44:39", "2023-12-28 18:44:39"),
    (6, "Loa", "Kedsz", "2023-12-10", "keds@gmail.com", "2023-12-28 18:57:41", "2023-12-28 18:57:41")
]

# Inserting data into the employee table
for item in data_to_insert:
    sql_query = """INSERT INTO employee (id_auto, first_name, last_name, date_of_birth, email, created_at, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql_query, item)

# Committing the transaction and closing the connection
conn.commit()
conn.close()
