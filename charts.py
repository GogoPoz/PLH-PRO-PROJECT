import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from db_functions import *
from class_transactions import *    

def top_expenses_bar_chart(start_date, end_date):
    """
    Δημιουργεί κατακόρυφο ραβδόγραμμα για τις πρώτες 3 κατηγορίες εξόδων με το μεγαλύτερο ποσό
    για το διάστημα που ορίζεται από τον χρήστη.
    """
    # Σύνδεση στη βάση δεδομένων
    engine = create_engine('mysql+mysqlconnector://root:1234qazwsx4321@localhost/transactionsdb')

    # Ανάκτηση δεδομένων για τον τρέχοντα μήνα
    query = """
    SELECT category, SUM(amount) as total_expense
    FROM transactions
    WHERE type_of_trans = 2 AND insert_date BETWEEN %s AND %s
    GROUP BY category
    ORDER BY total_expense DESC
    LIMIT 3
    """
    
    start_date_full = f"{start_date}-01"
    end_date_full = f"{end_date}-31"
    
    print(f"Query Parameters: {start_date_full}, {end_date_full}")
    
    df = pd.read_sql_query(query, engine, params=(start_date_full, end_date_full))
    
   # Αποσφαλμάτωση: Έλεγχος παραμέτρων και δεδομένων
    print(f"Query Parameters: {start_date_full}, {end_date_full}")
    print("DataFrame:")
    print(df)
    
    # Δημιουργία ραβδογράμματος
    # Δημιουργία ραβδογράμματος αν υπάρχουν δεδομένα
    if not df.empty:
        plt.bar(df['category'], df['total_expense'], color='blue')
        plt.xlabel('Κατηγορία')
        plt.ylabel('Ποσό')
        plt.title(f'3 Κορυφαίες Κατηγορίες Εξόδων από {start_date} έως {end_date}')
        plt.tight_layout()
        plt.show()
    else:
        print("Δεν βρέθηκαν δεδομένα για το συγκεκριμένο χρονικό διάστημα.")