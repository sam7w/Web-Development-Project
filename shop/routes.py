import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Brand, Watch, User
from shop.forms import RegistrationForm, LoginForm, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    watches = Watch.query.all()
    return render_template('home.html', watches=watches, title='Watches')

@app.route("/price")
def price():
    watches = Watch.query.order_by('price')
    return render_template('home.html', watches=watches, title='Watches')

@app.route("/watch_size")
def watch_size():
    watches = Watch.query.order_by('watch_size')
    return render_template('home.html', watches=watches, title='Watches')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/watch/<int:watch_id>")
def watch(watch_id):
	watch = Watch.query.get_or_404(watch_id)
	return render_template('watch.html', title = watch.title, watch = watch)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data, first_name=form.first_name.data, last_name=form.last_name.data, address=form.address.data)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created. You can now log in.')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/add_to_cart/<int:watch_id>")
def add_to_cart(watch_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(watch_id)
    flash(  "The watch has been added to your shopping cart!")
    return redirect("/cart")

@app.route("/wishlist_to_cart/<int:watch_id>", methods=['GET', 'POST'])
def wishlist_to_cart(watch_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(watch_id)
    session.modified=True
    session["wishlist"].remove(watch_id)
    flash(  "The watch has been added to your shopping cart!")
    return redirect("/cart")

@app.route("/add_to_wishlist/<int:watch_id>")
def add_to_wishlist(watch_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].append(watch_id)
    flash("The watch has been added to your wishlist.")
    return redirect("/wishlist")

@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
    if "cart" not in session:
        flash('There is nothing in your cart.')
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            watch = Watch.query.get_or_404(item)

            total_price += watch.price
            if watch.id in cart:
                cart[watch.id]["quantity"] += 1
            else:
                cart[watch.id] = {"quantity":1, "title": watch.title, "price":watch.price}
            total_quantity = sum(item['quantity'] for item in cart.values())


        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_quantity = total_quantity)

    return render_template('cart.html')

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
    if "wishlist" not in session:
        return render_template("wishlist.html")
    else:
        items = session["wishlist"]
        wishlist = {}
        total_wishlist_quantity = 0
        for item in items:
            watch=Watch.query.get_or_404(item)
            if watch.id in wishlist:
                wishlist[watch.id]["wishlist_quantity"] += 1
            else:
                wishlist[watch.id] = {"wishlist_quantity":1, "title":watch.title, "price":watch.price}
            total_wishlist_quantity = sum(item['wishlist_quantity'] for item in wishlist.values())
        return render_template("wishlist.html", title="Wishlist", display_wishlist = wishlist, total__wishlist_quantity=total_wishlist_quantity)
    return render_template('wishlist.html')

@app.route("/delete_watch/<int:watch_id>", methods=['GET', 'POST'])
def delete_watch(watch_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].remove(watch_id)

    flash("The watch has been removed from your shopping cart!")

    session.modified = True

    return redirect("/cart")

@app.route("/delete_wishlist_watch/<int:watch_id>", methods=['GET', 'POST'])
def delete_wishlist_watch(watch_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(watch_id)
    flash("The watch has been removed from your wishlist.")
    session.modified = True
    return redirect("/wishlist")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
            flash('Thank you for your purchase')
            session["cart"] = []
            return redirect(url_for('home'))
    return render_template('checkout.html', title='Checkout', form=form)