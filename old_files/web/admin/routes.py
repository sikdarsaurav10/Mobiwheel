from datetime import timedelta
from flask import Blueprint, render_template, request, redirect,\
    url_for, flash, session
from web import db
from web.model import People, Phone, Phonephotos, Admin
from web.utils import save_pic, generate_phone_id, save_title_pic
from flask_login import login_user, logout_user, login_required, current_user


adminLog = Blueprint('adminLog', __name__)


@adminLog.route('/', methods=['GET', 'POST'])
def index_admin():
    if current_user.is_authenticated:
        return redirect(url_for('adminLog.a_home'))
    if request.method == 'POST':
        username = request.form["username"]
        pwd = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and pwd == 'admin':
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('adminLog.a_home'))
        else:
            flash('Not authorised!!', 'danger')
            return redirect(url_for('adminLog.index_admin'))
    return render_template('admin/logIn.html')


@adminLog.route('/home')
@login_required
def a_home():
    title = "Admin Panel"
    return render_template('admin/admin_home.html', title=title)


@adminLog.route('/database')
@login_required
def a_base():
    title = "Admin Panel Database"
    return render_template('admin/admin_data.html',
                           title=title,
                           people=People.query.all())


@adminLog.route('/database/new', methods=['GET', 'POST'])
@login_required
def a_baseCreate():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        name = request.form['full_name']
        prob = request.form['problem']
        num = request.form['contact']

        user_info_main = People(
                        brand=brand,
                        md=model,
                        name=name,
                        problem=prob,
                        number=num)

        db.session.add(user_info_main)
        db.session.commit()

        return render_template('admin/create_user.html')

    return render_template('admin/create_user.html')


@adminLog.route('/database/remove')
@login_required
def remove_user():
    user_id = request.args.get('user_id')
    data_user = People.query.filter_by(id=user_id).first_or_404()

    db.session.delete(data_user)
    db.session.commit()

    return redirect(url_for('adminLog.a_base'))


@adminLog.route('/phoneData')
@login_required
def p_base():
    title = "Phone Database"
    return render_template('admin/phone_data.html',
                           title=title,
                           phones=Phone.query.all())


@adminLog.route('/upload')
@login_required
def a_upload():
    page = request.args.get('next')
    if page:
        n = '/admin'+page
        return redirect(n)
    return render_template('admin/admin_upload.html')


@adminLog.route('/upload/new', methods=['POST'])
@login_required
def phoneUpload():
    title_img = request.files['titleImg']
    img_main = save_title_pic(title_img)
    photos = request.files.getlist('file')
    img_output = []
    for i in photos:
        img = save_pic(i)
        img_output.append(img)

    brand = request.form['brand']
    model = request.form['model']
    ram = request.form['ram']
    price = request.form['price']
    descp = request.form['description']

    public_id = generate_phone_id(brand, model)
    new_item = Phone(public_id=public_id,
                     brand=brand,
                     model=model,
                     ram=ram,
                     price=price,
                     descp=descp,
                     title_img=img_main)

    db.session.add(new_item)

    for i in img_output:
        files = Phonephotos(phone_img=i, phone_id=public_id)
        db.session.add(files)

    db.session.commit()

    return render_template('admin/admin_upload.html')


@adminLog.route('/upload_database/remove')
@login_required
def remove_upload():
    public_id = request.args.get('public_id')
    phone = Phone.query.filter_by(public_id=public_id).first()

    db.session.delete(phone)
    db.session.commit()

    return redirect(url_for('adminLog.p_base'))


@adminLog.route('/upload_database/update')
@login_required
def edit_upload():
    public_id = request.args.get('public_id')
    phone = Phone.query.filter_by(public_id=public_id).first()

    brand = phone.brand
    model = phone.model
    ram = phone.ram
    price = phone.price
    descp = phone.descp

    return render_template('admin/update_upload.html',
                           public_id=public_id,
                           brand=brand,
                           model=model,
                           ram=ram,
                           price=price,
                           descp=descp)


@adminLog.route('/upload_database/update/new', methods=['POST'])
@login_required
def edit_uploadNew():
    public_id = request.args.get('public_id')
    phone = Phone.query.filter_by(public_id=public_id).first()

    phone.brand = request.form['brand']
    phone.model = request.form['model']
    phone.ram = request.form['ram']
    phone.price = request.form['price']
    phone.descp = request.form['description']

    db.session.commit()

    return redirect(url_for('adminLog.p_base'))


@adminLog.before_request
def before_request():
    session.permanent = True
    adminLog.permanent_session_lifetime = timedelta(minutes=30)


@adminLog.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('adminLog.index_admin'))
