from tkinter import *
from tkinter.ttk import Treeview
import sqlite3
from tkinter import messagebox
from db1 import Database

db=Database('WGS_testRun.db')

def populate_list(NOTE=''):
	for i in router_tree_view.get_children():
		router_tree_view.delete(i)
	for row in db.fetch(NOTE):
		router_tree_view.insert('', 'end', values=row)


def populate_list2(query='Select * from SAMPLE_METADATA_TABLE'):
	for i in router_tree_view.get_children():
		router_tree_view.delete(i)
	for row in db.fetch2(query):
		router_tree_view.insert('', 'end', values=row)

def add_router():
	if note_text.get() == '' or base_text.get() == '' or snp_text.get() == '' or freq_text.get() == '':
		messagebox.showerror('Required Fields', "Please include all fields")
		return
	db.insert(hostname.get(), brand_text.get())
	clear_text()
	populate_list()

def select_router(event):
	try:
		global selected_item
		index = router_tree_view.selection()[0]
		selected_item=router_tree_view.item(index)['values']
		note_entry.delete(0, END)
		note_entry.insert(END, selected_item[1])
		base_entry.delete(0, END)
		base_entry.insert(END, selected_item[2])
		snp_entry.delete(0, END)
		snp_entry.insert(END, selected_item[3])
		freq_entry.delete(0, END)
		freq_entry.insert(END, selected_item[4])
	except IndexError:
		pass

def remove_router():
	db.remove(selected_item[0])
	clear_text()
	populate_list()

def update_router():
	db.update(selected_item[0], note_text.get(), base_text.get(), snp_text.get(), freq_text.get())
	populate_list()

def clear_text():
	note_entry.delete(0, END)
	base_entry.delete(0, END)
	snp_entry.delete(0, END)
	freq_entry.delete(0, END)

def search_hostname():
	note=hostname_search.get()
	populate_list(note)

def execute_query():
	query=query_search.get()
	populate_list2(query)

#create GUI
app = Tk()
frame_search = Frame(app)
frame_search.grid(row=0, column=0)

lbl_search = Label(frame_search, text="Search by ATTR_VAL keyword", font=('bold', 12), pady=20)
lbl_search.grid(row=0, column=0, sticky=W)
hostname_search = StringVar()
hostname_search_entry = Entry(frame_search, textvariable=hostname_search)
hostname_search_entry.grid(row=0, column=1)

lbl_search = Label(frame_search, text="Search by Query", font=("bold", 12), pady=20)
lbl_search.grid(row=1, column=0, sticky=W)
query_search = StringVar()
query_search.set('SELECT * from SAMPLE_METADATA_TABLE WHERE ATTR_VAL = {}'.format("'"+"BR_IVX"+"'"))
query_search_entry = Entry(frame_search, textvariable=query_search, width = 40)
query_search_entry.grid(row=1, column=1)

#Fields from database
frame_fields = Frame(app)
frame_fields.grid(row=1, column=0)

note_text = StringVar()
note_label = Label(frame_fields, text="NOTE", font=("bold", 12))
note_label.grid(row=0, column=0, sticky=E)
note_entry = Entry(frame_fields, textvariable=note_text)
note_entry.grid(row=0, column=1, sticky=W)

base_text = StringVar()
base_label = Label(frame_fields, text="BASE", font=("bold", 12))
base_label.grid(row=0, column=2, sticky=E)
base_entry = Entry(frame_fields, textvariable=base_text)
base_entry.grid(row=0, column=3, sticky=W)

snp_text = StringVar()
snp_label = Label(frame_fields, text="SNP", font=("bold", 12))
snp_label.grid(row=1, column=0, sticky=E)
snp_entry = Entry(frame_fields, textvariable=snp_text)
snp_entry.grid(row=1, column=1, sticky=W)

freq_text = StringVar()
freq_label = Label(frame_fields, text="FREQ", font=("bold", 12))
freq_label.grid(row=1, column=2, sticky=E)
freq_entry = Entry(frame_fields, textvariable=freq_text)
freq_entry.grid(row=1, column=3, sticky=W)

#treeview with scrollbar
frame_router = Frame(app)
frame_router.grid(row=4, column=0, columnspan=5, rowspan=6, pady=20, padx=20)

columns=['SAMPLE', 'NOTE', 'BASE', 'SNP', 'FREQ']
router_tree_view = Treeview(frame_router, columns=columns, show="headings")
router_tree_view.column('SAMPLE', width=30)
for col in columns[1:]:
	router_tree_view.column(col, width=120)
	router_tree_view.heading(col, text=col)
router_tree_view.bind('<<TreeviewSelect>>', select_router)
router_tree_view.pack(side="left", fill="y")
scrollbar = Scrollbar(frame_router, orient='vertical')
scrollbar.configure(command=router_tree_view.yview)
scrollbar.pack(side="right", fill ="y")
router_tree_view.config(yscrollcommand=scrollbar.set)

#action buttons
frame_btns=Frame(app)
frame_btns.grid(row=3, column=0)

add_btn = Button(frame_btns, text="Add Entry", width=12, command=add_router)
add_btn.grid(row=0, column=0, pady=20)

remove_btn = Button(frame_btns, text="Remove Entry", width=12, command=remove_router)
remove_btn.grid(row=0, column=1)

update_btn = Button(frame_btns, text="Update Entry", width=12, command=update_router)
update_btn.grid(row=0, column=2)

clear_btn = Button(frame_btns, text="Clean Input", width=12, command=clear_text)
clear_btn.grid(row=0, column=3)

search_btn = Button(frame_search, text="Search", width=12, command=search_hostname)
search_btn.grid(row=0, column=2)

search_query_btn = Button(frame_search, text ="Search Query", width=12, command=execute_query)
search_query_btn.grid(row=1, column=2)

#title/geometry of app; populate
app.title('Pilot GUI Test')
app.geometry('750x500')

#populate data
populate_list()

#start program
app.mainloop()


