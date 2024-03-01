
from tkinter import *
from tkinter import ttk
import mysql.connector

myDB= mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="Library"
)
Cursor = myDB.cursor()


root = Tk()
root.title('CustomersDataBaseRedactor')

root.geometry("1000x500")


  
#Создание рамки для Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Создание treeview
my_tree = ttk.Treeview(tree_frame, selectmode="extended")
my_tree.pack()

#Задание колонок
my_tree['columns'] = ("First Name", "Last Name", "ID", "City", "Street", "House_flat")

#Форматирование заголовков
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("First Name", anchor=W, width=140)
my_tree.column("Last Name", anchor=W, width=140)
my_tree.column("ID", anchor=CENTER, width=100)
my_tree.column("City", anchor=CENTER, width=140)
my_tree.column("Street", anchor=CENTER, width=140)
my_tree.column("House_flat", anchor=CENTER, width=140)

#Создание заголовков
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("First Name", text="Имя", anchor=W)
my_tree.heading("Last Name", text="Фамилия", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("City", text="Город", anchor=CENTER)
my_tree.heading("Street", text="Улица", anchor=CENTER)
my_tree.heading("House_flat", text="Дом/квартира", anchor=CENTER)


data_frame = LabelFrame(root, text="Запись")
data_frame.pack(fill="x", expand="yes", padx=20)

fn_label = Label(data_frame, text="Имя")
fn_label.grid(row=0, column=0, padx=10, pady=10)
fn_entry = Entry(data_frame)
fn_entry.grid(row=0, column=1, padx=10, pady=10)

ln_label = Label(data_frame, text="Фамилия")
ln_label.grid(row=0, column=2, padx=10, pady=10)
ln_entry = Entry(data_frame)
ln_entry.grid(row=0, column=3, padx=10, pady=10)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=4, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=5, padx=10, pady=10)

address_label = Label(data_frame, text="Город")
address_label.grid(row=1, column=0, padx=10, pady=10)
city_entry = Entry(data_frame)
city_entry.grid(row=1, column=1, padx=10, pady=10)

city_label = Label(data_frame, text="Улица")
city_label.grid(row=1, column=2, padx=10, pady=10)
street_entry = Entry(data_frame)
street_entry.grid(row=1, column=3, padx=10, pady=10)

state_label = Label(data_frame, text="Дом/Квартира")
state_label.grid(row=1, column=4, padx=10, pady=10)
house_flat_entry = Entry(data_frame)
house_flat_entry.grid(row=1, column=5, padx=10, pady=10)

def query_database():

	Cursor.execute("SELECT * FROM customers")
	records = Cursor.fetchall()
	
	global count
	count = 0
	print(records)

	for record in records:
		my_tree.insert(parent='', index='end', text='', values=(record[0], record[1], record[2],record[3], record[4], record[5]))

def remove_one():
    x= my_tree.selection()[0]
    my_tree.delete(x)

    Cursor.execute("DELETE from customers WHERE id=" + id_entry.get())
    myDB.commit()

    clear_entries()

def remove_all():
    for record in my_tree.get_children():
        my_tree.delete(record)
    Cursor.execute("TRUNCATE TABLE customers")
    
def clear_entries():
	#Очистка полей ввода
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)
	city_entry.delete(0, END)
	street_entry.delete(0, END)
	house_flat_entry.delete(0, END)

def select_record():
	
	clear_entries()

	#Номер записи
	selected = my_tree.focus()
	#Значения записи
	values = my_tree.item(selected, 'values')

	#Вставка в поля ввода
	fn_entry.insert(0, values[0])
	ln_entry.insert(0, values[1])
	id_entry.insert(0, values[2])
	city_entry.insert(0, values[3])
	street_entry.insert(0, values[4])
	house_flat_entry.insert(0, values[5])

def update_record():
	selected = my_tree.focus()
	


	my_tree.item(selected, text="", values=(fn_entry.get(), ln_entry.get(), id_entry.get(), city_entry.get(), street_entry.get(), house_flat_entry.get(),))

	
	Cursor.execute("DELETE from customers WHERE id=" + id_entry.get())
	Cursor.execute("INSERT INTO customers(first_name, last_name, id, city, street, house_flat) values(%s,%s,%s,%s,%s,%s)", (fn_entry.get(),ln_entry.get(),id_entry.get(),city_entry.get(),street_entry.get(),house_flat_entry.get()))
	myDB.commit()
	clear_entries()
	
def add_record():
	
	Cursor.execute("INSERT INTO customers(first_name, last_name, id, city, street, house_flat) values(%s,%s,%s,%s,%s,%s)", (fn_entry.get(),ln_entry.get(),id_entry.get(),city_entry.get(),street_entry.get(),house_flat_entry.get()))
	myDB.commit()

	
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)
	city_entry.delete(0, END)
	street_entry.delete(0, END)
	house_flat_entry.delete(0, END)
	
	
	my_tree.delete(*my_tree.get_children())

	query_database()

#Добавление копок
button_frame = LabelFrame(root, text="Операции")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Обновить запись", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Добавить запись", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Удалить все записи", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Удалить выбранную запись", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

select_clear_button = Button(button_frame, text="Очистить поля ввода", command=clear_entries)
select_clear_button.grid(row=0, column=7, padx=10, pady=10)
select_record_button = Button(button_frame, text="Выбрать Запись", command=select_record)
select_record_button.grid(row=0, column=8, padx=10, pady=10)



query_database()

root.mainloop()