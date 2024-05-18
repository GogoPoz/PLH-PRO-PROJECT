from db_functions import *
from defensive_mechanisms import *
from datetime import date


class Transactions:
    """
    type: integer θα παίρνει τιμές 1 και 2. 1 = έσοδο, 2 = έξοδο
    monthly: integer θα παίρνει τιμές 1 και 2. 1 = μηνιαίο, 2 = άλλο
    description: string Η ονομασία της συναλλαγής. Επιτρεπτοί χαρακτήρες γράμματα και αριθμοί
    insert_date: date Παίρνει αυτόματα την ημερομηνία εισαγωγής κάθε συναλλαγής
    """
    def __init__(self, connector):
        self.type = None
        self.monthly = None
        self.description = None
        self.amount = None
        self.insert_date = None
        self.connector = connector

    def load_transaction(self, description):
        """H μέθοδος ψάχνει συναλλαγή με το συγκεκριμένο description(όνομα) και την επιστρέφει αν αυτή υπάρχει"""
        results = query_fetch_all(self.connector,
                                  "SELECT * FROM transactions WHERE descr_of_trans='" + str(description) + "'")
        # αρχικοποίηση αντικειμένου εφόσον βρεθεί μέσα στη βάση δεδομένων
        if results:
            data = results[0]
            self.type = data["type_of_trans"]
            self.monthly = data["sub_type_of_trans"]
            self.description = data["descr_of_trans"]
            self.amount = data["amount"]
            self.insert_date = data["insert_date"]
            return self
        else:
            return None

    def create_transaction(self):
        """Η μέθοδος δημιουργεί μία καινούρια συναλλαγή και την αποθηκεύει στη βάση δεδομένων εφόσον δεν υπάρχει ήδη
        συναλλαγή με το ίδιο όνομα"""
        self.description = check_description("Εισάγετε το όνομα της συναλλαγής που θέλετε να καταχωρήσετε: ")
        # έλεγχος αν υπάρχει συναλλαγή με ίδιο όνομα
        results = self.load_transaction(self.description)
        # περίπτωση που υπάρχει ήδη πρέπει να επιλεχθεί άλλο όνομα
        if results:
            print("Η συναλλαγή υπάρχει ήδη. Παρακαλώ επιλέξτε άλλο όνομα.")
            return
        # αρχικοποίηση της συναλλαγής και αποθήκευση
        elif results is None:
            self.monthly = int(input("Πρόκειται για μηνιαία συναλλαγή;"))
            self.type = int(input("H συναλλαγή σας αφορά έσοδο η έξοδο;"))
            print(f"Τύπος συναλλαγής: {self.type}")
            self.amount = check_amount("Εισάγετε το ποσό της συναλλαγής: ")
            self.insert_date = date.today()
            query = f"""INSERT INTO transactions (type_of_trans, sub_type_of_trans, descr_of_trans, amount, insert_date)
                        VALUES ({self.type}, {self.monthly}, '{self.description}', {self.amount}, '{self.insert_date}')
                        """
            insert_data(self.connector, query)
            self.connector.commit()
            print("Η συναλλαγή σας αποθηκεύτηκε επιτυχώς.")

    def update_transaction(self):
        """H μέθοδος ψάχνει συναλλαγή με το συγκεκριμένο description(όνομα) και την τροποποιεί αν αυτή υπάρχει"""
        description = check_description("Εισάγετε το όνομα της συναλλαγής που θέλετε να τροποποιήσετε: ")
        results = self.load_transaction(description)
        # περίπτωση που δεν υπάρχει συναλλαγή με αυτό το όνομα
        if results is None:
            print(f"Δεν βρέθηκε συναλλαγή με όνομα {description}. Παρακαλώ δοκιμάστε ξανά.")
            return
        while True:
            if results:
                choice = int(input("Επιλέξτε το στοιχείο προς τροποποίηση ή έξοδο στην περίπτωση που δεν θέλετε "
                                   "να τροποποιήσετε κάτι:\n1)Ποσό\n2)Όνομα\n"
                                   "3)Πρόσθεση/αφαίρεση από τις μηνιαίες συναλλαγές\n4)Έξοδος\n"))
                # αλλαγή το ποσό
                if choice == 1:
                    new_amount = check_amount("Εισάγετε το νέο ποσό: ")
                    delete_or_update_data(self.connector, f"UPDATE transactions SET amount={new_amount} "
                                                          f"WHERE descr_of_trans='{self.description}'")
                    self.connector.commit()
                    print("Το ποσό άλλαξε επιτυχώς.")
                # αλλαγή το όνομα
                elif choice == 2:
                    new_description = check_description("Εισάγετε το νέο όνομα: ")
                    delete_or_update_data(self.connector, f"UPDATE transactions "
                                                          f"SET descr_of_trans='{new_description}' "
                                                          f"WHERE descr_of_trans='{self.description}'")
                    self.connector.commit()
                    print("Το όνομα άλλαξε επιτυχώς.")
                # προσθήκη/αφαίρεση από τις μηνιαίες συναλλαγές
                elif choice == 3:
                    # αν είναι μηνιαίο (1) τροποποιείται σε μη μηνιαίο (2)
                    if self.monthly == 1:
                        delete_or_update_data(self.connector, f"UPDATE transactions SET sub_type_of_trans=2 "
                                                              f"WHERE descr_of_trans='{self.description}'")
                        print("Αφαιρέθηκε από τις μηνιαίες συναλλαγές επιτυχώς.")
                        self.connector.commit()
                    # αν δεν είναι μηνιαίο (2) τροποποιείται σε μηνιαίο (1)
                    else:
                        delete_or_update_data(self.connector, f"UPDATE transactions SET sub_type_of_trans=1 "
                                                              f"WHERE descr_of_trans='{self.description}'")
                        print("Προστέθηκε στις μηνιαίες συναλλαγές επιτυχώς.")
                        self.connector.commit()
                else:
                    break

    def delete_transaction(self):
        """H μέθοδος ψάχνει συναλλαγή με το συγκεκριμένο description(όνομα) και την διαγράφει αν αυτή υπάρχει"""
        description = check_description("Εισάγετε το όνομα της συναλλαγής που θέλετε να διαγράψετε: ")
        results = self.load_transaction(description)
        # περίπτωση που δεν υπάρχει συναλλαγή με αυτό το όνομα
        if results is None:
            print(f"Δεν βρέθηκε συναλλαγή με όνομα {description}. Παρακαλώ δοκιμάστε ξανά.")
            return
        # διαγραφή συναλλαγής από την βάση δεδομένων
        else:
            query = f"DELETE FROM transactions WHERE descr_of_trans='{self.description}'"
            delete_or_update_data(self.connector, query)
            self.connector.commit()
            print("Η συναλλαγή διαγράφηκε επιτυχώς.")


def main():
    connector = open_connection()
    transaction = Transactions(connector)

    while True:
        choice = int(input("1-Δημιουργία εσόδου: \n2-Επεξεργασία εσόδου: \n3-Delete: \n4-EXIT: \n"))
        if choice == 1:
            transaction.create_transaction()
        elif choice == 2:
            transaction.update_transaction()
        elif choice == 3:
            transaction.delete_transaction()
        elif choice == 4:
            break

    close_connection(connector)


main()
