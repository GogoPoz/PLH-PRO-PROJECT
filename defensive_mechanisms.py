import datetime
import calendar


def check_description(description):
    """ H συνάρτηση ελέγχει αν το description που εισάγεται είναι έγκυρο(να μην είναι κενό string και να περιέχει μόνο
    γράμματα ή αριθμούς - όχι ειδικούς χαρακτήρες)"""
    # έλεγχος για σκέτο enter η input που περιέχει μόνο κενά
    if description.strip() == "":
        # Μήνυμα λάθους 0: "Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά"
        return 0
    # περιορισμός να περιέχει μόνο γράμματα και αριθμούς
    elif not description.isalnum():
        # Μήνυμα λάθους 2: "Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς."
        return 2
    # Περίπτωση που το description είναι σωστό
    return 1


def check_amount(amount):
    """ Η συνάρτηση παίρνει ένα ποσό (amount) και ελέγχει αν αυτό το ποσό είναι int η float. Αν είναι γίνεται έλεγχος
     να είναι μεγαλύτερο του 0. Αν εισαχθεί οτιδήποτε άλλο πέρα από αριθμούς δε γίνεται αποδεκτό"""
    # Έλεγχος αν το ποσό που εισάχθηκε είναι int η float μεγαλύτερα του μηδενός
    if amount.replace('.', '', 1).isdigit():
        # όταν εισάγεται 0 η αρνητικός αριθμός
        if amount <= 0:
            # Μήνυμα λάθους 0: "Παρακαλώ εισάγετε ένα ποσό μεγαλύτερο του μηδενός."
            return 0
    else:  # όταν εισάγεται οτιδήποτε άλλο εκτός float η int
        # Μήνυμα λάθους 2: "Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά"
        return 2
    # Περίπτωση που το amount είναι σωστό
    return 1



def add_one_month(orig_date):
    new_year = orig_date.year
    # προσθέτει έναν μήνα στην αρχική ημερομηνία
    new_month = orig_date.month + 1
    # περίπτωση που αυτός ο μήνας είναι ο Δεκέμβριος ώστε να αλλάξει η χρονιά
    if new_month > 12:
        new_year += 1
        new_month -= 12

    # αποθηκεύει την τελευταία ημέρα του καινούριου μήνα ώστε να γίνει η κατάλληλη αλλαγή (περίπτωση που η αρχική ημέρα
    # βρίσκεται στο τέλος του μήνα πχ 31)
    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)
