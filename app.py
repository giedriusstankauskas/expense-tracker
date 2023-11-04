from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)


@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.form.get('description')
    amount = request.form.get('amount')

    if description and amount:
        expense = Expense(description=description, amount=amount)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
    else:
        flash('Please provide both description and amount.', 'danger')

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
