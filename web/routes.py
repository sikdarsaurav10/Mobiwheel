from flask import jsonify, request, render_template, redirect, url_for
from web import app, db
from web.model import People, Phone, Phonephotos
from web.utils import send_mail


@app.route('/user-info', methods=['GET', 'POST'])
def userData():
    try:
        if request.is_json and request.method == 'POST':
            resp = request.get_json()
            brand = resp['Brand']
            model = resp['Model']
            name = resp['Name']
            prob = resp['Problem']
            num = resp['Contact_no']
            ls = [brand, model, name, prob, num]
            try:
                user_info_main = People(
                    brand=brand,
                    md=model,
                    name=name,
                    problem=prob,
                    number=num)

                db.session.add(user_info_main)
                db.session.commit()
                send_mail(ls)
                return jsonify(name=name)
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify(msg='we cannot save the details')
    except Exception as e:
        print(e)


@app.route("/submit_brand", methods=['POST', 'GET'])
def info_2():
    try:
        if request.is_json and request.method == 'POST':
            resp = request.get_json()
            brand = resp['Brand']
            model = resp['Model']
            name = resp['Name']
            num = resp['Contact_no']
            ls = [brand, model, name, num]
            try:
                c_brand = People(
                    brand=brand,
                    md=model,
                    name=name,
                    number=num)

                db.session.add(c_brand)
                db.session.commit()
                send_mail(ls)
                return jsonify(name=name)
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify(msg='we cannot save the details')

    except Exception as e:
        print(e)


@app.route('/phone_view')
def viewPhone():
    public_id = request.args.get('public_id')
    phone = Phone.query.filter_by(public_id=public_id).first()
    images = Phonephotos.query.filter_by(author=phone)

    output = []
    for i in images:
        output.append(i.phone_img)

    brand = phone.brand
    model = phone.model
    ram = phone.ram
    price = phone.price
    descp = phone.descp

    return render_template('old_phone/phoneView.html',
                           brand=brand,
                           model=model,
                           ram=ram,
                           price=price,
                           description=descp,
                           imgs=output)


# @app.route('/filter', )
# def getBrands():
#     phones = Phone.query.all()

#     output = []
#     for phone in phones:
#         brand = phone.brand
#         if brand not in output:
#             output.append(brand)

#     return jsonify(output)


@app.route("/buy_phone/filter", methods=['POST'])
def filterPhone():
    # title = "Buy Phone"
    # page = request.args.get('page', 1, type=int)

    if not request.form.get("brand", None):
        if not request.form.get("ram", None):
            price = request.form['price']

            return redirect(url_for('buyPhone', price=price))

        elif not request.form.get("price", None):
            ram = request.form['ram']

            return redirect(url_for('buyPhone', ram=ram))

        else:
            ram = request.form['ram']
            price = request.form['price']

            return redirect(url_for('buyPhone', ram=ram, price=price))

    elif not request.form.get("ram", None):
        if not request.form.get("brand", None):
            price = request.form['price']

            return redirect(url_for('buyPhone', price=price))

        elif not request.form.get("price", None):
            brand = request.form['brand']

            return redirect(url_for('buyPhone', brand=brand))

        else:
            brand = request.form['brand']
            price = request.form['price']

            return redirect(url_for('buyPhone', brand=brand, price=price))

    elif not request.form.get("price", None):
        if not request.form.get("ram", None):
            brand = request.form['brand']

            return redirect(url_for('buyPhone', brand=brand))

        elif not request.form.get("brand", None):
            ram = request.form['ram']

            return redirect(url_for('buyPhone', ram=ram))

        else:
            brand = request.form['brand']
            ram = request.form['ram']

            return redirect(url_for('buyPhone', brand=brand, ram=ram))

    else:
        brand = request.form['brand']
        ram = request.form['ram']
        price = request.form['price']

        return redirect(url_for('buyPhone', brand=brand, ram=ram, price=price))


# @app.route("/buy_phone/filter")
# def dummy():
#     data = request.args
#     if 'brand' not in data:
#         if 'ram' not in data:
#             return '<h1>{{ data["price"] }}</h1>'
#         elif 'price' not in data:
#             return '<h1>{{ data["ram"] }}</h1>'
#         else:
#             return '<h1>{{ data["ram"] }}{{ data["price"] }}</h1>'

#     elif 'ram' not in data:
#         if 'brand' not in data:
#             return '<h1>{{ data["price"] }}</h1>'
#         elif 'price' not in data:
#             return '<h1>{{ data["brand"] }}</h1>'
#         else:
#             return '<h1>{{ data["brand"] }}{{ data["price"] }}</h1>'

#     elif 'price' not in data:
#         if 'ram' not in data:
#             return '<h1>{{ data["brand"] }}</h1>'
#         elif 'brand' not in data:
#             return '<h1>{{ data["ram"] }}</h1>'
#         else:
#             return '<h1>{{ data["brand"] }}{{ data["ram"] }}</h1>'

#     else:
#         return '<h1>{{ data["brand"] }}{{ data["ram"] }}\
#         {{ data["price"] }}</h1>'
    # phones = Phone.query.order_by(Phone.date_posted.desc())\
    #     .paginate(page=page, per_page=12)
    # return render_template('old_phone/buyPhone_home.html', title=title,
    #                        phones=phones)

