import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
from werkzeug.security import generate_password_hash

db = mysql.connector.connect(
    host=os.getenv("DB_HOST","127.0.0.1"),
    port=int(os.getenv("DB_PORT","3306")),
    user=os.getenv("DB_USER","root"),
    password=os.getenv("DB_PASSWORD",""),
    database=os.getenv("DB_NAME","barangay_health_center")
)
cur=db.cursor()
username=input("Admin username [admin]: ").strip() or "admin"
password=input("Admin password [admin123]: ").strip() or "admin123"
full_name=input("Full name [System Administrator]: ").strip() or "System Administrator"
cur.execute("""INSERT INTO users(username,password_hash,full_name,role)
VALUES(%s,%s,%s,'Administrator')
ON DUPLICATE KEY UPDATE password_hash=VALUES(password_hash),full_name=VALUES(full_name),role='Administrator'""",
(username,generate_password_hash(password),full_name))
db.commit();cur.close();db.close()
print("Administrator account is ready.")
