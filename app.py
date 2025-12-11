from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "RivaSecretKey123"

EXCEL_FILE = "Talabalar-11_12_2025_09_24_31.xlsx"

# Excelni o'qish
data = pd.read_excel(EXCEL_FILE, engine='openpyxl').fillna("")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        passport = request.form.get("passport").strip().upper()
        passport_col = "Pasport raqami"  # Exceldagi ustun nomi (bo'sh joy bo'lmasligi kerak)
        if passport_col not in data.columns:
            flash("❌ Excelda 'Pasport raqami' ustuni topilmadi!")
            return redirect(url_for("login"))

        found = data[data[passport_col].astype(str).str.upper() == passport]

        if not found.empty:
            session["passport"] = passport
            session["student_info"] = found.iloc[0].to_dict()
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Pasport topilmadi. Iltimos, to‘g‘ri raqam kiriting.")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "passport" not in session:
        return redirect(url_for("login"))
    student_info = session.get("student_info", {})
    return render_template("dashboard.html", student=student_info)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
