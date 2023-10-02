from web import app
from flask import render_template


@app.route('/home')
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    title = "About Page"
    return render_template('public/about.html', title=title)


@app.route('/terms&condition')
def terms():
    title = "Terms and Condition"
    return render_template('public/terms&cond.html', title=title)


@app.route('/warrantyPolicy')
def w_policy():
    title = "Warranty Policy"
    return render_template('public/warrantyPol.html', title=title)


@app.route('/privatePolciy')
def p_policy():
    title = "Privacy Policy"
    return render_template('public/privacyPol.html', title=title)


@app.route("/allBrands")
def brand():
    title = "All Brands"
    return render_template('brands/brand.html', title=title)


@app.route("/apple")
def book_A():
    title = "Apple Repair"
    return render_template('brands/book_apple.html', title=title)


@app.route("/xiaomi")
def book_X():
    title = "Xiaomi Repair"
    return render_template('brands/book_xiaomi.html', title=title)


@app.route("/huawei")
def book_H():
    title = "Huawei Repair"
    return render_template('brands/book_huawei.html', title=title)


@app.route("/lenovo")
def book_L():
    title = "Lenovo Repair"
    return render_template('brands/book_lenovo.html', title=title)


@app.route("/moto")
def book_M():
    title = "Motorola Repair"
    return render_template('brands/book_moto.html', title=title)


@app.route("/oneplus")
def book_P():
    title = "One Plus Repair"
    return render_template('brands/book_oneplus.html', title=title)


@app.route("/oppo")
def book_O():
    title = "Oppo Repair"
    return render_template('brands/book_oppo.html', title=title)


@app.route("/samsung")
def book_S():
    title = "Samsung Repair"
    return render_template('brands/book_samsung.html', title=title)


@app.route("/vivo")
def book_V():
    title = "Vivo Repair"
    return render_template('brands/book_vivo.html', title=title)
