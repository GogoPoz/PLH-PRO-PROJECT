import mysql.connector

MYSQL = mysql.connector


def open_connection():
    """ Η συνάρτηση δημιουργεί connection με το database"""
    try:
        return MYSQL.connect(
            host="localhost",
            user="root",
            password="1234qazwsx4321",
            database="transactionsdb"
        )
    except MYSQL.Error as e:
        print("Error" + str(e))


def close_connection(connection):
    """Η συνάρτηση κλείνει το connection με το database"""
    try:
        connection.close()
    except MYSQL.Error as e:
        print("Error" + str(e))


def import_sql_file(sql_file):
    try:
        with open(sql_file, 'r') as f:
            sql_script = f.read()
        return sql_script
    except FileNotFoundError:
        print("Το αρχείο SQL δεν βρέθηκε.")
        return None
    except Exception as e:
        print("Σφάλμα κατά την ανάγνωση του αρχείου SQL:", e)
        return None


def create_database():
    connection = open_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS transactionsdb")
            connection.commit()
            cursor.close()
            close_connection(connection)
            print("Η βάση δεδομένων δημιουργήθηκε επιτυχώς ή υπάρχει ήδη.")
        except MYSQL.Error as e:
            print("Error: " + str(e))
            close_connection(connection)
    else:
        print("Η σύνδεση στη βάση δεδομένων απέτυχε.")


def setup_database():
    create_database()
    connection = open_connection()
    if connection:
        try:
            # Σύνδεση στη συγκεκριμένη βάση δεδομένων
            connection.database = "transactionsdb"
            import_sql_file('transactions.sql')
            close_connection(connection)
        except MYSQL.Error as e:
            print("Error: " + str(e))
            close_connection(connection)
    else:
        print("Η σύνδεση στη βάση δεδομένων απέτυχε.")


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
