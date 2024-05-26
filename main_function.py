from class_transactions import *
from db_functions import *
from charts import top_expenses_bar_chart


def main():
    setup_database()
    #Σύνδεση με την βάση δεδομένων
    connection=open_connection()
    #Δημιουργία ενός αντικειμένου transaction της κλάσης Transactions το οποίο αλληλεπιδρά με την βάση δεδομένων
    transaction=Transactions(connection)
    #Κλήση της load_monthly για φόρτωμα των συναλλαγών και ενημέρωση των μηνιαίων 
    transaction.load_monthly()
    
    while True:
        #1ο στάδιο επιλογής ενέργειας (αρχική οθόνη)
        print("Τι ενέργεια επιθυμείτε;")
        print("1)Καταχώρηση/Τροποποίηση/Διαγραφή \n2)Γραφική Αναπαράσταση \n3)Εξαγωγή δεδομένων σε αρχείο Excel")
        action=int(input("Επιλέξτε την ενέργεια (1/2/3) ή '4' για έξοδο: "))
        
        if action==4:
            break
        
        elif action==1:
            #2ο στάδιο: Επιλογή τύπου διαχείριση συναλλαγής
            while True:
                print("1)Καταχώρηση \n2)Τροποποίηση \n3)Διαγραφή")
                sub_action=int(input("Επιλέξτε την ενέργεια (1/2/3) ή 4 για επιστροφή: "))
                
                if sub_action==4:
                    break
               
                
                #Επιλογή ΚΑΤΑΧΩΡΗΣΗΣ
                elif sub_action==1:
                    transaction.create_transaction()
                            
                
                #Επιλογή ΤΡΟΠΟΠΟΙΗΣΗΣ
                elif sub_action==2:
                    transaction.update_transaction()
                            
                
                #Επιλογή ΔΙΑΓΡΑΦΗΣ            
                elif sub_action==3:
                    transaction.delete_transaction()
                        
                else:
                    print("Μη έγκυρη επιλογή,παρακαλώ προσπαθήστε ξανά.")
                    
   
        #Επιλογή ΓΡΑΦΙΚΗΣ ΑΝΑΠΑΡΑΣΤΑΣΗΣ            
        elif action==2:
            #Λήψη ημερομηνιών από τον χρήστη
            start_date=input("Εισάγετε την ημερομηνία έναρξης σε μορφή YYYY-MM: ")
            end_date=input("Εισάγετε την ημερομηνία λήξης σε μορφή YYYY-MM: ")
            
            #Εμφάνιση του ραβδογράμματος στο επιλεγμένο διάστημα          
            top_expenses_bar_chart(start_date, end_date)           
        
        else:
            print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")             
                
    """   #Επιλογή EXCEL      
        elif action==3:  """
    
    
    close_connection(connection)  

if __name__ == "__main__":
    main()