@app.route("/buy_phone")
def buyPhone():
    title = "Buy Phone"

    brands = Phone.query.all()

    output = []
    for phone in brands:
        brand = phone.brand
        if brand not in output:
            output.append(brand)

    if request.args:
        data = request.args
        if 'brand' not in data:
            if 'ram' not in data:
                page = request.args.get('page', 1, type=int)

                if int(data['price']) < 5001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price <= 5000)\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 5001 < int(data['price']) < 10001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .filter(Phone.price.between(5000, 10000))\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 10001 < int(data['price']) < 15001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .filter(Phone.price.between(10000, 15000))\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 15001 < int(data['price']) < 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .filter(Phone.price.between(15000, 20999))\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if int(data['price']) > 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price > 20999)\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

            elif 'price' not in data:
                page = request.args.get('page', 1, type=int)
                phones = Phone.query.order_by(Phone.date_posted.desc())\
                    .filter_by(ram=data["ram"])\
                    .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones, output=output)

            else:
                page = request.args.get('page', 1, type=int)

                if int(data['price']) < 5001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price <= 5000)\
                            .filter_by(ram=data["ram"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 5001 < int(data['price']) < 10001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price.between(5000, 10000))\
                            .filter_by(ram=data["ram"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 10001 < int(data['price']) < 15001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price.between(10000, 15000))\
                            .filter_by(ram=data["ram"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 15001 < int(data['price']) < 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price.between(15000, 20999))\
                            .filter_by(ram=data["ram"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if int(data['price']) > 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price > 20999)\
                            .filter_by(ram=data["ram"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

        elif 'ram' not in data:
            if 'brand' not in data:
                page = request.args.get('page', 1, type=int)

                if int(data['price']) < 5001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price <= 5000)\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 5001 < int(data['price']) < 10001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .filter(Phone.price.between(5000, 10000))\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 10001 < int(data['price']) < 15001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .filter(Phone.price.between(10000, 15000))\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 15001 < int(data['price']) < 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .filter(Phone.price.between(15000, 20999))\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if int(data['price']) > 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price > 20999)\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

            elif 'price' not in data:
                page = request.args.get('page', 1, type=int)
                phones = Phone.query.order_by(Phone.date_posted.desc())\
                    .filter_by(brand=data["brand"])\
                    .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones, output=output)

            else:
                page = request.args.get('page', 1, type=int)

                if int(data['price']) < 5001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price <= 5000)\
                            .filter_by(brand=data["brand"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 5001 < int(data['price']) < 10001:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price.between(5000, 10000))\
                            .filter_by(brand=data["brand"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 10001 < int(data['price']) < 15001:
                    for phone in brands:
                        phones_prices = Phone.query.\
                            order_by(Phone.date_posted.desc())\
                            .filter(Phone.price.between(10000, 15000))\
                            .filter_by(brand=data["brand"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if 15001 < int(data['price']) < 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price.between(15000, 20999))\
                            .filter_by(brand=data["brand"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

                if int(data['price']) > 20999:
                    for phone in brands:
                        phones_prices = Phone.query\
                            .order_by(Phone.date_posted.desc())\
                            .filter(Phone.price > 20999)\
                            .filter_by(brand=data["brand"])\
                            .paginate(page=page, per_page=12)

                    return render_template('old_phone/buyPhone_home.html',
                                           title=title,
                                           phones=phones_prices, output=output)

        elif 'price' not in data:
            if 'ram' not in data:
                page = request.args.get('page', 1, type=int)
                phones = Phone.query.order_by(Phone.date_posted.desc())\
                    .filter_by(brand=data["brand"])\
                    .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones, output=output)

            elif 'brand' not in data:
                page = request.args.get('page', 1, type=int)
                phones = Phone.query.order_by(Phone.date_posted.desc())\
                    .filter_by(ram=data["ram"])\
                    .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones, output=output)

            else:
                page = request.args.get('page', 1, type=int)
                phones = Phone.query.order_by(Phone.date_posted.desc())\
                    .filter_by(brand=data["brand"], ram=data["ram"])\
                    .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones, output=output)

        else:
            page = request.args.get('page', 1, type=int)

            if int(data['price']) < 5001:
                for phone in brands:
                    phones_prices = Phone.query\
                        .order_by(Phone.date_posted.desc())\
                        .filter(Phone.price <= 5000)\
                        .filter_by(brand=data["brand"],
                                   ram=data["ram"])\
                        .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones_prices, output=output)

            if 5001 < int(data['price']) < 10001:
                for phone in brands:
                    phones_prices = Phone.query\
                        .order_by(Phone.date_posted.desc())\
                        .filter(Phone.price.between(5000, 10000))\
                        .filter_by(brand=data["brand"],
                                   ram=data["ram"])\
                        .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones_prices, output=output)

            if 10001 < int(data['price']) < 15001:
                for phone in brands:
                    phones_prices = Phone.query\
                        .order_by(Phone.date_posted.desc())\
                        .filter(Phone.price.between(10000, 15000))\
                        .filter_by(brand=data["brand"],
                                   ram=data["ram"])\
                        .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones_prices, output=output)

            if 15001 < int(data['price']) < 20999:
                for phone in brands:
                    phones_prices = Phone.query\
                        .order_by(Phone.date_posted.desc())\
                        .filter(Phone.price.between(15000, 20999))\
                        .filter_by(brand=data["brand"],
                                   ram=data["ram"])\
                        .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones_prices, output=output)

            if int(data['price']) > 20999:
                for phone in brands:
                    phones_prices = Phone.query\
                        .order_by(Phone.date_posted.desc())\
                        .filter(Phone.price > 20999)\
                        .filter_by(brand=data["brand"],
                                   ram=data["ram"])\
                        .paginate(page=page, per_page=12)

                return render_template('old_phone/buyPhone_home.html',
                                       title=title,
                                       phones=phones_prices, output=output)

    page = request.args.get('page', 1, type=int)
    phones = Phone.query.order_by(Phone.date_posted.desc())\
        .paginate(page=page, per_page=12)

    return render_template('old_phone/buyPhone_home.html', title=title,
                           phones=phones, output=output)
