from flask import Flask,request,render_template
import os
import psycopg2
from datetime import datetime,timezone
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt


##################################

# DATABASE 

CREATE_USER_TABLE=(
    "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,name Text NOT NULL,job_title TEXT NULL  ,email TEXT NOT NULL,password TEXT NOT NULL,token TEXT NULL, UNIQUE(email));"
)

CREATE_COMPANY_TABLE=(
    "CREATE TABLE IF NOT EXISTS company(company_id SERIAL PRIMARY KEY,email TEXT NOT NULL,job_id INTEGER,company TEXT NOT NULL,industry TEXT NOT NULL,address TEXT NOT NULL,phone TEXT NOT NULL,employees_no INTEGER,website_url TEXT,password TEXT NOT NULL,UNIQUE(email));"
    )

CREATE_Collaboration_TABLE="""CREATE TABLE IF NOT EXISTS collaboration(collaboration_id SERIAL PRIMARY KEY,project_name TEXT NOT NULL,industry TEXT NOT NULL,date TIMESTAMP,FOREIGN KEY(company_id) REFERENCES users(id) ON DELETE CASCADE);"""

CREATE_JOB_TABLE=("CREATE TABLE IF NOT EXISTS job(job_id SERIAL PRIMARY KEY,company_id  TEXT,email TEXT NOT NULL,title TEXT NOT NULL,working_hrs TEXT NOT NULL,job_type TEXT NOT NULL,industry TEXT NOT NULL,location TEXT NOT NULL,job_role TEXT NOT NULL,description TEXT NOT NULL,min_salary INTEGER NOT NULL,max_salary INTEGER NOT NULL,years_of_experience TEXT NOT NULL,FOREIGN KEY(email) REFERENCES company(email) ON DELETE CASCADE);")
INSERT_JOB_DATA=("INSERT INTO job(email,company_id,title,working_hrs,job_type,industry,location,job_role,description,min_salary,max_salary,years_of_experience) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *;")

LOGIN_USER=("SELECT * FROM users WHERE password=(%s) AND email =(%s);")
INSERT_USER_RETURN_ID = "INSERT INTO users(name,email,password,job_title,token) VALUES(%s,%s,%s,%s,%s) RETURNING id;"
UPDATE_USER_RETURN_ID ="UPDATE users SET password=(%s) WHERE email=(%s) AND token=(%s)  RETURNING *;"
INSERT_COMPANY_DATA=("INSERT INTO company(job_id,email,company,industry,address,phone,employees_no,website_url,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING company_id;")





load_dotenv()
app=Flask(__name__)
bcrypt = Bcrypt(app)
url=os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)



@app.route("/")
def index():
    return render_template("index.html")

# register
@app.post("/api/register")
def register():
    data=request.get_json() 
    name=data["name"]
    email=data["email"]
    password=data['password']
    job_title=data["job_title"]
    
    Token=data["token"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID,(name,email,password,job_title ,Token))
            name_id=cursor.fetchone()
    return {"id":name_id,"data":"User added"},201

    
    
# login
@app.post("/api/login")
def login():
    data=request.get_json()
    email=data["email"]
    password1=data['password']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(LOGIN_USER,(password1,email))
            user_data=cursor.fetchall()[0]
            print(user_data)
    return {"user":user_data[1]},200
    
# reset password
@app.post("/api/reset")
def rest_password():
    data=request.get_json()
    Token=data["token"]
    email=data["email"]
    password1=data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE users SET password='{password1}' WHERE email='{email}' OR token='{Token}'  RETURNING *;"
)
            user_data=cursor.fetchone()
        
            return {"id":user_data,"data":"Password Updated Successfully"},200
    


# add company
@app.post("/api/company")
def company():
    data=request.get_json()
    job_id=data["job_id"]
    company=data["company"]
    employees_no=data["employees_no"]
    address=data["address"]
    phone=data["phone"]
    industry=data["industry"]
    website_url=data["website_url"]
    password=data["password"]
    email=data["email"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_COMPANY_TABLE)
            cursor.execute(INSERT_COMPANY_DATA,(job_id,email,company,industry,address,phone,employees_no,website_url,password))
            user_data=cursor.fetchall()[0]
            return {"id":user_data[0],"data":"Company Added"},200
    

# fetch companies
@app.get("/api/companies")
def companies():
    data=request.get_json()
    company=data["company"]
    address=data["address"]
    industry=data["industry"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM company WHERE company ='{company}' OR address =  '{address}' OR industry ='{industry}';")
            user_data=cursor.fetchall() 
            print(len(user_data[0]))
            return {"data":user_data}


# Search Jobs
@app.get("/api/job")
def searchJob():
    data=request.get_json()
    title=data["title"]
    job_type=data['job_type']
    industry=data['industry']
    location=data["location"]
    working_hrs=data["working_hrs"]
    min_salary=data["min_salary"]
    max_salary =data["max_salary"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM job WHERE title ='{title}' OR working_hrs ='{working_hrs}' OR job_type ='{job_type}' OR industry ='{industry}' OR location ='{location}' OR min_salary ='{min_salary}' OR max_salary='{max_salary}';")
            user_data=cursor.fetchall()
    return {"data":user_data}


# add jobs
@app.post("/api/add_job")
def addJob():
    data=request.get_json()
    email=data["email"]
    company_id=data["company_id"]
    title=data["title"]
    working_hrs=data["working_hrs"]
    job_type=data['job_type']
    industry=data['industry']
    location=data["location"]
    job_role=data["job_role"]
    description=data["description"]
    min_salary=data["min_salary"]
    max_salary=data["max_salary"]
    years_of_experience=data["years_of_experience"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_JOB_TABLE)
            cursor.execute(INSERT_JOB_DATA,(email,company_id,title,working_hrs,job_type,industry,location,job_role,description,min_salary,max_salary,years_of_experience))
            user_data=cursor.fetchall()[0]
            print(user_data)
    return {"data":user_data}


#donate
@app.post("/api/donate")
def donate():
    data=request.get_json()
    cause_donating_to=data["cause_donating_to"]
    target_amount=data["target_amount"]
    amount=data["amount"]
    donation_info=data["donation_info"]
    date=data["date"]
    created_by=data["created_by"]
    donation_type=data["donation_type"]
    image_url=data["image_url"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
    "CREATE TABLE IF NOT EXISTS donate(donation_id SERIAL PRIMARY KEY, cause_donating_to TEXT NOT NULL,target_amount INTEGER NOT NULL,amount INTEGER,donation_info TEXT NOT NULL,donation_type TEXT NOT NULL,image_url TEXT NOT NULL,date TEXT NOT NULL,created_by TEXT NOT NULL );"
)
            cursor.execute(f"INSERT INTO donate(cause_donating_to,target_amount,amount,donation_info,donation_type,image_url,date,created_by) VALUES ('{cause_donating_to}',{target_amount},{amount},'{donation_info}','{donation_type}','{image_url}','{date}','{created_by}') RETURNING *;")
            user_data=cursor.fetchall()[0]
    print(user_data)
    return {"data":user_data}

@app.get("/api/donations")
def donations():
    data=request.get_json()
    amount=data["amount"]
    date=data['date']
    created_by=data["created_by"]
    donation_type=data["donation_type"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM donate WHERE amount={amount} OR date='{date}' OR  created_by='{created_by}' OR donation_type='{donation_type}';")

            user_data=cursor.fetchall()[0]
            print(user_data,"DATA")

    return {"data":user_data}



