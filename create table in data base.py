import mysql.connector

try:
    conn = mysql.connector.connect(host="localhost", database="atenddance", user="root", password="")
    tc = "CREATE TABLE attendance(st_name varchar(50) NOT NULL,curent_time TIME STEMP ,date DATE )"
    mycursor = conn.cursor()
    result = mycursor.execute(tc)
    print("atendance table creat sucssesfully.....")

except mysql.connector.Error as error:
    print("fail to creat a table in mysql:{}".format(error))
finally:
    if conn.is_connected():
        mycursor.close()
        conn.close()
        print("mysql is closed...")
