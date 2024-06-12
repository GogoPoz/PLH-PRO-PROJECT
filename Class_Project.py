
from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk
from class_transactions import *
from main_function import *
from db_functions import *
from defensive_mechanisms import *
from charts import category_stem_plot, all_categories_stem_plot



# Κυρία εφαρμογή
class Project(CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Financial Management")
        self.geometry("1100x520")
        setup_database()
        #Σύνδεση με την βάση δεδομένων
        connector=open_connection()
        #Δημιουργία ενός αντικειμένου transaction της κλάσης Transactions το οποίο αλληλεπιδρά με την βάση δεδομένων
        self.transaction=Transactions(connector)
        self.transaction.load_monthly()
        main_text = (
            "Γειά σου!\n"
            "Καλωσήρθες στο Project-Financial Management App. "
            "To PFM App είναι μια εφαρμογή διαχείρησης των οικονομικών εσόδων και εξόδων ενός ανθρώπου. Εδώ μπορείς να καταχωρήσεις/ τροποποιήσεις/ διαγράψεις οικονομικές πράξεις. Να τις διαχωρίσεις σε έσοδα και έξοδα καθώς και να τις χαρακτηρίσεις μηνιαίες. Με την εφαρμογή αυτή μπορείς επίσης να δεις γραφικές παραστάσεις από τα έσοδα-έξοδά σου, αλλά και να τα εξάγεις σε αρχείο Excel.\n"
            "Πάτησε το κουμπί 'NEXT' για να προχωρήσεις."
        )

        # Widgets για main page
        self.label1= CTkLabel(self, text=main_text, font=("Arial", 30), wraplength=750, justify="center", fg_color="black")
        self.btn1= CTkButton(self, text="Επόμενο", font=("Arial", 30), command=self.show_page1)

        # Φόρτωση εικόνων
        self.image1 = ImageTk.PhotoImage(Image.open("icons/Input_icon.png").resize((130, 100)))
        self.image2 = ImageTk.PhotoImage(Image.open("icons/Edit_icon.png").resize((130, 100)))
        self.image3 = ImageTk.PhotoImage(Image.open("icons/Delete_icon.png").resize((130, 100)))
        self.image4 = ImageTk.PhotoImage(Image.open("icons/graph_icon.png").resize((130, 100)))
        self.image5 = ImageTk.PhotoImage(Image.open("icons/excel_icon.png").resize((130, 100)))

        # Widgets για page1
        text2= "Παρακαλώ πάτα το αντίστοιχο εικονίδιο με την λειτουργία που θες να εκτελέσεις."
        self.label2= CTkLabel(self, text=text2, font=("Arial", 30))
        self.radio_var3= IntVar(value=0)
        self.btn_radio5= CTkButton(self, text="Καταχώρηση", compound="top", font=("Arial", 30),image=self.image1, command=lambda: self.update_radio_buttons2_and_var(1))
        self.btn_radio6= CTkButton(self, text="Επεξεργασία",compound="top", font=("Arial", 30),image=self.image2, command=lambda: self.update_radio_buttons2_and_var(2))
        self.btn_radio7= CTkButton(self, text="Διαγραφή",compound="top", font=("Arial", 30),image=self.image3, command=lambda:  self.update_radio_buttons2_and_var(3))
        self.btn_radio8= CTkButton(self, text="Γραφική\n Παράσταση",compound="top", font=("Arial", 30),image=self.image4, command=lambda:  self.update_radio_buttons2_and_var(4))
        self.btn_radio9= CTkButton(self, text="Αρχείο Excel",compound="top", font=("Arial", 30),image=self.image5, command=lambda:  self.update_radio_buttons2_and_var(5))
        self.btn5= CTkButton(self, text="Αρχική", font=("Arial", 30), command=self.main_page)
        self.btn6a= CTkButton(self, text="Επόμενο", font=("Arial", 30),command=self.epomeno1)
        self.btn6b= CTkButton(self, text="Επόμενο", font=("Arial", 30),command=self.epomeno2)
        self.btn6c= CTkButton(self, text="Επόμενο", font=("Arial", 30), command=self.epomeno3)
        self.btn6d= CTkButton(self, text="Επόμενο", font=("Arial", 30), command=self.epomeno4)
        self.btn6b.configure(state=DISABLED)


        # Widgets για page2
        text3= "Κατηγορία Συναλλαγής"
        self.label3= CTkLabel(self, text=text3, font=("Arial", 30))
        self.entry1= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry1.insert(0, "Πληκτρολογήστε εδώ...")
        text4= "Όνομα Συναλλαγής"
        self.label4= CTkLabel(self, text=text4, font=("Arial", 30))
        self.entry2= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry2.insert(0, "Πληκτρολογήστε εδώ...")
        self.label8=CTkLabel(self,text=" ",font=("Arial", 30))
        
        # Αρχικά απενεργοποίηση του κουμπιού "Επόμενο" στη σελίδα 2
        self.btn6c.configure(state=DISABLED)


        # Widgets για page3
        text5= "Πρόκειται για μηνιαία συναλλαγή;"
        self.label5= CTkLabel(self, text=text5, font=("Arial", 30))
        self.radio_var1= IntVar(value=0)
        self.btn_radio1= CTkButton(self, text="Ναι", font=("Arial", 30), command=lambda: self.set_radio_var(self.radio_var1, 1))
        self.btn_radio2= CTkButton(self, text="Όχι", font=("Arial", 30), command=lambda: self.set_radio_var(self.radio_var1, 2))
        text6= "Η συναλλαγή σας αφορά:"
        self.label6= CTkLabel(self, text=text6, font=("Arial", 30))
        self.radio_var2= IntVar(value=0)
        self.btn_radio3= CTkButton(self, text="Έσοδα", font=("Arial", 30), command=lambda: self.set_radio_var(self.radio_var2, 1))
        self.btn_radio4= CTkButton(self, text="Έξοδα", font=("Arial", 30), command=lambda: self.set_radio_var(self.radio_var2, 2))
        self.btn6d.configure(state=DISABLED)
        self.btn9=CTkButton(self,text="OK", font=("Arial", 30),command=self.call_transactions)

        for i in range(0,4):
            self.grid_columnconfigure(i,weight=1)
            self.grid_rowconfigure(i,weight=1)

        self.main_page()

    


        #widgets για page2b
        self.radio_var4= IntVar(value=0)
        self.btn_radio10= CTkButton(self, text="Ποσό", compound="top", font=("Arial", 30),command=lambda: self.update_radio_buttons3_and_var4(1))
        self.btn_radio11= CTkButton(self, text="Όνομα",compound="top", font=("Arial", 30), command=lambda: self.update_radio_buttons3_and_var4(2))
        self.btn_radio12= CTkButton(self, text="Κατηγορία",compound="top", font=("Arial", 30),command=lambda:  self.update_radio_buttons3_and_var4(3))
        self.btn_radio13= CTkButton(self, text="Προσθήκη/ Αφαίρεση",compound="top", font=("Arial", 30),command=lambda:  self.update_radio_buttons3_and_var4(4))

        #widgets για page3a
        self.label9= CTkLabel(self, text=text3, font=("Arial", 30))
        self.entry3= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry3.insert(0, "Πληκτρολογήστε εδώ...")
        self.btn6d.configure(state=NORMAL)

        #widgets για page4
        self.label7=CTkLabel(self,text="Επιλέξτε την κατηγορία συναλλαγών:", font=("Arial", 30))
        self.radio_var5= IntVar(value=0)
        self.btn_radio14= CTkButton(self, text="Τρόφιμα", compound="top", font=("Arial", 30),command=lambda: self.update_radio_buttons3_and_var5(1))
        self.btn_radio15= CTkButton(self, text="Λογαριασμοί",compound="top", font=("Arial", 30), command=lambda: self.update_radio_buttons3_and_var5(2))
        self.btn_radio16= CTkButton(self, text="Έκτακτα Επιδόματα",compound="top", font=("Arial", 30),command=lambda:  self.update_radio_buttons3_and_var5(3))
        self.btn_radio17= CTkButton(self, text="Όλες",compound="top", font=("Arial", 30),command=lambda:  self.update_radio_buttons3_and_var5(4))

        #widgets για page5
        text11= "Εισάγετε το έτος (π.χ. 2024):  "
        self.label11= CTkLabel(self, text=text11, font=("Arial", 30))
        self.entry4= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry4.insert(0, "Πληκτρολογήστε εδώ...")
        text10= "Εισάγετε τον μήνα σε μορφή mm (π.χ. 01 για Ιανουάριο):"
        self.label10= CTkLabel(self, text=text10, font=("Arial", 30))
        self.entry5= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry5.insert(0, "Πληκτρολογήστε εδώ...")
        self.label12=CTkLabel(self,text=" ",font=("Arial", 30))

        #widgets για page6
        text13= "Εισάγετε την ημερομηνία έναρξης σε μορφή dd-mm-yyyy: "
        self.label13= CTkLabel(self, text=text13, font=("Arial", 30))
        self.entry6= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry6.insert(0, "Πληκτρολογήστε εδώ...")
        text14= "Εισάγετε την ημερομηνία λήξης σε μορφή dd-mm-yyyy: "
        self.label14= CTkLabel(self, text=text14, font=("Arial", 30))
        self.entry7= CTkEntry(self, width=1, font=("Arial", 30))
        self.entry7.insert(0, "Πληκτρολογήστε εδώ...")
        self.label15=CTkLabel(self,text=" ",font=("Arial", 30))

        

    #Μορφοποίηση σελίδων
    def main_page(self):
        self.clear_page()
        self.label1.pack(fill='both', expand=True)
        self.btn6a.pack(side="right")

        # Επαναφορά των επιλογών γα κάθε κουμπί
        self.radio_var3.set(0)
        self.update_radio_buttons2(self.btn_radio5, self.btn_radio6, self.btn_radio7, self.btn_radio8, self.btn_radio9, 0)
        self.btn6b.configure(state=DISABLED)
        self.entry1.delete(0, END)
        self.entry1.insert(0, "Πληκτρολογήστε εδώ...")
        self.entry2.delete(0, END)
        self.entry2.insert(0, "Πληκτρολογήστε εδώ...")
        self.btn6c.configure(state=DISABLED)
        self.radio_var1.set(0)
        self.radio_var2.set(0)
        self.update_radio_buttons(self.btn_radio1, self.btn_radio2, 0)
        self.update_radio_buttons(self.btn_radio3, self.btn_radio4, 0)
        self.btn6d.configure(state=DISABLED)

    def show_page1(self):

        # Αφαίρεση widgets αρχικής σελίδας
        self.clear_page()
        # Εμφάνιση page1
        self.label2.grid(row=0, column=0, columnspan=5, rowspan=2)
        self.btn_radio5.grid(row=1, column=0, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio6.grid(row=1, column=1, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio7.grid(row=1, column=2, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio8.grid(row=1, column=3, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio9.grid(row=1, column=4, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn5.grid(row=4, column=0, padx=10, pady=10, sticky='sw')
        self.btn6b.grid(row=4, column=4, padx=10, pady=10, sticky='se')

    def show_page2(self):
        self.clear_page()
        page=self.radio_var3.get()
        # Τοποθέτηση Widgets
        if page==1:
            self.label3.grid(row=1, column=0, columnspan=4, sticky='ew')
            self.entry1.grid(row=2, column=0, columnspan=4, sticky='ew')
            self.label4.grid(row=3, column=0, columnspan=4, sticky='ew')
            self.entry2.grid(row=4, column=0, columnspan=4, sticky='ew')
            self.btn5.grid(row=5, column=0, padx=10, pady=10, sticky='sw')
            self.btn6c.grid(row=5, column=3, padx=10, pady=10, sticky='se')
        elif page==2:
            self.label3.grid(row=1, column=0, columnspan=4, sticky='ew')
            self.entry1.grid(row=2, column=0, columnspan=4, sticky='ew')
            self.label4.grid(row=3, column=0, columnspan=4, sticky='ew')
            self.entry2.grid(row=4, column=0, columnspan=4, sticky='ew')
            self.btn5.grid(row=5, column=0, padx=10, pady=10, sticky='sw')
            self.btn6c.grid(row=5, column=3, padx=10, pady=10, sticky='se')
            self.btn6c.configure(command=self.epomeno3)
        else:
            self.label4.grid(row=1, column=0, columnspan=4, sticky='ew')
            self.entry2.grid(row=2, column=0, columnspan=4, sticky='ew')
            self.btn5.grid(row=5, column=0, padx=10, pady=10, sticky='sw')
            self.btn6c.grid(row=5, column=3, padx=10, pady=10, sticky='se')
        self.label8.grid(row=0, column=0, columnspan=4, sticky='ew')


        self.entry1.bind("<FocusIn>", self.on_entry_click)
        self.entry1.bind("<FocusOut>", self.on_focus_out)
        self.entry2.bind("<FocusIn>", self.on_entry_click)
        self.entry2.bind("<FocusOut>", self.on_focus_out)
        self.entry1.bind("<KeyRelease>", self.check_entries)
        self.entry2.bind("<KeyRelease>", self.check_entries)




    def show_page2a(self):
        self.clear_page()
        self.label3.grid(row=0, column=0, columnspan=4, sticky='ew')
        self.entry1.grid(row=1, column=0, columnspan=4, sticky='ew')

        self.entry1.bind("<KeyRelease>", self.check_entries)
        self.entry1.bind("<FocusIn>", self.on_entry_click)
        self.entry1.bind("<FocusOut>", self.on_focus_out)

    def show_page2b(self):
        self.clear_page()
        self.label2.grid(row=0, column=0, columnspan=5, rowspan=2)
        self.btn_radio10.grid(row=1, column=0, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio11.grid(row=1, column=1, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio12.grid(row=1, column=2, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio13.grid(row=1, column=3, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn5.grid(row=4, column=0, padx=10, pady=10, sticky='sw')
        self.btn6b.grid(row=4, column=4, padx=10, pady=10, sticky='se')
        self.btn6b.configure(command=self.show_page3a)
        

    def show_page3(self):
        self.clear_page()


        # Επαναφορά των ραδιοκουμπιών στην αρχική κατάσταση
        self.radio_var1.set(0)
        self.radio_var2.set(0)
        self.update_radio_buttons(self.btn_radio1, self.btn_radio2, 0)
        self.update_radio_buttons(self.btn_radio3, self.btn_radio4, 0)

        # Τοποθέτηση Widgets
        self.label5.grid(row=0, column=0, columnspan=5, sticky='ew')
        self.btn_radio1.grid(row=1, column=0,columnspan=1, sticky='e')
        self.btn_radio2.grid(row=1, column=3,columnspan=1, sticky='w')
        self.label6.grid(row=2, column=0, columnspan=5, sticky='ew')
        self.btn_radio3.grid(row=3, column=0,columnspan=1, sticky='e')
        self.btn_radio4.grid(row=3, column=3,columnspan=1, sticky='w')
        self.btn5.grid(row=4, column=0, padx=10, pady=10, sticky='sw')
        self.btn6d.grid(row=4, column=3, padx=10, pady=10, sticky='se')
        self.btn9.grid(row=4, column=3, padx=10, pady=10, sticky='sw')

    def show_page4(self):
        self.clear_page()
        self.label7.grid(row=0, column=0, columnspan=5, rowspan=2)
        self.btn_radio14.grid(row=1, column=0, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio15.grid(row=1, column=1, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio16.grid(row=1, column=2, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn_radio17.grid(row=1, column=3, rowspan=3, columnspan=1, padx=10, pady=10)
        self.btn5.grid(row=4, column=0, padx=10, pady=10, sticky='sw')
        self.btn6b.grid(row=4, column=4, padx=10, pady=10, sticky='se')
        self.btn6b.configure(command=self.show_page5)
    
    def show_page5(self):
        self.clear_page()
        self.category5=self.radio_var5.get()
        self.label13.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.entry6.grid(row=2, column=0, columnspan=4, sticky='ew')
        self.label14.grid(row=3, column=0, columnspan=4, sticky='ew')
        self.entry7.grid(row=4, column=0, columnspan=4, sticky='ew')
        self.btn5.grid(row=5, column=0, padx=10, pady=10, sticky='sw')
        self.btn6c.grid(row=5, column=3, padx=10, pady=10, sticky='se')
        self.btn6c.configure(command=self.epomeno5)
        self.label15.grid(row=0, column=0, columnspan=4, sticky='ew')
        if self.entry4.get()!=" " and self.entry5.get()!=" ":
            self.btn6c.configure(state=NORMAL)

        self.entry4.bind("<FocusIn>", self.on_entry_click)
        self.entry5.bind("<FocusOut>", self.on_focus_out)
        self.entry5.bind("<FocusIn>", self.on_entry_click)
        self.entry5.bind("<FocusOut>", self.on_focus_out)
        self.entry4.bind("<KeyRelease>", self.check_entries)
        self.entry5.bind("<KeyRelease>", self.check_entries)




    def show_page3a(self):
        self.clear_page()
        choice=self.radio_var4.get()
        self.label9.grid(row=0, column=0, columnspan=4, sticky='ew')
        self.entry3.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.btn5.grid(row=4, column=0, padx=10, pady=10, sticky='sw')
        self.btn9.grid(row=4, column=3, padx=10, pady=10, sticky='sw')
        self.btn6d.grid(row=4, column=3, padx=10, pady=10, sticky='se')
        self.label9.configure(text=" ")
        self.entry3.bind("<FocusIn>", self.on_entry_click)
        self.entry3.bind("<FocusOut>", self.on_focus_out)
        self.entry3.bind("<FocusOut>", self.on_focus_out)
        self.btn9.configure(state=NORMAL)


        if choice==1:
            self.label9.configure(text="Εισάγετε το νέο ποσό.\n Πατήστε επόμενο και έπειτα ΟΚ.")
            
        elif choice==2:
            self.label9.configure(text="Εισάγετε το νέο όνομα.\n Πατήστε επόμενο και έπειτα ΟΚ.")
            
        elif choice==3:
            self.label9.configure(text="Εισάγετε τη νέα κατηγορία.\n Πατήστε επόμενο και έπειτα ΟΚ.")
            
        elif choice==4:
            self.entry3.configure(state=DISABLED)
            self.label9.configure(text="Πατήστε επόμενο και έπειτα ΟΚ.")
            self.btn9.configure(command=self.call_transactions)


    def show_page6(self):
        self.clear_page()
        self.label11.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.entry6.grid(row=2, column=0, columnspan=4, sticky='ew')
        self.label10.grid(row=3, column=0, columnspan=4, sticky='ew')
        self.entry7.grid(row=4, column=0, columnspan=4, sticky='ew')
        self.btn5.grid(row=5, column=0, padx=10, pady=10, sticky='sw')
        self.btn6c.grid(row=5, column=3, padx=10, pady=10, sticky='se')
        self.btn6c.configure(command=self.epomeno5)
        self.label12.grid(row=0, column=0, columnspan=4, sticky='ew')
        if self.entry4.get()!=" " and self.entry5.get()!=" ":
            self.btn6c.configure(state=NORMAL)


        self.entry6.bind("<FocusIn>", self.on_entry_click)
        self.entry7.bind("<FocusOut>", self.on_focus_out)
        self.entry7.bind("<FocusIn>", self.on_entry_click)
        self.entry7.bind("<FocusOut>", self.on_focus_out)
        self.entry6.bind("<KeyRelease>", self.check_entries)
        self.entry7.bind("<KeyRelease>", self.check_entries)


        
        

    def money_input(self):
        money_dialog = CTkInputDialog(text="Πληκτρολογήστε το ποσό...", title="Ποσό σε €")
        amount = money_dialog.get_input()
        print("CTkInputDialog:", amount)  # Για επαλήθευση της εισαγωγής
        self.transaction.amount = amount  # Αποθήκευση του ποσού στη μεταβλητή self.transaction.amount
        print(f"ποσό: {self.transaction.amount}")

    def epomeno1(self):
        self.show_page1()


    def epomeno2(self):
        page=self.radio_var3.get()
        if page==1:
            self.show_page2()
        elif page==2:
            self.show_page2()
        elif page==3:
            self.show_page2()
        elif page==4:
            self.show_page4()
        elif page==5:
            self.show_page6()



      
    
    
    def epomeno3(self):
        page=self.radio_var3.get()
        if page==1:
            self.transaction.category = self.entry1.get()
            self.transaction.description = self.entry2.get()
            print(f"Κατηγορία: {self.transaction.category}, Περιγραφή: {self.transaction.description}")
            cat=check_description(self.transaction.category)
            des=check_description(self.transaction.description)
            results = self.transaction.load_transaction(self.transaction.description)
            if results:
                self.label8.configure(text="Η συναλλαγή υπάρχει ήδη. Παρακαλώ επιλέξτε άλλο όνομα.")
                if cat==0 or des==0:
                    self.label8.configure(text="Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                    self.show_page2()
                elif cat==2 or des==2:
                    self.label8.configure(text="Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
                    self.show_page2()
                
            elif results is None:
                if cat==0 or des==0:
                    self.label8.configure(text="Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                    self.show_page2()
                elif cat==2 or des==2:
                    self.label8.configure(text="Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
                    self.show_page2()
                elif cat==1 and des==1:
                    self.show_page3()

                    
                    

            self.insert_date = date.today()

        elif page==2:
            self.transaction.category = self.entry1.get()
            self.transaction.description = self.entry2.get()
            print(f"Κατηγορία: {self.transaction.category}, Περιγραφή: {self.transaction.description}")
            cat=check_description(self.transaction.category)
            des=check_description(self.transaction.description)
            results = self.transaction.load_transaction(self.transaction.description)
            results1=self.transaction.load_transaction(self.transaction.category)
            self.monthly=self.transaction.monthly
            if results or results1:
                self.label8.configure(text="Η συναλλαγή υπάρχει.")
                if cat==0 or des==0:
                    self.label8.configure(text="Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                    self.show_page2()
                elif cat==2 or des==2:
                    self.label8.configure(text="Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
                    self.show_page2()
                elif des==1 and cat==1:
                    self.show_page2b()
            elif results or results1 is None:
                self.label8.configure(text="Η συναλλαγή δεν υπάρχει.")
                if cat==0 or des==0:
                    self.label8.configure(text="Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                    self.show_page2()
                elif cat==2 or des==2:
                    self.label8.configure(text="Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.") 
                    self.show_page2()
            self.insert_date = date.today()
            
        elif page==3:
            self.transaction.description = self.entry2.get()
            print(f"Κατηγορία: {self.transaction.category}, Περιγραφή: {self.transaction.description}")
            des=check_description(self.transaction.description)
            results = self.transaction.load_transaction(self.transaction.description)
            results1=self.transaction.load_transaction(self.transaction.category)
            if results or results1:
                self.label8.configure(text="Η συναλλαγή υπάρχει. Και διαγράφηκε επιτυχώς")
                if des==0:
                    self.label8.configure(text="Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                    self.show_page2()
                elif des==2:
                    self.label8.configure(text="Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.")
                    self.show_page2()
                elif des==1:
                    self.call_transactions()
            elif results or results1 is None:
                self.label8.configure(text="Η συναλλαγή δεν υπάρχει.")
                if des==0:
                    self.label8.configure(text="Λάθος είσοδος. Παρακαλώ προσπαθήστε ξανά")
                    self.show_page2()
                elif des==2:
                    self.label8.configure(text="Παρακαλώ εισάγετε μόνο γράμματα ή αριθμούς.") 
                    self.show_page2()
            self.insert_date = date.today()
                 
                
            


    def epomeno4(self):
        page=self.radio_var3.get()
        if page==1:
            try:
                self.transaction.monthly=self.radio_var1.get()
                self.transaction.type=self.radio_var2.get()
                print(f"Μηνιαία:{self.transaction.monthly},Εσοδο/Εξοδο:{self.transaction.type} ")
                self.money_input()
            except Exception as e:
                print(f"Error in epomeno3: {e}")
        elif page==2:
            try:
                self.new_amount=self.entry3.get()
                self.new_description=self.entry3.get()
                self.new_category=self.entry3.get()
                print(f"Μηνιαία:{self.transaction.monthly},Εσοδο/Εξοδο:{self.transaction.type} ")
            except Exception as e:
                print(f"Error in epomeno3: {e}")


    def epomeno5(self):
        page=self.radio_var3.get()
        if page==4:
            self.start_date=self.entry4.get()
            self.end_date=self.entry5.get()
            if not date_valid(self.start_date) or not date_valid(self.end_date):
                self.label12.configure(text="Μη έγκυρη μορφή ημερομηνίας, παρακαλώ προσπαθήστε ξανά.")
                self.show_page5()
            else:
                self.call_transactions()
        elif page==5:
            self.year=self.entry6.get()
            self.month=self.entry7.get()
            if date_valid(f"01-{self.month}-{self.year}"):
                self.call_transactions()
            else:
                self.btn6c.configure(text="Μη έγκυρο έτος ή μήνας. Παρακαλώ δοκιμάστε ξανά.")
                self.show_page6()



            
         
    def set_radio_var(self, var, value):

        var.set(value)
        if var==self.radio_var1:
            self.update_radio_buttons(self.btn_radio1, self.btn_radio2, value)
        elif var==self.radio_var2:
            self.update_radio_buttons(self.btn_radio3, self.btn_radio4, value)

        # Ενεργοποίηση του κουμπιού "Επόμενο" στη σελίδα 3 αν έχουν γίνει επιλογές
        if self.radio_var1.get() > 0 and self.radio_var2.get() > 0:
            self.btn6d.configure(state=NORMAL)
        else:
            self.btn6d.configure(state=DISABLED)
        




        # Ενημέρωση της μεταβλητής radio_var3

    def update_radio_buttons2_and_var(self, value):
        self.radio_var3.set(value)
        self.update_radio_buttons2(
            self.btn_radio5, self.btn_radio6, self.btn_radio7, self.btn_radio8, self.btn_radio9, value)
        if value > 0:           # Ενεργοποίηση του κουμπιού "Επόμενο" στη σελίδα 1 μόνο αν έχει επιλεγεί κάποια επιλογή
            self.btn6b.configure(state=NORMAL)          
        else:
            self.btn6b.configure(state=DISABLED)

    def update_radio_buttons3_and_var4(self, value):
        self.radio_var4.set(value)
        self.update_radio_buttons3(self.btn_radio10, self.btn_radio11, self.btn_radio12, self.btn_radio13, value)
        if value > 0:           # Ενεργοποίηση του κουμπιού "Επόμενο" στη σελίδα 1 μόνο αν έχει επιλεγεί κάποια επιλογή
            self.btn6b.configure(state=NORMAL)          
        else:
            self.btn6b.configure(state=DISABLED)

    def update_radio_buttons3_and_var5(self, value):
        self.radio_var5.set(value)
        self.update_radio_buttons3(self.btn_radio14, self.btn_radio15, self.btn_radio16, self.btn_radio17, value)
        if value > 0:           # Ενεργοποίηση του κουμπιού "Επόμενο" στη σελίδα 1 μόνο αν έχει επιλεγεί κάποια επιλογή
            self.btn6b.configure(state=NORMAL)          
        else:
            self.btn6b.configure(state=DISABLED)




    def update_radio_buttons(self, btn1, btn2, value):
        if value == 1:
            btn1.configure(fg_color="#123456")
            btn2.configure(fg_color="#1F6AA5")
        elif value == 2:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#123456")
        else:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#1F6AA5")

    def update_radio_buttons2(self, btn1, btn2, btn3, btn4, btn5, value):
        if value == 1:
            btn1.configure(fg_color="#123456")
            btn2.configure(fg_color="#1F6AA5")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
            btn5.configure(fg_color="#1F6AA5")
        elif value == 2:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#123456")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
            btn5.configure(fg_color="#1F6AA5")
        elif value==3:
            btn3.configure(fg_color="#123456")
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
            btn5.configure(fg_color="#1F6AA5")
        elif value==4:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#1F6AA5")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#123456")
            btn5.configure(fg_color="#1F6AA5")
        elif value==5:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#1F6AA5")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
            btn5.configure(fg_color="#123456")

    def update_radio_buttons3(self, btn1, btn2, btn3, btn4, value):
        if value == 1:
            btn1.configure(fg_color="#123456")
            btn2.configure(fg_color="#1F6AA5")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
        elif value == 2:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#123456")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
        elif value==3:
            btn3.configure(fg_color="#123456")
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#1F6AA5")
        elif value==4:
            btn1.configure(fg_color="#1F6AA5")
            btn2.configure(fg_color="#1F6AA5")
            btn3.configure(fg_color="#1F6AA5")
            btn4.configure(fg_color="#123456")

    def clear_page(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.grid_forget()

    # Καθαρίζει το κείμενο στα Entry Widgets
    def on_entry_click(self, event):
        widget = event.widget
        if widget.get() == "Πληκτρολογήστε εδώ...":
            widget.delete(0, "end")

    def on_focus_out(self, event):
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, "Πληκτρολογήστε εδώ...")

    def check_entries(self, event):
        page = self.radio_var3.get()

        if page == 1:
            if self.entry1.get() != "" and self.entry1.get() != "Πληκτρολογήστε εδώ..." and self.entry2.get() != "" and self.entry2.get() != "Πληκτρολογήστε εδώ...":
                self.btn6c.configure(state=NORMAL)
            else:
                self.btn6c.configure(state=DISABLED)
        elif page == 2 or page == 3:
            self.entry1.configure(state=NORMAL)  # Αλλάξτε από DISABLED σε NORMAL
            if self.entry2.get() != "" and self.entry2.get() != "Πληκτρολογήστε εδώ...":
                self.btn6c.configure(state=NORMAL)
            else:
                self.btn6c.configure(state=DISABLED)

    def call_transactions(self):
        page=self.radio_var3.get()
        choice=self.radio_var4.get()
        if page==1:
            category=self.transaction.category
            description=self.transaction.description
            monthly=self.transaction.monthly
            type=self.transaction.type
            amount=self.transaction.amount
            self.transaction.create_transaction(category,description,monthly,type,amount)
        elif page==2:
            if choice==1:
                new_amount=float(self.new_amount)
                old_amount=self.transaction.amount
                type=self.transaction.type
                description=self.transaction.description
                self.transaction.update_amount(new_amount,old_amount,type,description)
            elif choice==2:
                old_description=self.transaction.description
                new_description=self.new_description
                self.transaction.update_description(old_description,new_description)
            elif choice==3:
                old_category=self.transaction.category
                new_category=self.new_category
                description=self.transaction.description
                self.transaction.update_category(old_category,new_category,description)
            elif choice==4:
                monthly=self.monthly
                self.transaction.update_monthly(monthly)
        elif page==3:
            description=self.transaction.description
            type=self.transaction.type
            amount=self.transaction.amount
            self.transaction.delete_transaction(description,type,amount)
        elif page==4:
            start_date = self.entry4.get()
            end_date = self.entry5.get()
            category5 = self.radio_var5.get()
            
            try:
                category_stem_plot(start_date, end_date, category5)
            except Exception as e:
                print(f"Error: {e}")
        elif page==5:
            year=self.entry6.get()
            month=self.entry7.get()
            connection=self.transaction.connector
            try:
                export_to_excel(connection, year, month)
            except Exception as e:
                print(f"Error: {e}")
    
    
    
    
    
    
    def run(self):
        self.mainloop()

 
if __name__ == "__main__":
    project = Project()
    project.run()
    