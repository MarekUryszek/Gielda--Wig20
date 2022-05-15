from flask import Flask, redirect, render_template, url_for, request, flash, g, redirect
import sqlite3

app_info = {
    'db_file' : 'C:/Projekt/data/cantor.db'
}


app = Flask(__name__)

app.config['SECRET_KEY']='MMM'

def get_db():

    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):

    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

class Currency:
    
    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag

    def __repr__(self):
        return '<Currency {}>'.format(self.code)

class CantorOffer:

    def __init__(self):
        self.currencies= []
        self.denied_codes =[]

    def load_offer(self):
        self.currencies.append(Currency('TWTR','Twitter', 'twitter.png'))
        self.currencies.append(Currency('MSFT','Microsoft', 'microsoft.png'))
        self.currencies.append(Currency('AAPL','Apple', 'apple.png'))
        self.currencies.append(Currency('UBER','Uber', 'uber.png'))
        
        
    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        

@app.route('/')
def index():

    return render_template('index.html',active_menu='home')

@app.route('/exchange', methods=['GET','POST'])
def exchange():

    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange.html',active_menu='exchange', offer=offer)
    else:
        amount = 20
        if 'amount' in request.form:
            amount = request.form['amount']

        currency = 'MSFT'
        if 'currency' in request.form:
            currency = request.form['currency']

        kupno = '10.06.2010'
        if 'kupno' in request.form:
            kupno = request.form['kupno']

        sprzedaz = '10.06.2020'
        if 'sprzedaz' in request.form:
            sprzedaz = request.form['sprzedaz']
            
        if currency in offer.denied_codes:
            flash('The currency {} cannot be accepted'.format(currency))
        elif offer.get_by_code(currency) == 'unknown':
            flash('The selected currency is unknown and cannot be accepted')
        else:
            db =get_db()
            sql_command = 'insert into transactions(currency, amount, user) values(?, ?, ?)'
            db.execute(sql_command, [currency, amount, 'admin'])
            db.commit()
            flash('Kupiłeś {} akcji firmy {}.'.format(amount, currency))

        

        return render_template('exchange_results.html', active_menu='exchange', currency=currency, amount=amount,
                                    currency_info=offer.get_by_code(currency))
@app.route('/history')
def history():
    db = get_db()
    sql_command = 'select id, currency, amount, trans_date from transactions;'
    cur = db.execute(sql_command)
    transactions = cur.fetchall()

    return render_template('history.html',active_menu='history', transactions=transactions)

@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):

    db = get_db()
    sql_statement = 'delete from transactions where id = ?;'
    db.execute(sql_statement, [transaction_id])
    db.commit()

    return redirect(url_for('history'))


if __name__ == '__main__':
    app.run()
