import mariadb
import os

# Establish mariadb connection
def get_connection():
    return mariadb.connect(
        user=os.getenv("MYSQL_USER", "gymuser"), 
        password=os.getenv("MYSQL_PASSWORD", "gympass"),
        host=os.getenv("MYSQL_HOST", "mariadb"),
        port=3306,
        database=os.getenv("MYSQL_DATABASE", "gymrag")
    )