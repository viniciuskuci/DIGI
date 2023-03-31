import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import json
import numpy as np
import pandas as pd

class POSTGRES_FETCH:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def schedule(self, event_name, event_value,
                 host, port, user, password, dbname,
                 table_name):
        if event_name == 'INIT':
            # catch exception for invalid SQL connection
            try:
                # declare a new PostgreSQL connection object
                self.conn = psycopg2.connect(dbname=dbname, 
                    user=user, 
                    password=password,
                    host=host,
                    port=port)
                self.cursor = self.conn.cursor()
            except OperationalError as err:

                print(err)
                # set the connection to 'None' in case of error
                self.conn = None
            finally:
                return [event_value, None, None]

        elif event_name == 'RUN':
            if self.conn != None:
                query1 = "SELECT tempo_inicio FROM \"ProcessedParts\""
                query2 = "SELECT tempo_fim FROM \"ProcessedParts\" "
                try:
                    self.cursor.execute(query1)
                    start_times = self.cursor.fetchall()
                    size_1 = len(start_times)

                    self.cursor.execute(query2)
                    end_times = self.cursor.fetchall()
                    size_2 = len(end_times)

                    ziped = list(zip(start_times, end_times))
                    table = pd.DataFrame(ziped, columns=['Start', 'End'])
                    result = table.to_json(orient="split", date_format="iso", date_unit="us")
                    return [None, event_value, result]

                except Exception as err:
                    print(err)

                finally:
                    # self.cursor.close()
                    # self.conn.close()
                    # return None in case of any exception
                    return [None, event_value, None]
            
            else:
                print("No active connection to PostgreSQL DB.")
                return [None, event_value, None]
        
    
