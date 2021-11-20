import psycopg2
import json
from icecream import ic

def PSQL_INSERT(sql, incoming):
    with open('notes.json', 'r') as stream:
        try:
            db_credentials = json.load(stream)
        except json.JSONDecodeError as exc:
            print(exc)

    db_credentials = db_credentials[0]['Notes']
    conn = psycopg2.connect(host=db_credentials.get('host'),
                            database=db_credentials.get('database'),
                            user=db_credentials.get('user'),
                            password=db_credentials.get('password'))

    cur = conn.cursor()
    cur.execute(sql, incoming)
    conn.commit()
    cur.close()



# sql = """INSERT INTO rbwolfff."NOTES" ("dateTouch", "dateStore", "dateWrite", "noteType", "filePath", "rawText") VALUES (%s, %s, %s, %s, %s, %s);"""
