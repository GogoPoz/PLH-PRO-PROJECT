import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.dates import DateFormatter #Για την μορφοποίηση των ημερομηνιών πάνω στα γραφήματα

def category_stem_plot(start_date, end_date, category):
    """
    Δημιουργεί ένα stem plot γράφημα για μια συγκεκριμένη κατηγορία συναλλαγών στο καθορισμένο χρονικό διάστημα.
    
    :param start_date: Ημερομηνία έναρξης σε μορφή 'dd-mm-yyyy'
    :param end_date: Ημερομηνία λήξης σε μορφή 'dd-mm-yyyy'
    :param category: Κατηγορία συναλλαγών ('Τρόφιμα', 'Λογαριασμοί', 'Έκτακτα Εισοδήματα')
    """
    # Σύνδεση στη βάση δεδομένων
    engine = create_engine('mysql+mysqlconnector://root:1234qazwsx4321@localhost/transactionsdb')
    
    # Μετατροπή των ημερομηνιών στη μορφή 'yyyy-mm-dd', για αναγνώριση από την sql
    start_date_formatted = pd.to_datetime(start_date, format='%d-%m-%Y').strftime('%Y-%m-%d')
    end_date_formatted = pd.to_datetime(end_date, format='%d-%m-%Y').strftime('%Y-%m-%d')
    
    # Ανάκτηση δεδομένων για το καθορισμένο διάστημα και κατηγορία
    query = """
    SELECT insert_date, amount
    FROM transactions
    WHERE category = %s AND insert_date BETWEEN %s AND %s
    ORDER BY insert_date
    """
    
    #Φόρτωση των αποτελεσμάτων του query σε ένα dataframe
    df = pd.read_sql_query(query, engine, params=(category, start_date_formatted, end_date_formatted))
    
    #Τύπωση των παραμέτρων και δεδομένων για έλεγχο
    print(f"Query Parameters: {start_date, end_date, category}")
    print("DataFrame:")
    print(df)
    
    # Δημιουργία stem plot αν υπάρχουν δεδομένα
    if not df.empty:
        plt.figure(figsize=(10, 6))
        df['insert_date'] = pd.to_datetime(df['insert_date']) #Μετατροπή της στήλης insert_date του df από τύπο συμβολοσειράς σε αντικείμενα τύπου datetime

        # Καθορισμός χρώματος και θέσης δεδομένων
        if category in ['Τρόφιμα', 'Λογαριασμοί']:
            color = 'red'
            df['amount'] = -df['amount']  # Αναπαράσταση των εξόδων κάτω από το 0
        else:  # Έκτακτα Εισοδήματα, άνω του 0 
            color = 'blue'

        markerline, stemlines, baseline = plt.stem(df['insert_date'], df['amount'], linefmt=color, markerfmt='o', basefmt="k-") #Δημιουργία stem plot
        plt.setp(markerline, markersize=8)
        plt.setp(stemlines, linewidth=2)
        
        plt.xlabel('Ημερομηνία')
        plt.ylabel('Ποσό')
        plt.title(f'Stem plot για την κατηγορία {category}')
        plt.grid(True)
        
        #Μορφοποίηση άξονα ημερομηνιών
        date_form = DateFormatter("%d-%m-%Y")
        plt.gca().xaxis.set_major_formatter(date_form)
        plt.gcf().autofmt_xdate() 

        plt.show()
    else:
        print("Δεν βρέθηκαν δεδομένα για το καθορισμένο χρονικό διάστημα και κατηγορία.")

def all_categories_stem_plot(start_date, end_date):
    """
    Δημιουργεί ένα stem plot γράφημα για όλες τις κατηγορίες συναλλαγών στο καθορισμένο χρονικό διάστημα.
    
    :param start_date: Ημερομηνία έναρξης σε μορφή 'dd-mm-yyyy'
    :param end_date: Ημερομηνία λήξης σε μορφή 'dd-mm-yyyy'
    """
    categories = ['Τρόφιμα', 'Λογαριασμοί', 'Έκτακτα Εισοδήματα']
    colors = {'Τρόφιμα': 'red', 'Λογαριασμοί': 'green', 'Έκτακτα Εισοδήματα': 'blue'}
    
    #Σύνδεση στη βάση δεδομένων
    engine = create_engine('mysql+mysqlconnector://root:1234qazwsx4321@localhost/transactionsdb')
    
    #Μετατροπή των ημερομηνιών στη μορφή 'yyyy-mm-dd'
    start_date_formatted = pd.to_datetime(start_date, format='%d-%m-%Y').strftime('%Y-%m-%d')
    end_date_formatted = pd.to_datetime(end_date, format='%d-%m-%Y').strftime('%Y-%m-%d')
    
    plt.figure(figsize=(10, 6))
    
    for category in categories:
        #Ανάκτηση δεδομένων για το καθορισμένο διάστημα και κατηγορία
        query = """
        SELECT insert_date, amount
        FROM transactions
        WHERE category = %s AND insert_date BETWEEN %s AND %s
        ORDER BY insert_date
        """
        
        df = pd.read_sql_query(query, engine, params=(category, start_date_formatted, end_date_formatted))
        
        #Τύπωση των παραμέτρων και δεδομένων για έλεγχο
        print(f"Query Parameters: {start_date_formatted, end_date_formatted, category}")
        print("DataFrame:")
        print(df)
        
        if not df.empty:
            df['insert_date'] = pd.to_datetime(df['insert_date'])

            if category in ['Τρόφιμα', 'Λογαριασμοί']:
                df['amount'] = -df['amount']  #Αναπαράσταση των εξόδων κάτω από το 0

            plt.stem(df['insert_date'], df['amount'], linefmt=colors[category], markerfmt='o', basefmt="k-", label=category)

    plt.xlabel('Ημερομηνία')
    plt.ylabel('Ποσό')
    plt.title('Stem plot για όλες τις κατηγορίες')
    plt.grid(True)
    
    #Μορφοποίηση άξονα ημερομηνιών
    date_form = DateFormatter("%d-%m-%Y")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    plt.legend() #Προσθήκη υπομνήματος

    plt.show()
