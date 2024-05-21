import datetime
import calendar
from class_transactions import *
from db_functions import *
from defensive_mechanisms import *


def main():
    connection=open_connection()
    transaction=Transactions(connection)
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
                    #3o στάδιο: Επιλογή ΕΣΟΔΟΥ/ΕΞΟΔΟΥ
                    #Αυτό το στάδιο ίσως αφαιρεθεί καθώς υπάρχει στην μέθοδο create_transaction η εντολή self.type που προσδίδει το συγκεκριμένο χαρακτηριστικό
                    #Ωστόσο θα μπορούσε να προστεθεί αυτό του κουμπί εξτρά για το "φαίνεσθαι"
                    while True:
                        print("1)Έσοδο \n2)Έξοδο ")
                        trans_type=int(input("Επιλέξτε την κατηγορία (1/2) ή 3 για επιστροφή: "))
                        
                        if trans_type==3:
                            break
                        
                        else:
                            transaction.create_transaction()
                            
                
                #Επιλογή ΤΡΟΠΟΠΟΙΗΣΗΣ
                elif sub_action==2:
                    #3o στάδιο: Επιλογή ΕΣΟΔΟΥ/ΕΞΟΔΟΥ
                    while True:
                        print("1)Έσοδο \n2)Έξοδο ")
                        trans_type=int(input("Επιλέξτε την κατηγορία (1/2) ή 3 για επιστροφή: "))
                        
                        if trans_type==3:
                            break
                                        
                        else:
                            transaction.update_transaction()
                            
                
                #Επιλογή ΔΙΑΓΡΑΦΗΣ            
                elif sub_action==3:
                    #3o στάδιο: Επιλογή ΕΣΟΔΟΥ/ΕΞΟΔΟΥ
                    while True:
                        print("1)Έσοδο \n2)Έξοδο ")
                        trans_type=int(input("Επιλέξτε την κατηγορία (1/2) ή 3 για επιστροφή: "))
                        
                        if trans_type==3:
                            break
                                        
                        else:
                            transaction.delete_transaction()
                        
                else:
                    print("Μη έγκυρη επιλογή,παρακαλώ προσπαθήστε ξανά.")
                    
        else:
            print("Μη έγκυρη επιλογή, παρακαλώ προσπαθήστε ξανά.")
   
   
    """ #Επιλογή ΓΡΑΦΙΚΗΣ ΑΝΑΠΑΡΑΣΤΑΣΗΣ            
        elif action==2:                """
                    
                
    """ #Επιλογή EXCEL      
        elif action==3:   """

            
        
    
    
    
    
    close_connection(connection)  

