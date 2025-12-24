
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "contact_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="3695",
    database="contact_manager"
)
cursor = db.cursor(buffered=True)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))

    return render_template('login.html')


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
            (username, email, password)
        )
        db.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute(
        "SELECT * FROM contacts WHERE user_id=%s",
        (session['user_id'],)
    )
    contacts = cursor.fetchall()
    return render_template('dashboard.html', contacts=contacts)


# ---------------- ADD CONTACT ----------------
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        cursor.execute(
            "INSERT INTO contacts (name, phone, email, user_id) VALUES (%s,%s,%s,%s)",
            (name, phone, email, session['user_id'])
        )
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_contact.html')


# ---------------- EDIT CONTACT ----------------
@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        cursor.execute(
            "UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s",
            (name, phone, email, id)
        )
        db.commit()
        return redirect(url_for('dashboard'))

    cursor.execute("SELECT * FROM contacts WHERE id=%s", (id,))
    contact = cursor.fetchone()
    return render_template('edit_contact.html', contact=contact)


# ---------------- DELETE CONTACT ----------------
@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    cursor.execute("DELETE FROM contacts WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for('dashboard'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)