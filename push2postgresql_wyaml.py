import psycopg2
import yaml
from icecream import ic

def PSQL_INSERT(sql, incoming):
    with open('notes.yaml', 'r') as stream:
        try:
            db_credentials = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    db_credentials = db_credentials[0]['Notes']
    conn = psycopg2.connect(host=db_credentials['host'],
                            database=db_credentials['database'],
                            user=db_credentials['user'],
                            password=db_credentials['password'])

    cur = conn.cursor()
    cur.execute(sql, incoming)
    conn.commit()
    cur.close()

    return ic('Completed INSERT')

# sql = """INSERT INTO rbwolfff."NOTES" ("dateTouch", "dateStore", "dateWrite", "noteType", "filePath", "rawText") VALUES (%s, %s, %s, %s, %s, %s);"""
