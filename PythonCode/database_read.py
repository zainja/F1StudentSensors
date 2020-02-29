from rethinkdb import RethinkDB

r = RethinkDB()
conn = r.connect("localhost", 28015).repl()
d = {}
cursor = r.db("F1_data").table("sensor_data").changes().run()
for document in cursor:
    print(document['new_val'])