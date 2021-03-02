import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db", connect_args={'check_same_thread': False})

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # create variables to collect all information needed to be displayed in this page (stocks, quantity, current price, value, sum of all stocks value, total cash, cash + holdings)
    username = session["user_id"]
    value_holdings = 0
    stocks = db.execute("SELECT * FROM portfolio WHERE id = :id", id = username)
    for stock in stocks:
        shares = int(stock["quantity"])
        symbol = stock["symbol"]
        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        value = float(price * shares)
        value_holdings += value

        stock["name"] = name
        stock["price"] = usd(price)
        stock["value"] = usd(value)
        stock["shares"] = shares

    cash = (db.execute("SELECT cash FROM users WHERE id = :id", id = username))[0]["cash"]
    total_assets = cash + value_holdings
    return render_template("/index.html", stocks=stocks ,name=name, price=usd(price), total_assets=usd(total_assets), symbol=symbol, cash=usd(cash), value=value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("/buy.html")
    else:
        # create variable called 'amount' with qty of stocks times current price.
        stock = request.form.get("symbol").upper()
        quantity = int(request.form.get("shares"))
        # in case the field is empty
        if not stock:
            return apology("must provide stock name", code=406)

        # dictionary of company name, symbol, price. 'acao' means stock in portuguese
        acao = lookup(stock)
        now = datetime.datetime.now()
        current_price = acao["price"]

        #price to be paid for the purchase
        amount = current_price * float(quantity)

        #amount of money available
        username = session["user_id"]
        available = db.execute("SELECT cash FROM users WHERE id = :id", id = username)[0]["cash"]


        # Check if user already owns stocks of the symbol he wishes to buy AND he has enough money to execute the purchase
        if  db.execute("SELECT COUNT(*) FROM portfolio WHERE id = :id and symbol = :symbol", id = username, symbol=stock)[0]["COUNT(*)"] > 0 and available >= amount:
            current = db.execute("SELECT quantity FROM portfolio WHERE id = :id", id = username)[0]["quantity"]
            new_amount = current + quantity
            db.execute("UPDATE portfolio SET quantity = :quantity WHERE id = :id AND symbol = :symbol", id = username, symbol = stock, quantity = new_amount)
            # diminish his cash
            new_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = username)[0]["cash"] - amount
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", id = username, cash = new_cash)
            db.execute("INSERT INTO trade (id, type, price, symbol, shares, date) VALUES (:id,:type,:price,:symbol,:shares,:date)",
                id = username, symbol = stock, shares = quantity, type = "BUY", date = now, price = current_price)
            # PROBLEM Amount of all stocks is becoming the same
            return apology("Done", code=406)

        # If he doesn't own any such stocks yet, but has the money to purchase them
        elif available >= amount:
            #TODO COMPLETE PURCHASE
            db.execute("INSERT INTO portfolio (username, symbol, quantity) VALUES (:username, :symbol, :quantity)", id = username, symbol=stock, quantity=quantity)
            new_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = username)[0]["cash"] - amount
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", id = username, cash = new_cash)
            db.execute("INSERT INTO trade (id, type, price, symbol, shares, date) VALUES (:id,:type,:price,:symbol,:shares,:date)",
                id = username, symbol = stock, shares = quantity, type = "BUY", date = now, price = current_price)
            return apology("Done", code=406)

        else:
            return apology("Not enough money to complete the purchase", code=406)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if method is GET then request page
    if request.method == "GET":
        return render_template("/quote.html")
    else:

    # if method is POST something is being input into the page, which is the stock's symbol being submitted so the user can retrieve the stock's information
        stock = request.form.get("symbol")

        # in case the field is empty
        if not stock:
            return apology("must provide stock name", code=400)

        acao = lookup(stock)
        # in case the symbol can't be found due to mispelling, wrong stock exchange or anything else
        if acao == None:
            return apology("symbol does not exist in the database", code=400)
        else:
            return render_template("/quoted.html", name_stock=acao["name"] , price_stock=acao["price"] , symbol_stock=acao["symbol"])



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # in this method we prevent the user from leaving any field empty
    # Also we require that the "password" field and the "password confirmation" fields are the same
    # The database is verified for the same username being taken

    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        if not name:
            return apology("must provide name", code=400)
        password = request.form.get("password")
        if not password:
            return apology("must provide password", code=400)
        password2 = request.form.get("confirmation")
        if not password2:
            return apology("must provide password confirmation", code=400)
        if password != password2:
            return apology("passwords must match", code=400)

        # Check if the username already exists on the database
        elif db.execute("SELECT COUNT(*) username FROM users WHERE username = :username", username = name)[0]["username"] == 0 :
            hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=name, hash=hash_password)
            return redirect("/", code=200)
        else:
            return apology("username already taken", code=400)



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    username = session["user_id"]
    stock = request.form.get("symbol")
    quantity = (request.form.get("shares"))
    now = datetime.datetime.now()

    if request.method == "GET":
        return render_template("/sell.html")
    else:
        # in case the field is empty request that a name be provided
        if not stock:
            return apology("must provide stock name", code=406)

        # # Check if user has such stock in his portfolio
        if db.execute("SELECT quantity FROM portfolio WHERE id = :id AND symbol = :symbol", id = username, symbol=stock) == None:
             return apology("user does not own this stock", code=400)

        acao = lookup(stock)
        current_price = acao["price"]

        #price to be earned for the sale
        profit = current_price * float(quantity)

        current_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = username)[0]["cash"]
        new_cash = current_cash + profit

        # check if user has stocks to sell
        if not db.execute("SELECT quantity FROM portfolio WHERE id = :id AND symbol = :symbol", id = username, symbol = stock):
             return apology("User doesn't have this stock", code=400)

        shares_owned = db.execute("SELECT quantity FROM portfolio WHERE id = :id AND symbol = :symbol", id = username, symbol = stock)[0]["quantity"]
        # amount of shares owned by the user
        new_share_quantity = shares_owned - int(quantity)

        # check if user has shares enough to sell the quantity requested to be sold by the user
        if(db.execute("SELECT quantity FROM portfolio WHERE id = :id AND symbol = :symbol", id = username, symbol = stock)[0]["quantity"]) < int(quantity):
            return apology("Not enough stocks to sell", code=400)

        # If user wished to sell all shares, delete the entry from the database
        elif shares_owned == int(quantity):
            db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND id = :id", id = username, symbol = stock)
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", id = username, cash = new_cash)

        # If user wishes to sell some but not all his shares
        elif shares_owned > int(quantity):
            db.execute("UPDATE portfolio SET quantity = :quantity WHERE id = :id AND symbol =:symbol", id = username, quantity = new_share_quantity, symbol = stock)
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", id = username, cash = new_cash)
            db.execute("INSERT INTO trade (id, type, price, symbol, shares, date) VALUES (:id,:type,:price,:symbol,:shares,:date)",
                id = username, symbol = stock, shares = quantity, type = "SELL", date = now, price = current_price)

    return apology("SOLD!")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
