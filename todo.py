import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from time import strftime
import getpass
import datetime


todos = {}


def detailTodo(cb=None):
    tanggal = str(cal.selection_get())
    win = tk.Toplevel()
    win.wm_title("Detail todo")
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)["text"]
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value=selectedTodo["judul"])
    tk.Label(win, text="Tanggal:").grid(row=0, column=0, sticky="N")
    tk.Label(win,text="{} | {}".format(tanggal,selectedTodo["waktu"])).grid(row=0,column=1,sticky="E")
    tk.Label(win, text="Judul:").grid(row=1, column=0, sticky="N")
    tk.Entry(win, state="disabled", textvariable=judul).grid(row=1,column=1,sticky="E")
    tk.Label(win, text="Keterangan:").grid(row=2, column=0, sticky="N")
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, sticky="E")
    keterangan.insert(tk.INSERT, selectedTodo["keterangan"])
    keterangan.configure(state="disabled")


def LoadTodos():
    global todos
    f = open("mytodo.dat", "r")
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()


def SaveTodos():
    f = open("mytodo.dat", "w")
    f.write(str(todos))
    f.close()


def delTodo():
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        tanggal = str(cal.selection_get())
        selectedItem = treev.focus()
        ms = tk.messagebox.askquestion("Delete ToDo","Yakin hapus ToDo?",icon="question")
        if ms == "yes":
            todos[tanggal].pop(treev.item(selectedItem)["text"])
            tk.messagebox.showinfo("Delete ToDo", "ToDo berhasil dihapus")
        else:
            tk.messagebox.showinfo("Delete ToDo", "ToDo batal dihapus")
    else:
        tk.messagebox.showinfo("Delete ToDo", "Tidak ada ToDo tersedia untuk dihapus!", icon='warning')
    ListTodo()


def ListTodo(cb=None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("","end",text=i,values=(todos[tanggal][i]["waktu"],todos[tanggal][i]["judul"]),)


def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        "waktu": "{}:{}".format(jam.get(), menit.get()),
        "judul": judul.get(),
        "keterangan": keterangan.get("1.0", tk.END),
    }

    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]

    win.destroy()
    ListTodo()

# membuat function addForm
def AddForm():
    win = tk.Toplevel()
    win.wm_title("+")
    jam = tk.IntVar(value=10)
    menit = tk.IntVar(value=30)
    judul = tk.StringVar(value="")
    tk.Label(win, text="Waktu\t    :").grid(row=0, column=0, sticky='W')
    tk.Spinbox(win, from_=0, to=23, textvariable=jam, width=2).grid(row=0,column=1, sticky="W")
    tk.Spinbox(win, from_=0, to=59, textvariable=menit, width=2).grid(row=0,column=1, sticky="E")
    tk.Label(win, text="Judul\t    :").grid(row=1, column=0, sticky='W')
    tk.Entry(win, textvariable=judul).grid(row=1, column=1, columnspan=3)
    tk.Label(win, text="Keterangan:").grid(row=2, column=0,sticky='W')
    keterangan = ScrolledText(win, width=13, height=5,)
    keterangan.grid(row=2, column=1, columnspan=5, rowspan=4)
    tanggal = str(cal.selection_get())
    tk.Button(win,text="Tambah",command=lambda: addTodo(win, tanggal, jam, menit, judul, keterangan), width=7).grid(row=6, column=1, sticky='S')
    tk.Button(win,text="Batal",command=win.destroy, width=7).grid(row=6, column=2, sticky='SE')


def title():
    waktu = strftime("%H:%M")
    tanggal = str(cal.selection_get())
    root.title(tanggal + " | " + waktu + " | Kalenderku ")


# Membuat settingan waktu untuk sapaan
def waktuLocal():
    jamLocal = datetime.datetime.now().time()
    jamLocal.hour
    global waktu
    if (jamLocal.hour>= 5 and jamLocal.hour <= 10) or (jamLocal.hour >=1 and jamLocal.hour < 5):
        waktu = "Morning"
    elif jamLocal.hour> 10 and jamLocal.hour <= 18:
        waktu = "Afternoon"
    elif jamLocal.hour > 18 or (jamLocal.hour > 0 and jamLocal.hour < 1):
        waktu = "Night"
    return waktu

root = tk.Tk()
s = ttk.Style()
s.configure("Treeview", rowheight=19)

# Membuat calendar
cal = Calendar(root, font="Calibri 14", selectmode="day", locale="id_ID", cursor="hand2", showweeknumbers=False)
cal.grid(row=0, column=0, sticky="N", rowspan=8, columnspan=2)
cal.bind("<<CalendarSelected>>", ListTodo)
cal.configure(foreground='#424242', background='#f5f5f5', headersbackground='#f5f5f5', headersforeground='#424242', normalbackground='#fafafa', normalforeground='#424242', selectforeground='#1e88e5', selectbackground='#fafafa', weekendbackground='#f8f8f8', weekendforeground='#e57373', othermonthbackground='#eeeeee', othermonthwebackground='#eeeeee', othermonthweforeground='#ef9a9a')
tanggal = str(cal.selection_get())


# Membuat sapaan
waktu = ''
username = getpass.getuser()
sapaan = tk.Label(font='Cursive 14', text="Good {} {}.\nHow is it going?".format(waktuLocal(), username.title()))
sapaan.grid(row=0, column=3, rowspan=2, columnspan=2)
sapaan.configure(width=30, foreground='#424242')

# Membuat widget di sebelah kanan dari calendar
treev = ttk.Treeview(root)
treev.grid(row=2, column=3, sticky="WNE", rowspan=7, columnspan=2)

# Membuat scroll y axis di sebelah kanan
scrollBar = tk.Scrollbar(root, orient="vertical", command=treev.yview)
scrollBar.grid(row=3, column=4, sticky="ENS", rowspan=5)

# mendesign widget di sebelah kanan calendar
treev.configure(yscrollcommand=scrollBar.set)
treev.bind("<Double-1>", detailTodo)
treev["columns"] = ("1", "2")
treev["show"] = "headings"
treev.column("1", width=100)
treev.heading("1", text="JAM")
treev.heading("2", text="Judul")



# Membuat button "Tambah"
btnAdd = tk.Button(root, text="Add ToDo", font='Arial 9 bold', width=10, command=AddForm, background='#eeeeee', foreground='#424242', borderwidth=0.5)
btnAdd.grid(row=8, column=0, sticky="W")
# Membuat button "Hapus"
btnDel = tk.Button(root, text="Delete", font='Arial 9 bold', width=10, command=delTodo, background='#eeeeee', foreground='#e57373', borderwidth=0.5)
btnDel.grid(row=8, column=1, sticky="E")

# Membuat button "Load"
btnLoad = tk.Button(root, text="Load", font='Arial 9 bold', width=10, command=LoadTodos, background='#eeeeee', foreground='#424242', borderwidth=0.5)
btnLoad.grid(row=8, column=0, sticky="E")

# Membuat tombol "Save"
btnSave = tk.Button(root, text="Save", font='Arial 9 bold', width=10, command=SaveTodos, background='#eeeeee', foreground='#424242', borderwidth=0.5)
btnSave.grid(row=8, column=1, sticky="W")

title()
root.mainloop()
