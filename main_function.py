from class_transactions import *
from db_functions import *
from charts import *
from excel_projection import export_to_excel

def main():
    connection = open_connection()  # Έναρξη σύνδεσης με την βάση δεδομένων
    transaction = Transactions(connection)  # Δημιουργία αντικειμένου
    transaction.load_monthly()  # Ενημέρωση των παλιών μηνιαίων καταχωρήσεων

    while True:
        # Στάδιο επιλογής ενέργειας (αρχική οθόνη)
        print(
            "Τι ενέργεια επιθυμείτε;\n 1) Καταχώρηση/Τροποποίηση/Διαγραφή\n 2) Γραφική Αναπαράσταση\n 3) Εξαγωγή δεδομένων σε αρχείο Excel"
        )
        action = input("Επιλέξτε την ενέργεια (1/2/3) ή '4' για έξοδο: ")

        if not action.isdigit() or int(action) not in [1, 2, 3, 4]:  # Έλεγχος εισόδου
            print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
            continue

        action = int(action)

        if action == 4:
            break

        elif action == 1:
            # Επόμενο στάδιο: Επιλογή τύπου διαχείρισης συναλλαγής
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
            # Επόμενο στάδιο: Επιλογή κατηγορίας συναλλαγών
            print(
                "Επιλέξτε την κατηγορία συναλλαγών:\n 1) Τρόφιμα\n 2) Λογαριασμοί\n 3) Έκτακτα Εισοδήματα\n 4) Όλες"
            )
            category_action = input(
                "Επιλέξτε την κατηγορία (1/2/3/4) ή '5' για επιστροφή: "
            )

            categories = {
                "1": "Τρόφιμα",
                "2": "Λογαριασμοί",
                "3": "Έκτακτα Εισοδήματα",
                "4": "Όλες",
            }  # Δημιουργία λεξικού

            if not category_action.isdigit() or category_action not in categories:
                print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
                continue

            category = categories[category_action]

            if category_action == 5:
                break

            else:
                # Λήψη ημερομηνιών από τον χρήστη και έλεγχος της εγκυρότητάς της (σε 2 λούπες)
                while True:
                    start_date = input("Εισάγετε την ημερομηνία έναρξης σε μορφή dd-mm-yyyy: ")
                    if not date_valid(start_date):
                        print("Μη έγκυρη μορφή ημερομηνίας, παρακαλώ προσπαθήστε ξανά.")
                        continue
                    break

                while True:
                    end_date = input("Εισάγετε την ημερομηνία λήξης σε μορφή dd-mm-yyyy: ")
                    if not date_valid(end_date):
                        print("Μη έγκυρη μορφή ημερομηνίας, παρακαλώ προσπαθήστε ξανά.")
                        continue
                    break

                if category == "Όλες":
                    all_categories_stem_plot(start_date, end_date)  # Αναπαράσταση όλων των κατηγοριών συνδυαστικά
                else:
                    category_stem_plot(start_date, end_date, category)  # Αναπαράσταση της επιλεγμένης κατηγορίας

        elif action == 3:
            #Επιλογή αναπαράστασης δεδομένων σε αρχείο excel
            while True:
                year = input("Εισάγετε το έτος (π.χ. 2024): ")        
                month = input("Εισάγετε τον μήνα σε μορφή mm (π.χ. 01 για Ιανουάριο): ")

                if date_valid(f"01-{month}-{year}"):
                    break
                else:
                    print("Μη έγκυρο έτος ή μήνας. Παρακαλώ δοκιμάστε ξανά.")
                    
            export_to_excel(connection, year, month)


    close_connection(connection)  # Διακοπή σύνδεσης με την βάση


if __name__ == "__main__":
    main()
