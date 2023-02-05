from flask import Flask, render_template
from dotenv import dotenv_values
from pathlib import Path
#read envirement variables
from flask_mysqldb import MySQL
from utils.get_persante import get_persante
import os
import pandas as pd
config = dotenv_values(".env") 
app = Flask(__name__, static_folder='static')
#app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_HOST'] = config['DATABASE_HOST']
app.config['MYSQL_USER'] = config['DATABASE_USER']
app.config['MYSQL_PASSWORD'] = config['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = config['DATABASE_NAME']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
from pathlib import Path
parent_path = Path(__file__).parent
parent_path = str(parent_path)
ssl_ca = os.path.join(parent_path,'cacert-2023-01-10.pem')
ssl_ca = str(ssl_ca)
print(ssl_ca)
app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca":ssl_ca },'charset': 'utf8mb4'} 
mysql =MySQL(app)
airlines = {
        'Fly Nas':'flynas.jpg',
        'Fly Adeal':'fly-adeal.png',
        'Fly Dubai':'air-dubai.jpg',
        'Air Arabia':'air-arabia.jpg',
        'Ajazerah Airways':'aljazera-airlines.jpg',
    }
table = 'airplanes_tweets'
images_path = '../static/images'
@app.route("/")
def index():
    urls = ['flynas','fly-adeal','air-dubai','air-arabia','aljazera-airlines']
    data = zip(airlines.items(),urls)
    cur = mysql.connection.cursor()
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS `{table}` (
    `id` int(11) NOT NULL,
    `tweet` varchar(6000) DEFAULT NULL,
    `cleaned_tweet` varchar(6000) DEFAULT NULL,
    `airline` varchar(150) DEFAULT NULL,
    `class` varchar(150) DEFAULT NULL
    ) ENGINE=InnoDB ;
    ALTER TABLE {table} ADD PRIMARY KEY (`id`);
    ALTER TABLE {table} MODIFY `id` int(11) NOT NULL AUTO_INCREMENT; COMMIT;
    ''')
    return render_template("index.html",images_path=images_path,data=data)

@app.route("/airline/<airline>")
def airline(airline):
    airlines_name = ['flynas','fly-adeal','air-dubai','air-arabia','aljazera-airlines']

    if airline in airlines_name:
        airline_index = airlines_name.index(airline)
        airlines_csv_name = ['Fly Nas' ,'Fly Adeal' , 'Fly dubai','Alarabiah', 'Aljazeerah']
        airline_image = list(airlines.values())[airline_index]
        airline_image = f'{images_path}/{airline_image}'
        cur = mysql.connection.cursor()
        airline_name =  airlines_csv_name[airline_index]
        cur.execute(f'SELECT count(*) as count FROM {table} where airline="{airline_name}" and class="positive" ')
        postive_count = cur.fetchone()
        postive_count = postive_count ['count']
        cur.execute(f'SELECT count(*) as count FROM {table} where airline="{airline_name}" and class="negative" ')
        negative_count = cur.fetchone()
        negative_count = negative_count['count']
        somme = postive_count+negative_count
        postive_count = get_persante(somme,postive_count)
        postive_count = round(postive_count ,2)
        negative_count = get_persante(somme,negative_count)
        negative_count = round(negative_count ,2)
        cur.close()

        tweets_file_path = os.path.join(parent_path,'data')
        tweets_file_path = os.path.join(tweets_file_path,'tweets_Data.csv')
        df = pd.read_csv(tweets_file_path)
        tweets = df[df['Airline']==airline_name]
        tweets = [ {'tweet':tweet['tweet'],'class':tweet['Class']} for item,tweet in tweets.iterrows()]
        print(tweets)
        return render_template("airline.html",context=airline,airline_image=airline_image,postive_count=postive_count,negative_count=negative_count,tweets=tweets)
    return render_template("404.html")

if __name__ == '__main__':
	app.run(debug=True)