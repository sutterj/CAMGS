import sqlite3 as sql
import csv


def build_csv(value_id):
    connection = sql.connect('../db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
         'SELECT * FROM generator_composition WHERE id IS '
         + value_id)
    csv_file = open('../user_data/composition' + value_id + '.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)
    csv_file.close()
    connection.close()

    connection = sql.connect('../db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
         'SELECT * FROM generator_noteobject WHERE composition_id IS '
         + value_id + ' ORDER BY order ASC')
    csv_file = open('../user_data/notes' + value_id + '.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)
    csv_file.close()
    connection.close()
