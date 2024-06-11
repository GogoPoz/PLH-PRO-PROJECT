from db_functions import *
from defensive_mechanisms import *
from datetime import date
import calendar


class Transactions:
    """
    type: integer. Θα παίρνει τιμές 1 και 2. 1 = έσοδο, 2 = έξοδο
    monthly: integer. Θα παίρνει τιμές 1 και 2. 1 = μηνιαίο, 2 = άλλο
    category: string. Η κατηγορία της συναλλαγής πχ. Κατηγορία super market. Επιτρεπτοί χαρακτήρες γράμματα και αριθμοί
    description: string. Η ονομασία της συναλλαγής. Επιτρεπτοί χαρακτήρες γράμματα και αριθμοί
    amount: float. Το ποσό που αφορά τη συναλλαγή
    insert_date: date. Παίρνει αυτόματα την ημερομηνία εισαγωγής κάθε συναλλαγής
    total: float Κρατάει το συνολικό χρηματικό ποσό
    original_date: date. Παίρνει αυτόματα την ημερομηνία εισαγωγής κάθε συναλλαγής. Εξυπηρετεί τη σωστή ενημέρωση
    μηνιαίων συναλλαγών σε περίπτωση που αυτές βρίσκονται στο τέλος του μήνα (29/30/31).
    """

    def __init__(self, connector):
        self.type = None
        self.monthly = None
        self.category = None
        self.description = None
        self.amount = None
        self.insert_date = None
        self.total = None
        self.original_date = None
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
            self.category = data["category"]
            self.description = data["descr_of_trans"]
            self.amount = data["amount"]
            self.insert_date = data["insert_date"]
            return self
        else:
            return None

    def add_to_total(self, amount):
        """Η μέθοδος προσθέτει στα συνολικά χρήματα το ποσό που παίρνει σαν όρισμα"""
        results = query_fetch_all(self.connector, "SELECT * FROM total_amount")
        # Περίπτωση που υπάρχει ήδη ποσό μέσα στο total_amount
        if results:
            data = results[0]
            self.total = data["total"]
            self.total += amount
            delete_or_update_data(self.connector, f"UPDATE total_amount SET total={self.total}")
            self.connector.commit()
        # Περίπτωση που στο total_amount δεν υπάρχει ήδη κάποιο ποσό
        else:
            self.total = amount
            query = f"INSERT INTO total_amount (total) VALUES ({self.total})"
            insert_data(self.connector, query)
            self.connector.commit()

    def subtract_from_total(self, amount):
        """Η μέθοδος αφαιρεί από τα συνολικά χρήματα το ποσό που παίρνει σαν όρισμα"""
        results = query_fetch_all(self.connector, "SELECT * FROM total_amount")
        # Περίπτωση που υπάρχει ήδη ποσό μέσα στο total_amount
        if results:
            data = results[0]
            self.total = data["total"]
            self.total -= amount
            delete_or_update_data(self.connector, f"UPDATE total_amount SET total={self.total}")
            self.connector.commit()
        # Περίπτωση που στο total_amount δεν υπάρχει ήδη κάποιο ποσό
        else:
            self.total = -amount
            query = f"INSERT INTO total_amount (total) VALUES ({self.total})"
            insert_data(self.connector, query)
            self.connector.commit()

    def load_monthly(self):
        """Η μέθοδος παίρνει όλες τις συναλλαγές που έχουν χαρακτηριστεί ως μηνιαίες κάθε φορά που εκτελείται το
        πρόγραμμα. Συγκρίνει την ημερομηνία κάθε συναλλαγής με την τωρινή ημερομηνία και προσθέτει η αφαιρεί το ανάλογο
        ποσό, έπειτα ενημερώνει την ημερομηνία της συναλλαγής( θέτει τον μήνα και τον χρόνο στο τελευταίο Update που
        έγινε)."""
        results = query_fetch_all(self.connector, "SELECT * FROM transactions WHERE sub_type_of_trans=1")
        monthly_transactions = []
        if results:
            # αρχικοποίηση των μηνιαίων συναλλαγών και αποθήκευση στη λίστα
            for result in results:
                transaction = Transactions(self.connector)
                transaction.type = result["type_of_trans"]
                transaction.description = result["descr_of_trans"]
                transaction.amount = result["amount"]
                transaction.insert_date = result["insert_date"]
                transaction.original_date = result["original_date"]
                monthly_transactions.append(transaction)

        # Μεταβλητές που κρατάν όλα τα μηνιαία ποσά ώστε στο τέλος να προστεθούν/ αφαιρεθούν από το total_amount
        amount_to_add = 0
        amount_to_subtract = 0

        # ενημέρωση ημερομηνίας και συνολικού ποσού
        for transaction in monthly_transactions:
            old_date = transaction.insert_date
            today = date.today()
            # περίπτωση που η συναλλαγή αφορά έσοδο
            if transaction.type == 1:
                while (old_date.year < today.year) or (
                        old_date.year == today.year and old_date.month < today.month):
                    # περίπτωση που είναι η ημέρα συναλλαγής δεν έχει φτάσει ακόμα στον τρέχων μήνα
                    if old_date.month == today.month - 1 and old_date.day > today.day:
                        break
                    else:
                        old_date = add_one_month(old_date)
                        amount_to_add += transaction.amount
                        transaction.insert_date = old_date
                        print(transaction.insert_date)
            # περίπτωση που η συναλλαγή αφορά έξοδο
            elif transaction.type == 2:
                while (old_date.year < today.year) or (
                        old_date.year == today.year and old_date.month < today.month):
                    # περίπτωση που είναι η ημέρα συναλλαγής δεν έχει φτάσει ακόμα στον τρέχων μήνα
                    if old_date.month == today.month - 1 and old_date.day > today.day:
                        break
                    else:
                        old_date = add_one_month(old_date)
                        amount_to_subtract += transaction.amount
                        transaction.insert_date = old_date

            # ενημέρωση ημέρας σε περίπτωση που η ημερομηνίας της συναλλαγής βρίσκεται στο τέλος του μήνα
            original_day = transaction.original_date.day
            last_day_of_current_month = \
            calendar.monthrange(transaction.insert_date.year, transaction.insert_date.month)[1]
            """Περίπτωση που η ημέρα της αρχικής ημερομηνίας είναι μεγαλύτερη απο την τελευταία μέρα του 
            συγκεκριμένου μήνα, αποθηκεύεται η τελευταία μέρα του συγκεκριμένου μήνα στην insert_date"""
            if original_day > last_day_of_current_month:
                transaction.insert_date = transaction.insert_date.replace(day=last_day_of_current_month)
            # αλλιώς αν είναι μικρότερη η ίση αποθηκεύεται η μέρα της αρχικής ημερομηνίας στην insert_date
            elif original_day <= last_day_of_current_month:
                transaction.insert_date = transaction.insert_date.replace(day=original_day)
            delete_or_update_data(self.connector, f"UPDATE transactions SET "
                                                  f"insert_date='{transaction.insert_date}' "
                                                  f"WHERE descr_of_trans='{transaction.description}'")

            self.connector.commit()
        self.add_to_total(amount_to_add)
        self.subtract_from_total(amount_to_subtract)

    def create_transaction(self, category, description, monthly, type, amount):
        """Η μέθοδος δημιουργεί μία καινούρια συναλλαγή και την αποθηκεύει στη βάση δεδομένων εφόσον δεν υπάρχει ήδη
                συναλλαγή με το ίδιο όνομα"""
        self.category = category
        self.description = description
        self.monthly = monthly
        self.type = type
        self.amount = amount
        self.insert_date = date.today()
        self.original_date = date.today()

        query = (f"INSERT INTO transactions (type_of_trans, sub_type_of_trans, category, descr_of_trans, amount, "
                 f"insert_date, original_date) "
                 f"VALUES ({self.type}, {self.monthly}, '{self.category}', '{self.description}', {self.amount}, "
                 f"'{self.insert_date}', '{self.original_date}')")

        insert_data(self.connector, query)
        self.connector.commit()

        # αν είναι έσοδο προσθέτει το ποσό στα συνολικά χρήματα
        if self.type == 1:
            self.add_to_total(self.amount)
        # αν είναι έξοδο αφαιρεί το ποσό από τα συνολικά χρήματα
        elif self.type == 2:
            self.subtract_from_total(self.amount)
        print("Η συναλλαγή σας αποθηκεύτηκε επιτυχώς.")

    def update_amount(self, new_amount, old_amount, type, description):
        """Η μέθοδος αλλάζει το ποσό μιας συγκεκριμένης συναλλαγής. Συγκρίνει το καινούριο ποσό με το παλιό, με σκοπό
        να προστεθεί/ αφαιρεθεί η διαφορά από το συνολικό ποσό (χρησιμοποιώντας τις παραμέτρους new_amount και
        old_amount) ανάλογα με το αν η συναλλαγή αφορά έσοδο η έξοδο (παράμετρος type). Αλλάζει το ποσό στη βάση
        δεδομένων με βάση την παράμετρο description (ονομασία συναλλαγής)."""
        self.amount = old_amount
        self.description = description
        self.type = type
        if new_amount != self.amount:
            # αν πρόκειται για έσοδο
            if self.type == 1:
                # αν το καινούριο ποσό είναι μεγαλύτερο από το παλιό προσθέτει τη διαφορά στην total
                if new_amount > self.amount:
                    amount_to_add = new_amount - self.amount
                    self.amount = new_amount
                    self.add_to_total(amount_to_add)
                # αν το καινούριο ποσό είναι μικρότερο από το παλιό αφαιρεί τη διαφορά από την total
                elif new_amount < self.amount:
                    amount_to_subtract = self.amount - new_amount
                    self.amount = new_amount
                    self.subtract_from_total(amount_to_subtract)
            # αν πρόκειται για έξοδο
            elif self.type == 2:
                # αν το καινούριο ποσό είναι μεγαλύτερο από το παλιό αφαιρεί τη διαφορά από την total
                if new_amount > self.amount:
                    amount_to_subtract = new_amount - self.amount
                    self.amount = new_amount
                    self.subtract_from_total(amount_to_subtract)
                # αν το καινούριο ποσό είναι μικρότερο από το παλιό προσθέτει τη διαφορά στην total
                elif new_amount < self.amount:
                    amount_to_add = self.amount - new_amount
                    self.amount = new_amount
                    self.add_to_total(amount_to_add)
        delete_or_update_data(self.connector, f"UPDATE transactions SET amount={new_amount} "
                                              f"WHERE descr_of_trans='{self.description}'")

        self.connector.commit()
        print("Το ποσό άλλαξε επιτυχώς.")

    def update_description(self, old_description, new_description):
        """Η μέθοδος αλλάζει την ονομασία της συναλλαγής στη βάση δεδομένων στην τιμή της παραμέτρου new_description
        αναζητώντας τη συναλλαγή με το παλιό της όνομα (old_description)."""
        self.description = old_description
        delete_or_update_data(self.connector, f"UPDATE transactions "
                                              f"SET descr_of_trans='{new_description}' "
                                              f"WHERE descr_of_trans='{self.description}'")
        self.connector.commit()
        self.description = new_description
        print("Το όνομα άλλαξε επιτυχώς.")

    def update_category(self, old_category, new_category, description):
        """Η μέθοδος αλλάζει την κατηγορία της συναλλαγής στη βάση δεδομένων στην τιμή της παραμέτρου new_category
                αναζητώντας τη συναλλαγή με το όνομα της (description)."""
        self.category = old_category
        delete_or_update_data(self.connector, f"UPDATE transactions "
                                              f"SET category='{new_category}' "
                                              f"WHERE descr_of_trans='{description}'")
        self.connector.commit()
        self.category = new_category
        print("Η κατηγορία άλλαξε επιτυχώς.")

    def update_monthly(self, monthly):
        """Η μέθοδος παίρνει σαν παράμετρο τη monthly που έχει τιμές 1 για μηνιαία και 2 για μη μηνιαία. Εάν η συναλλαγή
        είναι μηνιαία την αλλάζει σε μη μηνιαία και αν είναι μη μηνιαία την αλλάζει σε μηνιαία αντίστοιχα."""
        self.monthly = monthly

        # αν είναι μηνιαίο (1) τροποποιείται σε μη μηνιαίο (2)
        if self.monthly == 1:
            delete_or_update_data(self.connector, f"UPDATE transactions SET sub_type_of_trans=2 "
                                                  f"WHERE descr_of_trans='{self.description}'")
            self.monthly = 2
            print("Αφαιρέθηκε από τις μηνιαίες συναλλαγές επιτυχώς.")
            self.connector.commit()
        # αν δεν είναι μηνιαίο (2) τροποποιείται σε μηνιαίο (1)
        elif self.monthly == 2:
            delete_or_update_data(self.connector, f"UPDATE transactions SET sub_type_of_trans=1 "
                                                  f"WHERE descr_of_trans='{self.description}'")
            self.monthly = 1
            print("Προστέθηκε στις μηνιαίες συναλλαγές επιτυχώς.")
            self.connector.commit()

    def delete_transaction(self, description, type, amount):
        """H μέθοδος ψάχνει συναλλαγή με το συγκεκριμένο description(όνομα) και τη διαγράφει. Ενημερώνει αντίστοιχα
        και το συνολικό χρηματικό ποσό με βάση αν είναι έσοδο ή έξοδο (type). Αν είναι έσοδο τότε αφαιρεί το ποσό
        (amount) της συναλλαγής προς διαγραφή από το συνολικό και αν είναι έξοδο το προσθέτει."""
        self.type = type
        self.amount = amount

        query = f"DELETE FROM transactions WHERE descr_of_trans='{description}'"
        delete_or_update_data(self.connector, query)

        # Περίπτωση που είναι έσοδο αφαιρείται το ποσό από το συνολικό χρηματικό ποσό.
        if self.type == 1:
            self.subtract_from_total(self.amount)
        # Περίπτωση που είναι έξοδο προστίθεται το ποσό στο συνολικό χρηματικό ποσό.
        elif self.type == 2:
            self.add_to_total(self.amount)
        self.connector.commit()
        print("Η συναλλαγή διαγράφηκε επιτυχώς.")

    def print_transactions(self):
        """Η μέθοδος τραβάει όλες τις συναλλαγές από τη βάση δεδομένων και τις τυπώνει"""
        results = query_fetch_all(self.connector, "SELECT * FROM transactions")
        print_transactions = []

        if results:
            # αρχικοποίηση των μηνιαίων συναλλαγών και αποθήκευση στη λίστα
            for result in results:
                transaction = Transactions(self.connector)
                transaction.type = result["type_of_trans"]
                transaction.monthly = result["sub_type_of_trans"]
                transaction.category = result["category"]
                transaction.description = result["descr_of_trans"]
                transaction.amount = result["amount"]
                transaction.insert_date = result["insert_date"]
                print_transactions.append(transaction)
        else:
            print("Δεν βρέθηκαν συναλλαγές.")

        for transaction in print_transactions:
            st = ""
            st += f"Κατηγορία: {transaction.category}, Όνομα συναλλαγής: {transaction.description}, Τύπος συναλλαγής: "
            # Έλεγχος αν είναι έσοδο/ έξοδο
            if transaction.type == 1:
                st += "Έσοδο, "
            elif transaction.type == 2:
                st += "Έξοδο, "
            # Έλεγχος αν είναι μηνιαίο/ άλλο
            st += "Μηνιαία συναλλαγή: "
            if transaction.monthly == 1:
                st += "Ναι, "
            elif transaction.monthly == 2:
                st += "Όχι, "
            st += f"Ποσό: {transaction.amount}, Ημερομηνία συναλλαγής: {transaction.insert_date}."
            print(st)

    def print_total(self):
        """Η μέθοδος εμφανίζει το συνολικό χρηματικό ποσό"""
        results = query_fetch_all(self.connector, "SELECT * FROM total_amount")
        # Περίπτωση που υπάρχει ποσό μέσα στο total_amount
        if results:
            transaction = Transactions(self.connector)
            transaction.total = results[0]["total"]
            print(f"Συνολικό ποσό: {transaction.total}")
        # Περίπτωση που δεν υπάρχει ποσό στο total_amount
        else:
            print("Δεν βρέθηκαν χρήματα στο συνολικό ποσό.")
