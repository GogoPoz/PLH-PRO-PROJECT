from class_income import Income

class Incomes:
    def __init__(self):
        """
        H incomes είναι μία κενή λίστα που κρατάει όλα τα έσοδα
        """
        self.incomes = []

    def check_amount(self, message = None):
        """
        Η μέθοδος παίρνει ένα ποσό από το input, ελέγχει αν αυτο το ποσό είναι int η float και αν είναι το επιστρέφει
        Το όρισμα message είναι None ώστε όταν καλείται η check_amount να παιρνει όρισμα το εκάστοτε μήνυμα που
        θέλουμε να εμφανίσουμε
        """
        while True:
            amount_input = input(message)
            # Έλεγχος αν το ποσό που εισάχθηκε είναι int η float μεγαλύτερα του μηδενός
            if amount_input.replace('.', '', 1).isdigit():
                amount_input = float(amount_input)
                if amount_input > 0:
                    break
                else:  # όταν εισάγεται 0 η αρνητικός αριθμός
                    print("Παραkαλώ εισάγετε ένα ποσό μεγαλύτερο του μηδενός.")
                    continue
            else:  # όταν εισάγεται οτιδήποτε άλλο εκτός float η int
                print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                continue
        return amount_input

    def check_description(self, message = None):
        """
        H μέθοδος ελέγχει αν η ονομασια του εσόδου είναι έγκυρη(να μην είναι κενό string) και την επιστρέφει
        Το όρισμα message είναι None ώστε όταν καλείται η check_amount να παιρνει όρισμα το εκάστοτε μήνυμα που
        θέλουμε να εμφανίσουμε
        """
        while True:
            description_input = input(message)

            if description_input.strip() == "":
                print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                continue
            return description_input

    def create_income(self):
        """
        Η μέθοδος δημιουργει ένα αντικείμενο τύπου income και το επιστρέφει αφού το προσθέσει στην λίστα
        με τα συνολικά έσοδα
        """
        amount = self.check_amount("Εισάγετε το ποσό του εσόδου που θέλετε να καταχωρήσετε: ")
        description = self.check_description("Εισάγετε την ονομασία του εσόδου που θέλετε να καταχωρήσετε: ")
        print("Θέλετε να καταχωρήσετε το ποσό ως μηνιαίο;")
        monthly = int(input("Πληκτρολογείστε 1 για την καταχώρηση ως μηνιαίο η 2 για απλή καταχώρηση: "))
        if monthly == 1:
            new_income = Income(amount, description, monthly = True)
        elif monthly == 2:
            new_income = Income(amount, description)
        self.incomes += [new_income]
        print("Το έσοδο σας καταχωρήθηκε επιτυχώς")
        return new_income

    def edit_income(self, description):
        """
        Η μέθοδος εντοπίζει ένα έσοδο με βάση το όνομα του(descreption) και δίνει την δυνατότητα για επεξεργασία
        ενός η όλων των στοιχείων του.
        """
        found = False #μεταβλητή που δηλώνει ότι βρήκαμε το προς αναζήτηση στοιχείο
        while True:
            for income in self.incomes:
                if income.description == description:
                    found = True #βρέθηκε το στοιχείο
                    choice = int(input("Επιλέξτε το στοιχείο προς τροποποίηση:\n1)Ποσό\n2)Όνομα\n"
                                   "3)Πρόσθεση/αφαίρεση από τα μηνιαία έσοδα\n4)Όλα τα παραπάνω"))
                    if choice == 1:#αλλαγή μόνο ποσό
                        income.amount = self.check_amount("Εισάγετε το νέο ποσό: ")
                        print("Το ποσό άλλαξε επιτυχώς.")
                    elif choice == 2:#αλλαγή μόνο όνομα
                        income.description = self.check_description("Εισάγετε το νέο όνομα: ")
                        print("To όνομα άλλαξε επιτυχώς")
                    elif choice == 3:#αλλαγή μηνιαίου
                        if income.monthly == False:
                            income.monthly = True
                            print("To ποσό προστέθηκε στα μηνιαία έσοδα επιτυχώς.")
                        else:
                            income.monthly = False
                            print("To ποσό αφαιρέθηκε από τα μηνιαία έσοδα επιτυχώς.")
                    elif choice == 4:#αλλαγή όλων των στοιχείων
                        income.amount = self.check_amount("Εισάγετε το νέο ποσό: ")
                        print("Το ποσό άλλαξε επιτυχώς.")
                        income.description = self.check_description("Εισάγετε το νέο όνομα: ")
                        print("To όνομα άλλαξε επιτυχώς")
                        if income.monthly == False:
                            income.monthly = True
                            print("To ποσό προστέθηκε στα μηνιαία έσοδα επιτυχώς.")
                        else:
                            income.monthly = False
                            print("To ποσό αφαιρέθηκε από τα μηνιαία έσοδα επιτυχώς.")
            if found:
                break
            else:#περίπτωση λάθος ονόματος
                print(f"Δεν βρέθηκε έσοδο με όνομα '{description}'. Παρακαλώ δοκιμάστε ξανά.")
                description = input("Εισάγετε το όνομα του εσόδου προς τροποποίηση: ")
                continue

    def delete_income(self, description):
        """
        Η μέθοδος εντοπίζει ένα έσοδο με βάση το όνομα του(description) και το διαγράφει
        """
        for income in self.incomes:
            if income.description == description:
                self.incomes.remove(income)
        print("Το έσοδο διαγράφηκε επιτυχώς")

    def __str__(self):
        st = ""
        for income in self.incomes:
            st += "\n" + str(income)
        return st

def main():
    incomes = Incomes()

    while True:
        choice = int(input("1-Δημιουργία εσόδου: \n2-Επεξεργασία εσόδου: \n3-Διαγραφή εσόδου: \n"))
        if choice == 1:
            new_income = incomes.create_income()
            print("Έσοδα:" + str(incomes))
        elif choice == 2:
            description = input("2- Εισάγετε το όνομα του εσόδου προς τροποποίηση: ")
            incomes.edit_income(description)
            print("Έσοδα:" + str(incomes))
        elif choice == 3:
            description = input("3- Εισάγετε το όνομα του εσόδου προς διαγραφή: ")
            incomes.delete_income(description)
            print("Έσοδα:" + str(incomes))

main()
