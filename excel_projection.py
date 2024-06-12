import pandas as pd
import xlsxwriter
from sqlalchemy import create_engine

def export_to_excel(connection, year, month):
    """
    Εξάγει τα δεδομένα ενός συγκεκριμένου μήνα σε αρχείο Excel.
    
    :param connection: Σύνδεση στη βάση δεδομένων.
    :param year: Το έτος των δεδομένων που θα εξαχθούν.
    :param month: Ο μήνας των δεδομένων που θα εξαχθούν.
    """
    #Σύνδεση στη βάση δεδομένων
    engine = create_engine('mysql+mysqlconnector://root:1234qazwsx4321@localhost/transactionsdb')
    
    #Ανάκτηση δεδομένων για το καθορισμένο διάστημα
    query = """
    SELECT *
    FROM transactions
    WHERE YEAR(insert_date) = %s AND MONTH(insert_date) = %s
    """
    
    #Φόρτωση των αποτελεσμάτων του query σε ένα dataframe
    df = pd.read_sql_query(query, engine, params=(year, int(month.zfill(2))))

    if df.empty:
        print("Δεν βρέθηκαν δεδομένα για τον συγκεκριμένο μήνα.")
        return

    #Δημιουργία αρχείου Excel
    filename = f"transactions_{month}_{year}.xlsx"
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')  #Δημιουργία αντικειμένου τύπου excel

    #Εγγραφή του dataframe στο αρχείο excel
    df.to_excel(writer, sheet_name='Transactions', index=False)
    
    #Αποθήκευση φύλλου εργασίας σε ένα αντικείμενο
    worksheet = writer.sheets['Transactions']

    #Αυτόματη ρύθμιση του πλάτους της στήλης
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_index = df.columns.get_loc(column)
        worksheet.set_column(col_index, col_index, column_width)

    #Κλείσιμο και αποθήκευση του αρχείου Excel
    writer.close()
    print(f"Τα δεδομένα εξήχθησαν επιτυχώς στο αρχείο {filename}.")
