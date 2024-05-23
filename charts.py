import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from db_functions import *
from class_transactions import *    

def top_expenses_bar_chart():
    """
    Δημιουργεί κατακόρυφο ραβδόγραμμα για τις πρώτες 3 κατηγορίες εξόδων με το μεγαλύτερο ποσό
    για το διάστημα που ορίζεται από τον χρήστη.
    """
    # Σύνδεση στη βάση δεδομένων
    conn1 = open_connection()
    
    # Ανάκτηση δεδομένων για τον τρέχοντα μήνα
    query = """
    SELECT category, SUM(amount) as total_expense
    FROM transactions
    WHERE type_of_trans = 2 AND strftime('%Y-%m', insert_date) BETWEEN ? AND ?
    GROUP BY category
    ORDER BY total_amount DESC
    LIMIT 3
    """
    
    df = pd.read_sql_query(query, conn1,parameters=(start_date, end_date))
    
    # Κλείσιμο της σύνδεσης με τη βάση δεδομένων
    conn1.close()
    
    # Δημιουργία ραβδογράμματος
    plt.bar(df['category'], df['total_expense'], color='blue')
    plt.xlabel('Κατηγορία')
    plt.ylabel('Ποσό')
    plt.title(f'3 Κορυφαίες Κατηγορίες Εξόδων από {start_date} έως {end_date}')
    plt.show()
