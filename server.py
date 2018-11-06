from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = "secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/create_email', methods=["POST"])
def create():

	mysql = connectToMySQL('emaildb')
	emails = mysql.query_db("SELECT email FROM email")
	if not EMAIL_REGEX.match (request.form['email']): #check if input follows email format
		flash("*email doesn't follow email format")
		return redirect('/')

	for email in emails: #check if email input is already in the database
		print(email)
		if request.form['email'] == email['email']:
			flash("*email is already in the database")
			return redirect('/')
	else:
		mysql = connectToMySQL('emaildb')
		query = "INSERT INTO email(email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW())" 
		data = {
		'email': request.form['email']
		}
		add_email = mysql.query_db(query, data)
	return redirect('/success')

@app.route('/success')
def view_email():
	mysql = connectToMySQL('emaildb')
	emails = mysql.query_db("SELECT * FROM email")
	print(emails)

	return render_template('success.html', emails= emails)

if __name__ == "__main__":
	app.run(debug=True)