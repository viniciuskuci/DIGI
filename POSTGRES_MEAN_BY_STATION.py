# ATENTION! First install dependencies (example for Linux): 
# sudo apt install python3-dev libpq-dev
# pip install psycopg2
# Error handling took from: https://kb.objectrocket.com/postgresql/python-error-handling-with-the-psycopg2-postgresql-adapter-645
# Error handling must be improved, not working with queries

import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import json
import numpy as np
import pandas as pd

class POSTGRES_MEAN_BY_STATION:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def schedule(self, event_name, event_value,
                 host, port, user, password, dbname, id):
        if event_name == 'INIT':
            try:
                self.conn = psycopg2.connect(dbname=dbname, 
                    user=user, 
                    password=password,
                    host=host,
                    port=port)
                self.cursor = self.conn.cursor()
            except OperationalError as err:

                print(err)
                self.conn = None
            finally:
                return [event_value, None, None]
        elif event_name == 'RUN':
            if self.conn != None:  
                query = "SELECT AVG(tempo_fim - tempo_inicio) AS \"value\" FROM \"ProcessedParts\" where station_id = %s"
                try:
                    self.cursor.execute(query, (id,))
                    data = self.cursor.fetchone()
                    MEAN = data[0].total_seconds()
                    print(MEAN)
                    return [None, event_value, MEAN]
                except Exception as err:
                    print(err)
                finally:
                    #self.cursor.close()
                    #self.conn.close()
                    return [None, event_value, None]
            else:
                print("No active connection to PostgreSQL DB.")
                return [None, event_value, None]

#a = POSTGRES_MEAN_BY_STATION()
#retorno = a.schedule("INIT", 1, "192.168.1.103", 5432, "postgres", "myPassword", "LineStatistics", 2)
#retorno = a.schedule("RUN", 1, "192.168.1.103", 5432, "postgres", "myPassword", "LineStatistics", 2) 



   
