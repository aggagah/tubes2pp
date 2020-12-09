import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

root = tk.Tk()
root.title("Tubes 2: To Do Program")
s = ttk.Style()
s.configure('Treeview', rowheight=16)

cal = Calendar(root, font='Arial 14', selectmode='day',
               local='id_ID', cursor='hand1')
cal.grid(row=0, column=0, sticky='N', rowspan=8)

treev = ttk.Treeview(root)
treev.grid(row=0, column=1, sticky='WNE', rowspan=4, columnspan=2)
scrollBar = tk.Scrollbar(root, orient='vertical', command=treev.yview)
scrollBar.grid(row=0, column=3, sticky="ENS", rowspan=4)


treev.configure(yscrollcommand=scrollBar.set)
treev['columns'] = ("1", "2")
treev['show'] = 'headings'
treev.column("1", width=100)
treev.heading("1", text="JAM")
treev.heading("2", text="Judul")


root.mainloop()
