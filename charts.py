import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
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
    
    
    #Έλεγχος παραμέτρων
    print(f"Query Parameters: {start_date}, {end_date}")
    
    df = pd.read_sql_query(query, engine, params=(start_date, end_date))
    
    #Έλεγχος δεδομένων
    print(f"Query Parameters: {start_date}, {end_date}")
    print("DataFrame:")
    print(df)
    
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


def category_expense_pie_chart(start_date, end_date):
    """
    Δημιουργεί ένα pie chart που αναπαριστά τα ποσοστά από όλες τις κατηγορίες
    εξόδων στο διάστημα που ορίζεται από τον χρήστη.
    """
    # Σύνδεση στη βάση δεδομένων
    engine = create_engine('mysql+mysqlconnector://root:1234qazwsx4321@localhost/transactionsdb')

    # Ανάκτηση δεδομένων για το καθορισμένο διάστημα
    query = """
    SELECT category, SUM(amount) as total_expense
    FROM transactions
    WHERE type_of_trans = 2 AND insert_date BETWEEN %s AND %s
    GROUP BY category
    """

 
    #Έλεγχος παραμέτρων
    print(f"Query Parameters: {start_date}, {end_date}")
    
    df = pd.read_sql_query(query, engine, params=(start_date, end_date))
    
    #Έλεγχος δεδομένων
    print(f"Query Parameters: {start_date}, {end_date}")
    print("DataFrame:")
    print(df)
    
    #Δημιουργία pie chart αν υπάρχουν δεδομένα
    if not df.empty:
        plt.figure(figsize=(8, 8))
        plt.pie(df['total_expense'], labels=df['category'], autopct='%1.1f%%', startangle=140)
        plt.title(f'Ποσοστά Εξόδων ανά Κατηγορία από {start_date} έως {end_date}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        plt.show()
    else:
        print("Δεν βρέθηκαν δεδομένα για το συγκεκριμένο χρονικό διάστημα.")



def trans_analysis_line_chart(start_date, end_date):
    """
    Δημιουργεί ένα γραμμικό διάγραμμα που αναπαριστά το ποσό κάθε εσόδου και εξόδου
    για το διάστημα που ορίζεται από τον χρήστη.
    """
    # Σύνδεση στη βάση δεδομένων
    engine = create_engine('mysql+mysqlconnector://root:1234qazwsx4321@localhost/transactionsdb')

    # Ανάκτηση δεδομένων για το καθορισμένο διάστημα
    query = """
    SELECT insert_date, amount, type_of_trans
    FROM transactions
    WHERE insert_date BETWEEN %s AND %s
    ORDER BY insert_date
    """

    df = pd.read_sql_query(query, engine, params=(start_date, end_date))
    
    #Έλεγχος δεδομένων
    print(f"Query Parameters: {start_date}, {end_date}")
    print("DataFrame:")
    print(df)
    
    # Δημιουργία γραμμικού διαγράμματος αν υπάρχουν δεδομένα
    if not df.empty:
        plt.figure(figsize=(10, 6))
        
        # Φιλτράρισμα για έσοδα και έξοδα
        income_df = df[df['type_of_trans'] == 1]
        expense_df = df[df['type_of_trans'] == 2]
        
        # Σχεδίαση γραμμών για έσοδα και έξοδα
        plt.plot(income_df['insert_date'], income_df['amount'], marker='o', linestyle='-', color='g', label='Έσοδα')
        plt.plot(expense_df['insert_date'], expense_df['amount'], marker='o', linestyle='-', color='r', label='Έξοδα')
        
        plt.xlabel('Ημερομηνία')
        plt.ylabel('Ποσό')
        plt.title(f'Ποσά Εσόδων και Εξόδων από {start_date} έως {end_date}')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("Δεν βρέθηκαν δεδομένα για το συγκεκριμένο χρονικό διάστημα.")
        
            
