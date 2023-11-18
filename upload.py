import psycopg2
import mysql.connector
from pprint import pprint

def local():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port=3306,
        database="users"
    )

    mycursor = mydb.cursor()
    get_user_query = "select * from users;"
    mycursor.execute(get_user_query )
    all = mycursor.fetchall()
    mydb.close()
    pprint("ended local fetch")
    pprint(all)
    return all

def flo(all):
    mydb = psycopg2.connect(
        host="ep-yellow-wave-54660248.ap-southeast-1.aws.neon.fl0.io",
        user="fl0user",
        password="PNFY3rXkWDs2",
        port=5432,
        database="users",
        sslmode="require",
    )

    mycursor = mydb.cursor()

    for i in all:
        id, unified_id, rollno, name = i
        add_user_query = """
        insert into users(unified_id, rollno, name)
        values(%s, %s, %s)
        """
        user_data = (unified_id, rollno, name)
        print(user_data)
        try:
            mycursor.execute(add_user_query, user_data)
            print(f'ADDED: {user_data}')
        except Exception as e:
            print(f"Error adding user {user_data}", e)


    mydb.commit()
    mydb.close()
    return 0

if __name__ == "__main__":
    flo(local())
