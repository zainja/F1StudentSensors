from rethinkdb import RethinkDB
from tkinter import *
from tkinter.ttk import *

window = Tk()
r = RethinkDB()
connection = False
try:
    conn = r.connect("sam.soon.it", 8912).repl()
    connection = True
except:
    exit(0)


def initiate_connection(window):
    if connection:
        receive_data(window)


def stop_connection():
    conn.close()


def receive_data(tk_window):
    cursor = r.db("F1_data").table("sensor_data").changes().run()
    for document in cursor:
        print(document['new_val']['RPM'])
        tk_window.update_idletasks()
        rpm_bar['value'] = document['new_val']['RPM']/10**68


rpm_label = Label(window, text="RPM")
rpm_label.grid(row=0)
rpm_bar = Progressbar(window, orient=HORIZONTAL, length=1000, mode='determinate')
rpm_bar.grid(row=0, column=1)
init_button = Button(window, text="Read Data", command=lambda: initiate_connection(window)).grid(row=1, column=0)


window.geometry("600x600")
window.mainloop()
