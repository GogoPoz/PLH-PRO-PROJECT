def check_description(message=None):
    """
    H συνάρτηση ελέγχει αν η ονομασία του εσόδου είναι έγκυρη(να μην είναι κενό string και να περιέχει μόνο γράμματα ή
    αριθμούς - όχι ειδικούς χαρακτήρες)
    """
    while True:
        # έλεγχος για σκέτο enter η input που περιέχει μόνο κενά
        description_input = input(message)
        if description_input.strip() == "":
            print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
            continue
        # περιορισμός να περιέχει μόνο γράμματα και αριθμούς
        elif not description_input.isalnum():
            print("Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
            continue
        return description_input


def check_amount(message=None):
    """
    Η συνάρτηση παίρνει ένα ποσό από το input, ελέγχει αν αυτό το ποσό είναι int η float και αν είναι το επιστρέφει
    Το όρισμα message είναι None ώστε όταν καλείται η check_amount να παίρνει όρισμα το εκάστοτε μήνυμα που
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
                print("Παρακαλώ εισάγετε ένα ποσό μεγαλύτερο του μηδενός.")
                continue
        else:  # όταν εισάγεται οτιδήποτε άλλο εκτός float η int
            print("Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
            continue
    return amount_input
