from rethinkdb import RethinkDB
from tkinter import *
from tkinter.ttk import *
from threading import Thread

window = Tk()
r = RethinkDB()
connection = False
try:
    # conn = r.connect("localhost", 8912).repl()
    conn = r.connect("localhost", 28015).repl()

    connection = True
except:
    exit(0)


def stop_connection():
    global conn, window
    conn.close()
    window.destroy()
    exit(0)
# thread function
def receive_data():
    global window, conn
    cursor = r.db("F1_data").table("sensor_data").changes().run(conn)
    print("running")
    for document in cursor:
        print("ren")
        if document['old_val'] is None:
            print(document['new_val']['RPM'])
            window.update_idletasks()
            rpm_bar['value'] = ((document['new_val']['RPM']) / 32767) * 100


read_data = Thread(target=receive_data, daemon=True)
read_data.start()
rpm_label = Label(window, text="RPM")
rpm_label.grid(row=0)
rpm_bar = Progressbar(window, orient=HORIZONTAL, length=100, mode='determinate')
rpm_bar.grid(row=0, column=1)
stop_button = Button(window, text="Stop Reading", command=lambda: stop_connection()).grid(row=1, column=1)

window.geometry("600x600")
window.mainloop()
