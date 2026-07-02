from flask import Flask, render_template, request, redirect, session

from database import connect


import cloudinary
import cloudinary.uploader


import resend

import os

from dotenv import load_dotenv



load_dotenv(override=True)

print("RESEND KEY:", os.getenv("RESEND_API_KEY"))



app = Flask(__name__)


app.secret_key = "portfolio_secret"



# ======================
# CONFIG
# ======================


cloudinary.config(

    cloud_name=os.getenv("CLOUD_NAME"),

    api_key=os.getenv("CLOUD_API_KEY"),

    api_secret=os.getenv("CLOUD_API_SECRET")

)



resend.api_key = os.getenv("RESEND_API_KEY")







# ======================
# HOME
# ======================


@app.route("/")
def home():


    db = connect()

    c = db.cursor(dictionary=True)



    c.execute("""
        SELECT *
        FROM profiles
        LIMIT 1
    """)

    profile = c.fetchone()



    c.execute("""
        SELECT *
        FROM skills
    """)

    skills = c.fetchall()



    c.execute("""
        SELECT *
        FROM experiences
    """)

    experiences = c.fetchall()



    c.execute("""
        SELECT *
        FROM projects
    """)

    projects = c.fetchall()



    db.close()



    return render_template(

        "index.html",

        profile=profile,

        skills=skills,

        experiences=experiences,

        projects=projects

    )









# ======================
# LOGIN
# ======================


@app.route("/login", methods=["GET","POST"])

def login():


    if request.method=="POST":


        username=request.form["username"]

        password=request.form["password"]



        if username=="admin" and password=="admin123":


            session["admin"]=username


            return redirect("/admin")



    return render_template("login.html")









# ======================
# ADMIN
# ======================


@app.route("/admin")

def admin():


    if "admin" not in session:


        return redirect("/login")



    db=connect()

    c=db.cursor(dictionary=True)



    c.execute("SELECT * FROM profiles LIMIT 1")

    profile=c.fetchone()



    c.execute("SELECT * FROM skills")

    skills=c.fetchall()



    c.execute("SELECT * FROM experiences")

    experiences=c.fetchall()



    c.execute("SELECT * FROM projects")

    projects=c.fetchall()



    c.execute("SELECT * FROM contacts")

    contacts=c.fetchall()



    db.close()



    data={


        "profile":profile,

        "skills":skills,

        "experiences":experiences,

        "projects":projects,

        "contacts":contacts


    }



    return render_template(

        "admin.html",

        data=data

    )









# ======================
# PROFILE
# ======================


@app.route("/profile/update",methods=["POST"])

def profile_update():


    db=connect()

    c=db.cursor()



    c.execute("""

    UPDATE profiles

    SET

    nama_lengkap=%s,

    posisi=%s,

    deskripsi=%s

    WHERE id=1

    """,

    (

    request.form["nama_lengkap"],

    request.form["posisi"],

    request.form["deskripsi"]

    ))



    db.commit()

    db.close()



    return redirect("/admin")











# ======================
# SKILL
# ======================


@app.route("/skill/add",methods=["POST"])

def skill_add():


    image=request.files.get("image")


    image_url=None



    if image and image.filename!="":


        upload=cloudinary.uploader.upload(image)


        image_url=upload["secure_url"]




    db=connect()

    c=db.cursor()



    c.execute("""

    INSERT INTO skills

    (user_id,nama_skill,image_url)

    VALUES

    (1,%s,%s)

    """,

    (

    request.form["nama_skill"],

    image_url

    ))



    db.commit()

    db.close()



    return redirect("/admin")






@app.route("/skill/delete/<id>")

def skill_delete(id):


    db=connect()

    c=db.cursor()



    c.execute(

    "DELETE FROM skills WHERE id=%s",

    (id,)

    )



    db.commit()

    db.close()



    return redirect("/admin")









# ======================
# EXPERIENCE
# ======================


@app.route("/experience/add",methods=["POST"])

def experience_add():


    image=request.files.get("image")


    image_url=None



    if image and image.filename!="":


        upload=cloudinary.uploader.upload(

            image,

            folder="experience"

        )


        image_url=upload["secure_url"]




    db=connect()

    c=db.cursor()



    c.execute("""

    INSERT INTO experiences

    (user_id,pengalaman,keterangan,image_url)

    VALUES

    (1,%s,%s,%s)

    """,

    (

    request.form["pengalaman"],

    request.form["keterangan"],

    image_url

    ))



    db.commit()

    db.close()



    return redirect("/admin")







@app.route("/experience/delete/<id>")

def experience_delete(id):


    db=connect()

    c=db.cursor()



    c.execute(

    "DELETE FROM experiences WHERE id=%s",

    (id,)

    )



    db.commit()

    db.close()



    return redirect("/admin")







# ======================
# PROJECT
# ======================


@app.route("/project/add",methods=["POST"])

def project_add():


    db=connect()

    c=db.cursor()



    c.execute("""

    INSERT INTO projects

    (user_id,judul,keterangan)

    VALUES

    (1,%s,%s)

    """,

    (

    request.form["judul"],

    request.form["keterangan"]

    ))



    db.commit()

    db.close()



    return redirect("/admin")





# ======================
# PROJECT DELETE
# ======================


@app.route("/project/delete/<id>")
def project_delete(id):


    db = connect()

    c = db.cursor()



    c.execute(

        "DELETE FROM projects WHERE id=%s",

        (id,)

    )



    db.commit()

    db.close()



    return redirect("/admin")









# ======================
# CONTACT + RESEND
# ======================


@app.route("/contact/send",methods=["POST"])

def contact_send():


    nama=request.form["nama"]

    email=request.form["email"]

    pesan=request.form["pesan"]




    db=connect()

    c=db.cursor()



    c.execute("""

    INSERT INTO contacts

    (nama,email,pesan)

    VALUES

    (%s,%s,%s)

    """,

    (

    nama,

    email,

    pesan

    ))



    db.commit()

    db.close()






    resend.Emails.send({


        "from":

        "Portfolio <onboarding@resend.dev>",



        "to":

        ["androluturmas150@gmail.com"],



        "subject":

        "Pesan Baru Portfolio",



        "html":

        f"""

        <h2>Pesan dari {nama}</h2>

        <p>Email : {email}</p>

        <p>{pesan}</p>

        """

    })



    return redirect("/")









# ======================
# LOGOUT
# ======================


@app.route("/logout")

def logout():


    session.clear()


    return redirect("/login")









if __name__=="__main__":


    app.run()