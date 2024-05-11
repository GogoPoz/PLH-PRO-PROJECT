class Income:
    def __init__(self, amount, description, monthly = False):
        """
        :param amount: float
        είναι το ποσό του εσόδου
        :param description:  str
        είναι η περιγραφή του εσόδου
        :param monthly: boolean
        είναι προεραιτικό όρισμα: αν ένα έσοδο είναι μηνιαίο
        """
        self.amount = amount
        self.description = description
        self.monthly = monthly

    def __str__(self):
        """
        Η μέθοδος επιστρέφει τα χαρακτηριστικά του αντικειμένου σε string
        Η εντολή if εκτελείται όταν το έσοδο είναι μηνιαίο
        """
        if self.monthly is True:
            return f"Ποσό: {self.amount}, Κατηγορία: {self.description}, είναι μηνιαίο έσοδο"
        else:
            return f"Ποσό: {self.amount}, Κατηγορία: {self.description}"
