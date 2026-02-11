from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# --- Optional: free AI placeholder ---
def ask_biomedlm(symptoms_text):
    # Disclaimer: This is a placeholder. Not real medical advice.
    return f"Based on the reported symptoms ({symptoms_text}), here is some educational information..."

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Change this for production security

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- List of symptoms to ask ---
SYMPTOMS_LIST = [
    "fever",
    "cough",
    "headache",
    "sore throat",
    "fatigue",
    "nausea",
    "shortness of breath"
]

# --- Routes ---
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        finally:
            conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password."
    return render_template("login.html")

# --- THIS IS THE MISSING PART THAT CAUSED YOUR ERROR ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
# -----------------------------------------------------

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/diagnosis", methods=["GET", "POST"])
def diagnosis():
    if "username" not in session:
        return redirect(url_for("login"))

    # Initialize session tracking if it doesn't exist
    if "symptom_index" not in session:
        session["symptom_index"] = 0
        session["symptom_answers"] = []

    if request.method == "POST":
        # Save answer
        answer = request.form.get("answer")
        
        # We must retrieve the list, append to it, and re-save it
        current_answers = session.get("symptom_answers")
        current_answers.append((SYMPTOMS_LIST[session["symptom_index"]], answer))
        session["symptom_answers"] = current_answers
        
        session["symptom_index"] += 1

    # Check if we are done with all symptoms
    if session["symptom_index"] >= len(SYMPTOMS_LIST):
        summary = ", ".join(f"{symptom}: {ans}" for symptom, ans in session["symptom_answers"])
        try:
            result = ask_biomedlm(summary)
        except Exception as e:
            print("AI error:", e)
            result = "Sorry, there was a problem generating the educational explanation."
        
        # Reset session so they can try again later
        session.pop("symptom_index", None)
        session.pop("symptom_answers", None)
        
        return render_template("result.html", result=result)

    current_symptom = SYMPTOMS_LIST[session["symptom_index"]]
    return render_template("diagnosis.html", symptom=current_symptom)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)