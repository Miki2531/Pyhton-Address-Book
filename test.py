import json
from uuid import uuid4 as uuid
import tkinter as tk
from tkinter import messagebox , ttk
from typing import List
class AddressBook:
    def __init__(self, name, address, phone, email, id=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        if id is None:
            self.id =str(uuid())[:4]
        else:
            self.id = id
    def save(self):
        with open('addressBook.json') as f:
            data = json.load(f)
         
        data.append(self.__dict__)
        with open('addressBook.json', 'w') as f:
            json.dump(data, f, indent=4)
        
    def update(self):
        with open('addressBook.json') as f:
            data = json.load(f)

        for i, address in enumerate(data):
            if address.get('id') == self.id:
                data[i] = self.__dict__
            
        with open('addressBook.json', 'w') as f:
            json.dump(data, f, indent=4)

    def delete(self):
        with open('addressBook.json') as f:
            data = json.load(f)
        
        
        for i, address in enumerate(data):
            if address.get('id') == self.id:
                data.pop(i)
            
        with open('addressBook.json', 'w') as f:
            json.dump(data, f, indent=4)
     

    @classmethod
    def get(cls, id):
        with open('addressBook.json') as f:
            data = json.load(f)
        
        
        for address in data:
            if address.get('id') == id:
                return cls(**address)
            
        # with open('addressBook.json', 'w') as f:
        #     json.dump(data, f, indent=4)

    @classmethod
    def load(cls):
        with open('addressbook.json') as f:
            data = json.load(f)
            return[cls(**address) for address in data]


class MainGUI:

    def __init__(self):
        self.window= tk.Tk()
        self.window.title('Address Book')
        self.window.geometry('600x800')

        self.form_frame, self.name_entry, self.address_entry, self.phone_entry, self.email_entry = self.add_form()
        self.form_frame.pack(fill="x", padx=10, pady=10)

        self.submit_button = tk.Button(self.window, text='submit', command=self.submit)
        self.submit_button.pack(pady=10)

        addresses = AddressBook.load()
        self.add_table(addresses)
        

        self.window.mainloop()

    def add_form(self):
        form_frame = tk.Frame(self.window)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, minsize=10)

        name_lable = tk.Label(form_frame, text='Name')
        name_lable.grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1, sticky='w', pady=10)

        address_lable = tk.Label(form_frame, text='Address')
        address_lable.grid(row=1, column=0, sticky='e')
        address_entry = tk.Entry(form_frame)
        address_entry.grid(row=1, column=1, sticky='w', pady=10)

        phone_lable = tk.Label(form_frame, text='phone')
        phone_lable.grid(row=2, column=0, sticky='e')
        phone_entry = tk.Entry(form_frame)
        phone_entry.grid(row=2, column=1, sticky='w', pady=10)

        email_lable = tk.Label(form_frame, text='Email')
        email_lable.grid(row=3, column=0, sticky='e')
        email_entry = tk.Entry(form_frame)
        email_entry.grid(row=3, column=1, sticky='w', pady=10)


        return form_frame, name_entry, address_entry, phone_entry, email_entry
    
    def submit(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        address = AddressBook(name, address, phone, email)
        address.save()

        self.name_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        messagebox.showinfo('success', 'Address saved successfully')
    

    def add_table(self, addresses: List[AddressBook]):
        columns = ('Id', 'Name', 'Address', 'Phone', 'Email')

        tree = ttk.Treeview(self.window, columns=columns, show='headings')
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        for address in addresses:
            tree.insert('', 'end', values=(address.id, address.name, address.address, address.phone, address.email))


        tree.pack(fill="both", expand=True, padx=10, pady=10)

        return tree




MainGUI()




