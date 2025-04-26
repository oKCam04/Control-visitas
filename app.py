from flask import Flask 
from flask_mongoengine import MongoEngine 
from dotenv import load_dotenv
import os 

load_dotenv()

app=Flask(__name__)
app.secret_key="12uyi348re589"

uri=os.environ.get("URI")
dbname=os.environ.get("DB")

app.config["UPLOAD_FOLDER"]= "./static/img"
app.config['MONGODB_SETTINGS']=[{
    "db":dbname,
    "host":uri
  
}]
print("Base de datos usada:", dbname)

db=MongoEngine(app)



if __name__ == '__main__':
    from routes.Entradas import *
    from routes.Usuario import *
    from routes.oficina import *
    from routes.RegistrarVisitante import *
    app.run(port=3000, host="0.0.0.0",debug=True)