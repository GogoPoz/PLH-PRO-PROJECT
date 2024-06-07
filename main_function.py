from class_transactions import *
from db_functions import *
from charts import *
from datetime import datetime

def main():
    connection = open_connection()
    transaction = Transactions(connection)
    
    #Κλήση της load_monthly για ενημέρωση των συναλλαγών βάσει της σημερινής ημερομηνίας
    transaction.load_monthly()

    while True:
        # 1ο στάδιο επιλογής ενέργειας (αρχική οθόνη)
        print("Τι ενέργεια επιθυμείτε;")
        print("1) Καταχώρηση/Τροποποίηση/Διαγραφή")
        print("2) Γραφική Αναπαράσταση")
        print("3) Εξαγωγή δεδομένων σε αρχείο Excel")
        action = input("Επιλέξτε την ενέργεια (1/2/3) ή '4' για έξοδο: ")

        if not action.isdigit() or int(action) not in [1, 2, 3, 4]:
            print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
            continue

        action = int(action)

        if action == 4:
            break

        elif action == 1:
            # 2ο στάδιο: Επιλογή τύπου διαχείρισης συναλλαγής
            while True:
                print("1) Καταχώρηση\n2) Τροποποίηση\n3) Διαγραφή")
                sub_action = input(
                    "Επιλέξτε την ενέργεια (1/2/3) ή '4' για επιστροφή: "
                )

                if not sub_action.isdigit() or int(sub_action) not in [1, 2, 3, 4]:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
                    continue

                sub_action = int(sub_action)

                if sub_action == 4:
                    break

                # Επιλογή ΚΑΤΑΧΩΡΗΣΗΣ
                elif sub_action == 1:
                    transaction.create_transaction()

                # Επιλογή ΤΡΟΠΟΠΟΙΗΣΗΣ
                elif sub_action == 2:
                    transaction.update_transaction()

                # Επιλογή ΔΙΑΓΡΑΦΗΣ
                elif sub_action == 3:
                    transaction.delete_transaction()

                else:
                    print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")

        elif action == 2:
            # Λήψη ημερομηνιών από τον χρήστη
            start_date = input("Εισάγετε την ημερομηνία έναρξης σε μορφή dd-mm-yyyy: ")
            end_date = input("Εισάγετε την ημερομηνία λήξης σε μορφή dd-mm-yyyy: ")
            
            try:
                start_date_converted = datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                end_date_converted = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError:
                print("Μη έγκυρη ημερομηνία, παρακαλώ προσπαθήστε ξανά.")
                continue

            print("1) 3 Κορυφαίες 2Κατηγορίες Εξόδων (Bar Chart)\n2) Ποσοστά Εξόδων ανά Κατηγορία (Pie Chart)\n3) Αναλυτική Συναλλαγών(Linear Chart)")
            
            chart_action = input("Επιλέξτε τον τύπο γραφήματος (1/2/3): ")

            if chart_action == "1":
                top_expenses_bar_chart(start_date_converted, end_date_converted)
            elif chart_action == "2":
                category_expense_pie_chart(start_date_converted, end_date_converted)
            elif chart_action == "3":
                trans_analysis_line_chart(start_date_converted, end_date_converted)
            else:
                print("Μη έγκυρη επιλογή.")

        elif action == 3:
            # Υλοποίηση για εξαγωγή δεδομένων
            print("Η λειτουργία αυτή δεν έχει υλοποιηθεί ακόμη.")

    close_connection(connection)


if __name__ == "__main__":
    main()
