from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list1 = [random.choice(letters) for i in range(nr_letters)]

    password_list2 = [random.choice(numbers) for i in range(nr_symbols)]

    password_list3 = [random.choice(symbols) for i in range(nr_numbers)]

    password_list = password_list1 + password_list2 + password_list3

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(END, password)
    pyperclip.copy(password)
    messagebox.showwarning(title="Copied", message="Password is copied to keyboard!!")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    new_data = {
        website:
            {
                "email": email,
                "password": password
            }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        error_mess = messagebox.showerror(title='Oops', message="Please don't leave any fields empty!!")

    else:
        try:
            with open('data.json', mode='r') as file:
                # loading old data
                data = json.load(file)
                # updating old to new data
                data.update(new_data)

            with open('data.json', mode='w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open('data.json', mode='w') as file:
                json.dump(new_data, file, indent=4)
        except json.decoder.JSONDecodeError:
            with open('data.json', mode='w') as file:
                json.dump(new_data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    name = website_entry.get()
    try:
        with open('data.json', mode='r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title='ERROR', message='No Data File Found !')
    else:
        if name in data:
            username = data[name]['email']
            password = data[name]['password']
            messagebox.showinfo(title=name, message=f'Username: {username}\nPassword: {password}')
        else:
            messagebox.showerror(title='ERROR', message='No details for the website exists')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(pady=50, padx=50)
window.title('Password Manager')

canvas = Canvas(width=200, height=200)
lock = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock)
canvas.grid(row=0, column=1)

# labels
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)
password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=18)
website_entry.focus()
website_entry.grid(row=1, column=1)
email_entry = Entry(width=35)
email_entry.insert(END, 'aryanmaingi2000@gmail.com')
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=18)
password_entry.grid(row=3, column=1)

# Button
generate_button = Button(text='Generate Password', command=generate_pass)
generate_button.grid(row=3, column=2)
add_button = Button(text='Add', width=32, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text='Search', width=12, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
