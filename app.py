from flask import   Flask , request , jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import psycopg
import os
import traceback

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)


DATABASE_URL = os.environ.get("DATABASE_URL")
def get_db_connection():
    return psycopg.connect(DATABASE_URL)


@app.route("/api/sign-up", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username", "").strip() 
    password = data.get("password", "").strip()
    email    = data.get("email",    "").strip().lower()
    phone_number = data.get("phone_number", "").strip()

    # check for empty fields
    if not all([username, password, email, phone_number]):
        return jsonify({"error": "All fields are required"}), 400
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")


    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # check existing user 
        cursor.execute("""
                    SELECT user_id
                    FROM users
                    WHERE username = %s 
                        """,
                        (username,)
                        )
        existing_username = cursor.fetchone()
        if existing_username:
            cursor.close()
            conn.close()
            return jsonify({"error":"Username already exists."}),409

        
                    #Checks if email already exists 
        cursor.execute("""
                        SELECT user_id
                        FROM users
                        WHERE email = %s
                                    """,
                    (email,)
                    )
        existing_email = cursor.fetchone()
                
        if existing_email :
                        cursor.close()
                        conn.close()
                        return{"error":"Email already registered"},409

        cursor.execute("""
            INSERT INTO users(
            username,
            passwor_hash,
            email,
            phone_number)
            VALUES(%s,%s,%s,%s)
            """,(username,
                 password_hash,
                 email,
                 phone_number)
                 )

        
        
        conn.commit()
    except Exception as e:
        traceback.print_exc()
        # return({"error":str(e)}),500
        return ({"error":"Something went wrong"}),500

    return jsonify({"message":"Account created"}),200

@app.route("/api/log-in",methods = ["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    # check for empty fields
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
                        SELECT * FROM users 
                        WHERE email = %s
                    """,(email,))
        conn.commit()
        user = cursor.fetchone()

        # if user isnt found
        if not user :
             return jsonify({"error":"User does not exist"})
        
    except Exception as e:
         traceback.print_exc()
    return jsonify({"message":"Welcome back."})

# add tasks
@app.route("api/add_task",methods =["POST"])
def add_task():
    data = request.get_json()

    task_title =data.get("task_title", "")
    date = data.get("date","")
    priority = data.get("priority", "")
    description = data.get("description", "")

    # empty field check
    if not task_title or date or description or priority :
         return jsonify({"error":"All fields are required"}),400

    try:
     conn = get_db_connection()
     cursor = conn.cursor()

     cursor.execute("""
        INSERT INTO tasks(
        task_title,
        date,
        priority,
        description
        )
        VALUES(%s,%s,%s,%s)    
        """,(
             task_title,
             date,
             priority,
             description
        ))
     conn.commit()
    except Exception as e:
         traceback.print_exc()
        #  return ({"error":str(e)}),500
         return jsonify({"error":"Task could not be added.Please try again."}),500
    return jsonify({"message":"Task added successfully"}),200







# if __name__ == "__main__":
#     app.run(debug=True)

