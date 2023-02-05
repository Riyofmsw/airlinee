import mysql.connector
import mysql.connector
from dotenv import dotenv_values
#read envirement variables
from datetime import date
from pathlib import Path
import os
parent_path = Path(__file__).parent
parent_path = Path(parent_path).parent
config_file = os.path.join(parent_path,'.env')
config = dotenv_values(config_file) 
print(config)
class DB:
    def __init__(self):
        self.tablename = config['DATABASE_HOST']
        self.mydb = mysql.connector.connect(
             host=config['DATABASE_HOST'],
            user=config['DATABASE_USER'],
            password=config['DATABASE_PASSWORD'],
            database=config['DATABASE_NAME']
        )
    def get_tweets_by_airline_and_class(self,airline,classe):
        mycursor = self.mydb.cursor()
        mycursor.execute(f"SELECT * FROM {self.tablename} where airline='{airline}' and class='{classe}' ")
        myresult = mycursor.fetchall()
        mycursor.close()
        return myresult
    def is_tweet_exists(self,tweet):
        tweet = tweet.replace('"','')
        mycursor = self.mydb.cursor()
        print(f'SELECT * FROM {self.tablename} where tweet="{tweet}" ')
        mycursor.execute(f'SELECT * FROM {self.tablename} where tweet="{tweet}" ')
        myresult = mycursor.fetchall()
        mycursor.close()
        return True if len(myresult) !=0 else False
    def insert(self,data):
        mycursor = self.mydb.cursor()
        if not self.is_tweet_exists(data['tweet']):
            sql = f'INSERT INTO {self.tablename} (tweet,cleaned_tweet,airline,class) VALUES (%s, %s,%s,%s)'
            val = (data['tweet'],data['cleaned_tweet'],data['airline'],data['class'])
            mycursor.execute(sql, val)
            self.mydb.commit()

db = DB()