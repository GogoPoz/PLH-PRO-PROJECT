import mysql.connector

MYSQL = mysql.connector


def open_connection():
    """ Η συνάρτηση δημιουργεί connection με το database"""
    try:
        return MYSQL.connect(
            host="localhost",
            user="db_finance_user",
            password="vsc127wx@127",
            database="financedb"
        )
    except MYSQL.Error as e:
        print("Error" + str(e))


def close_connection(connection):
    """Η συνάρτηση κλείνει το connection με το database"""
    try:
        connection.close()
    except MYSQL.Error as e:
        print("Error" + str(e))


def insert_data(connection, query):
    """H συνάρτηση εισάγει εγγραφή το query που θα πάρει ως όρισμα στο database"""
    cursor = connection.cursor()
    cursor.execute(query)
    lastrowid = None
    if cursor.lastrowid:
        lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid


def delete_or_update_data(connection, query):
    """Η συνάρτηση επεξεργάζεται η διαγράφει εγγραφές του database"""
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()


def query_fetch_all(connection, query):
    """H συνάρτηση επιστρέφει τα δεδομένα του query που παίρνει σαν όρισμα"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except MYSQL.Error as e:
        print("Error" + str(e))
