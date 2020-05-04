import sqlite3 as sql
import csv

connection = sql.connect('../db.sqlite3')
cursor = connection.cursor()
cursor.execute(
        'SELECT * FROM generator_composition WHERE id IS 1')
csv_file = open('../user_data/composition1.csv', 'w')
csv_writer = csv.writer(csv_file, delimiter=",")
csv_writer.writerow([i[0] for i in cursor.description])
csv_writer.writerows(cursor)
csv_file.close()
connection.close()

connection = sql.connect('../db.sqlite3')
cursor = connection.cursor()
cursor.execute(
        'SELECT * FROM generator_noteobject WHERE composition_id IS 1')
csv_file = open('../user_data/notes1.csv', 'w')
csv_writer = csv.writer(csv_file, delimiter=",")
csv_writer.writerow([i[0] for i in cursor.description])
csv_writer.writerows(cursor)
csv_file.close()
connection.close()
