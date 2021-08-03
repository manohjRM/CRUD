from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E , N, S, Entry, END, StringVar, Scrollbar, Toplevel, font

from tkinter import ttk
import sqlite3

class contacts:
    db_filename = 'contacts.db'
    def __init__(self, root):
        self.root = root
        self.create_gui()
        ttk.style = ttk.Style()
        ttk.style.configure('Treeview', font=('helvetica', 10))
        ttk.style.configure('Treeeview.Heading', font=('helvetica', 12, 'bold'))

    def execute_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print('You have successfully connected to db')
            cursor = conn.cursor()
            query_result  = cursor.execute(query, parameters)
            conn.commit()
        return query_result
        
    def create_gui(self):
        
        self.create_left_icon()
        self.create_lable_frame()
        self.create_message()
        self.create_tree_view()
        self.create_scrollV()
        self.create_scrollH()
        self.create_bottom_buttons()
        self.view_records()
        

    def create_left_icon(self):
        photo = PhotoImage(file='dtlogo.gif')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

    def create_lable_frame(self):
        lableframe = LabelFrame(self.root, text='Create New', bg='sky blue')
        lableframe.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        Label(lableframe, text='Company Name: ', bg='red', fg='white').grid(row=1, column=1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(lableframe)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5, pady=2)
        Label(lableframe, text='Contact Person: ', bg='red', fg='white').grid(row=2, column=1, sticky=W, pady=2, padx=15)
        self.personfield = Entry(lableframe)
        self.personfield.grid(row=2, column=2, sticky=W, padx=5, pady=2)
        Label(lableframe, text='Email: ', bg='red', fg='white').grid(row=3, column=1, sticky=W, pady=2, padx=15)
        self.emailfield = Entry(lableframe)
        self.emailfield.grid(row=3, column=2, sticky=W, padx=5, pady=2)
        Label(lableframe, text='Number: ', bg='red', fg='white').grid(row=4, column=1, sticky=W, pady=2, padx=15)
        self.numfield = Entry(lableframe)
        self.numfield.grid(row=4, column=2, sticky=W, padx=5, pady=2)
        Label(lableframe, text='Additional Number: ', bg='red', fg='white').grid(row=5, column=1, sticky=W, pady=2, padx=15)
        self.anumfield = Entry(lableframe)
        self.anumfield.grid(row=5, column=2, sticky=W, padx=5, pady=2)
        Label(lableframe, text='Designation: ', bg='red', fg='white').grid(row=6, column=1, sticky=W, pady=2, padx=15)
        self.desgfield = Entry(lableframe)
        self.desgfield.grid(row=6, column=2, sticky=W, padx=5, pady=2)
        Button(lableframe, text='Add Contact', command=self.on_add_clicked,bg='blue', fg='white').grid(row=7,column=2, sticky=E, padx=5, pady=5)

    def create_message(self):
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=1,sticky=W)

    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10, columns=('contact_person', 'email', 'number', 'additional_number', 'designation'), style='Treeview')
        self.tree.grid(row=9, column=0, columnspan=6)
        self.tree.heading('#0', text='Company Name', anchor=W)
        self.tree.heading('contact_person', text='Contact Person', anchor=W)
        self.tree.heading('email', text='Email ID', anchor=W)
        self.tree.heading('number', text='Contact Number', anchor=W)
        self.tree.heading('additional_number', text='Additional Contact', anchor=W)
        self.tree.heading('designation', text='Designation', anchor=W)

    def create_scrollV(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=9, column=6, rowspan=10, sticky='sn')

    def create_scrollH(self):
        self.scrollbar = Scrollbar(orient='horizontal', command=self.tree.xview)
        self.scrollbar.grid(row=10, columnspan=2, sticky=S)

    def create_bottom_buttons(self):
        Button(text='Delete Selected', command=self.on_delete_selected_button_clicked, bg='red',fg='white').grid(row=12, column=0, sticky=W, pady=10, padx=20)
        Button(text='Modify Selected', command=self.on_modify_selected_button_clicked, bg='purple',fg='white').grid(row=12, column=1, sticky=W, pady=10, padx=20)

    def on_add_clicked(self):
        self.new_contact()

    def on_delete_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_contacts()

    def on_modify_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            self.message['text'] = 'No item selected to modify'
            return
        self.open_modify_window()

    def new_contact(self):
        if self.new_contact_validation():
            query = 'INSERT INTO contacts VALUES(NULL,?,?,?,?,?,?)'
            parameters = (self.namefield.get(),self.personfield.get(),self.emailfield.get(),self.numfield.get(),self.anumfield.get(),self.desgfield.get())
            self.execute_query(query, parameters)
            self.message['text'] = 'New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0, END)
            self.personfield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
            self.anumfield.delete(0, END)
            self.desgfield.delete(0, END)

        else:
            self.message['text'] = 'Please give all details'
            pass
        self.view_records()

    def new_contact_validation(self):
        return len(self.namefield.get()) != 0 and len(self.personfield.get()) != 0 and len(self.numfield.get()) != 0

    def view_records(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = "SELECT * FROM contacts"
        contact_entries = self.execute_query(query)
        for row in contact_entries:
            self.tree.insert('',0,text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))

    def delete_contacts(self):
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacts WHERE Company_name = ?'
        self.execute_query(query, (name,))
        self.message['text'] = 'Contacts for {} deleted'.format(name)
        self.view_records()

    def open_modify_window(self):
        name = self.tree.item(self.tree.selection())['text']
        old_number = self.tree.item(self.tree.selection())['values'][2]
        self.transient = Toplevel()
        self.transient.title('Update Contact')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Contact Number:').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_number), state='readonly').grid(row=1, column=2)

        Label(self.transient, text='New Phone Number:').grid(
            row=2, column=1)
        new_phone_number_entry_widget = Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2, column=2)


        Button(self.transient, text='Update Contact', command=lambda: self.update_contacts(
            new_phone_number_entry_widget.get(), old_number, name)).grid(row=3, column=2, sticky=E)


        self.transient.mainloop()

    def update_contacts(self, newphone, old_phone,name):
        query = 'UPDATE contacts SET number=? WHERE number =? AND Company_name =?'
        parameters = (newphone, old_phone, name)
        self.execute_query(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Phone number of {} modified'.format(name)
        self.view_records()
        

if __name__ == '__main__':
    root = Tk()
    root.title("Customers")
    application = contacts(root)
    root.mainloop()