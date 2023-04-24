import json
from uuid import uuid4 as uuid
import tkinter as tk
from tkinter import messagebox , ttk
from typing import List
class AddressBook:
    gender = ''
    def __init__(self, name, address, phone, email, gender="", id=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.gender = gender
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
            if address.get('id') == str(id):
                return cls(**address)
            
        # with open('addressBook.json', 'w') as f:
        #     json.dump(data, f, indent=4)

    @classmethod
    def load(cls):
        with open('addressbook.json') as f:
            data = json.load(f)
            return[cls(**address) for address in data]

    
    @classmethod
    def search(cls, query):
        with open('addressbook.json') as f:
            data = json.load(f)
        results = []
        for address in data:
            if query.lower() in address.get('name').lower():
                results.append(cls(**address))

        return results



class MainGUI:

    def __init__(self):
        self.window= tk.Tk()
        self.window.title('Address Book')
        self.window.geometry('600x800')

        self.detail_address = None
        self.form_frame, self.name_entry, self.address_entry, self.phone_entry, self.email_entry, self.gender_entry = self.add_form()
        self.form_frame.pack(fill="x", padx=10, pady=10)

        self.submit_button = tk.Button(self.window, text='submit', command=self.submit, bg="blue", fg="yellow")
        self.submit_button.pack(pady=10)


        self.search_entry = tk.Entry(self.window)
        self.search_entry.pack(pady=10)
        self.search_entry.bind('<Key>', self.search_address)
        search_button = tk.Button(self.window, text='Search', command=self.search_address)
        search_button.pack(pady=10)
        search_button.bind('<Key>', self.search_address)
        addresses = AddressBook.load()
        self.tree = self.add_table(addresses)
        

        self.window.mainloop()

    def add_form(self, window=None, name=None, address=None, phone=None, email=None, gender=None):
        form_frame = tk.Frame(window or self.window)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, minsize=10)

        name_lable = tk.Label(form_frame, text='Name', fg="white", bg="black")
        name_lable.grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(form_frame)
        if name is not None:
            name_entry.insert(0, name)
        name_entry.grid(row=0, column=1, sticky='w', pady=10)

        address_lable = tk.Label(form_frame, text='Address', fg="white", bg="black")
        address_lable.grid(row=1, column=0, sticky='e')
        address_entry = tk.Entry(form_frame)
        if address is not None:
            address_entry.insert(0, address)
        address_entry.grid(row=1, column=1, sticky='w', pady=10)

        phone_lable = tk.Label(form_frame, text='phone', fg="white", bg="black")
        phone_lable.grid(row=2, column=0, sticky='e')
        phone_entry = tk.Entry(form_frame)
        if phone is not None:
            phone_entry.insert(0, phone)
        phone_entry.grid(row=2, column=1, sticky='w', pady=10)

        email_lable = tk.Label(form_frame, text='Email', fg="white", bg="black")
        email_lable.grid(row=3, column=0, sticky='e')
        email_entry = tk.Entry(form_frame)
        if email is not None:
            email_entry.insert(0, email)
        email_entry.grid(row=3, column=1, sticky='w', pady=10)

        gender_lable = tk.Label(form_frame, text='gender', fg="white", bg="black")
        gender_lable.grid(row=4, column=0, sticky='e')
        gender_entry = tk.Entry(form_frame)
        if gender is not None:
            gender_entry.insert(0, gender)
        gender_entry.grid(row=4, column=1, sticky='w', pady=10)


        return form_frame, name_entry, address_entry, phone_entry, email_entry, gender_entry
    
    def submit(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        gender = self.gender_entry.get()

        address = AddressBook(name, address, phone, email, gender)
        address.save()

        self.name_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.gender_entry.delete(0, 'end')
        messagebox.showinfo('success', 'Address saved successfully')
        self.tree.destroy()
        self.tree = self.add_table(AddressBook.load())
    

    def add_table(self, addresses: List[AddressBook]):
        columns = ('Id', 'Name', 'Address', 'Phone', 'Email', 'gender')

        tree = ttk.Treeview(self.window, columns=columns, show='headings')
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        for address in addresses:
            tree.insert('', 'end', values=(address.id, address.name, address.address, address.phone, address.email, address.gender))


        tree.pack(fill="both", expand=True, padx=10, pady=10)
        tree.bind('<<TreeviewSelect>>', self.column_click)


        return tree
    def column_click(self, event):
        try:
            item_selected = self.tree.selection()[0]
            item = self.tree.item(item_selected).get('values')
            address = AddressBook.get(item[0])
            self.detail_view(address)
            

        except Exception as e:
            print(e)

    def detail_view(self, address: AddressBook):
        self.detail_window = tk.Toplevel(self.window)
        self.detail_window.title(f'{address.name} address Detail')
        self.detail_window.geometry("400x300")
        self.detail_address = address
        self.detail_form_frame, self.detail_name_entry, self.detail_address_entry, self.detail_phone_entry, self.detail_email_entry, self.detail_gender_entry = self.add_form(
            self.detail_window, address.name, address.address, address.phone, address.email, address.gender
        )
        self.detail_form_frame.pack(fill="x", expand=True, padx=10, pady=10)

        self.detail_submit_button = tk.Button(self.detail_window, text='Update', command=self.update)
        self.detail_submit_button.pack(pady=10)
        self.detail_delete_button = tk.Button(self.detail_window, text='Delete', command=self.delete, fg='red')
        self.detail_delete_button.pack(pady=10)


        self.detail_window.mainloop()
    
    def update(self):
        if not self.detail_address:
            return
        
        self.detail_address.name = self.detail_name_entry.get()
        self.detail_address.address = self.detail_address_entry.get()
        self.detail_address.phone = self.detail_phone_entry.get()
        self.detail_address.email = self.detail_email_entry.get()
        self.detail_address.gender = self.detail_gender_entry.get()

        self.detail_address.update()
        self.detail_window.destroy()
        self.detail_address = None

        messagebox.showinfo('Success', 'Address update successfully!')
        self.tree.destroy()
        self.tree =self.add_table(AddressBook.load())

    def delete(self):
        if not self.detail_address:
            return
        if messagebox.askokcancel("Delete", "Do you want to delete?"):
            self.detail_address.delete()
            self.detail_window.destroy()
            self.detail_address = None
            messagebox.showinfo('Success', 'Address book successfully deleted!')
            self.tree.destroy()
            self.tree = self.add_table(AddressBook.load())
    
    def search_address(self, event=None):
        search_query = self.search_entry.get()
        addresses = AddressBook.search(search_query)
        self.tree.destroy()
        self.tree = self.add_table(addresses)





MainGUI()




