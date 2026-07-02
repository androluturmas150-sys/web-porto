import mysql.connector
import os

from dotenv import load_dotenv

import cloudinary
import cloudinary.uploader



load_dotenv()



# ======================
# CLOUDINARY CONFIG
# ======================


cloudinary.config(

    cloud_name=os.getenv("CLOUD_NAME"),

    api_key=os.getenv("CLOUD_API_KEY"),

    api_secret=os.getenv("CLOUD_API_SECRET")

)





# ======================
# DATABASE TiDB CONNECT
# ======================


def connect():


    db = mysql.connector.connect(


        host=os.getenv("DB_HOST"),


        user=os.getenv("DB_USER"),


        password=os.getenv("DB_PASSWORD"),


        database=os.getenv("DB_NAME"),


        port=4000,


        ssl_disabled=False,


        ssl_verify_cert=False,


        ssl_verify_identity=False


    )


    return db