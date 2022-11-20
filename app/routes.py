from flask import render_template, url_for, flash, redirect
from app import app, db

# import all models from models.py
from app.models import *
import ast
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested

# from os.path import join, dirname, realpath
import os
from flask import  render_template, url_for, request, redirect, jsonify, make_response, flash, Response
from flask_cors import CORS, cross_origin
from sqlalchemy import  desc

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


from flask_jwt_extended import create_access_token, create_refresh_token , decode_token
from dateutil.tz import  tzlocal


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

# images folder
IMAGES_FOLDER = 'app/static/images'
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
# icons folder
ICONS_FOLDER = 'app/static/icons'
app.config['ICONS_FOLDER'] = ICONS_FOLDER



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# @socketio.on('order')
@app.route('/get_client_order', methods=["POST", "GET"])
# @cross_origin(origin='*', headers=['Content- Type', 'json'])
def get_client_order():
    if request.method == "POST":
        data = request.get_json()

        # print(data)
        # send(data, broadcast=True)
        client_token = decode_token(data['user'])['sub']
        client = Customer.query.filter_by(username=str(client_token)).first()
        order = data['order']
        DamandeType = data['DamandeType']
        if client:
            order_data = []
            for el in order:
                category_id = el['category']
                food_id = el['id']
                amount = el['amount']
                isMenu = el['isMenu']
                unSelectedRecipes = el['unSelectedRecipes']
                supplement = el['supplement']
                order_data.append(
                    {
                        "category_id": category_id,
                        "food_id": food_id,
                        "amount": amount,
                        "isMenu": isMenu,
                        "unSelectedRecipes": unSelectedRecipes,
                        "supplement": supplement
                    }
                )
                order = Order(
                    customer_id=client.id,
                    order=str(order_data),
                    DamandeType=str(DamandeType)
                )
                db.session.flush()
                db.session.add(order)
                db.session.commit()
                print(order.id)
                notif = Notification(
                    customer_id=client.id,
                    order_id=order.id,
                )
                db.session.add(notif)
                db.session.commit()

            return {"client_id": client.id, "order": order_data, "isConfirmed": True, 'OrderNum': order.id}
        else:
            print({"client_id": client.id, "order": order_data})
            return {"client_id": client.id, "order": order_data}


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registre', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content- Type', 'json'])
def registre_client():
    if request.method == 'POST':
        json = request.get_json()
        try:
            if json['refrech'] == None:
                return jsonify({"access_token": "invalid token"}), 201
            if decode_token(json['refrech']):
                identity = decode_token(json['refrech'])['sub']
                client = Customer.query.filter_by(
                    username=identity).first()
                access_token = create_access_token(identity=identity)
                userData = {
                    "id": client.id,
                    "username": client.username,
                    "Nom": client.Nom,
                    "email": client.email,
                    "Prenom": client.Prenom,
                    "Tel": client.Tel,
                    "last_order": OrderSchema().dump(Order.query.order_by(Order.id.desc()).filter_by(customer_id=client.id).first())

                }
                return jsonify(userData), 200

        except KeyError:
            client = Customer.query.filter_by(
                username=json['username']).first()
            if len(json) == 2:
                if not client:
                    return jsonify({"access_token": "user not regsitred"}), 302

                if client and client.verify_password(json['password']):
                    access_token = create_access_token(
                        identity=client.username)
                    refresh_token = create_refresh_token(
                        identity=client.username)
                    userData = {
                        "id": client.id,
                        "username": client.username,
                        "Nom": client.Nom,
                        "email": client.email,
                        "Prenom": client.Prenom,
                        "Tel": client.Tel,
                        "last_order": OrderSchema().dump(Order.query.order_by(Order.id.desc()).filter_by(customer_id=client.id).first())
                    }
                    return jsonify(access_token=access_token, refresh_token=refresh_token, userData=userData), 200

                else:
                    return jsonify({"access_token": "Unauthorized"}), 401
            else:
                clientMail = Customer.query.filter_by(
                    email=json['email']).first()
                clientPhone = Customer.query.filter_by(
                    email=json['email']).first()

                if client:
                    return jsonify({'access_token': 'use already existe faild'}), 306
                if clientMail:
                    return jsonify({'access_token': 'use already existe faild'}), 300
                if clientPhone:
                    return jsonify({'access_token': 'use already existe faild'}), 300
                else:
                    access_token = create_access_token(
                        identity=json['username'])
                    refresh_token = create_refresh_token(
                        identity=json['username'])

                    client = Customer(
                        username=json['username'],
                        password=json['password'],
                        Nom=json['nom'],
                        Prenom=json['Prenom'],
                        Tel=json['tel'],
                        email=json['email'],
                        adress=json['adress'],
                    )
                    db.session.add(client)
                    db.session.commit()
                    client = Customer.query.filter_by(
                        username=json['username']).first()
                    userData = {
                        "id": client.id,
                        "username": client.username,
                        "Nom": client.Nom,
                        "email": client.email,
                        "Prenom": client.Prenom,
                        "Tel": client.Tel,
                        "adress": client.adress,
                        "last_order": OrderSchema().dump(Order.query.order_by(Order.id.desc()).filter_by(customer_id=client.id).first())

                    }
                    return jsonify(access_token=access_token, refresh_token=refresh_token, userData=userData), 200

    return Response("{'a':'b'}", status=404, mimetype='application/json')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=user).first()
        print('login start', user, password)

        if user and user.verify_password(password):
            print('login succes')
            login_user(user)
            return redirect(url_for('dashbord'))
        else:
            flash("Login ivalido!")

    return render_template('login.html')


@app.route('/')
@login_required
def dashbord():
    dd = Categories.query.order_by(Categories.id).all()
    orders_data = Order.query.all()
    clients_data = Customer.query.all()

    return render_template('index.html', categories_data=dd, orders_data=orders_data, clients_data=clients_data)


@app.context_processor
def inject_categories():
    data = Categories.query.order_by(Categories.id).all()
    return dict(data=data)


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    if request.method == 'GET':
        food_id = request.args.get('get_rate_data')
        # return ""
        TotalRating = len(RatingSchema(many=True).dump(
            Rating.query.filter_by(FoodID=food_id)))

        fiveStars = len(RatingSchema(many=True).dump(
            Rating.query.filter_by(count=5, FoodID=food_id)))

        fourStars = len(RatingSchema(many=True).dump(
            Rating.query.filter_by(count=4, FoodID=food_id)))
        threeStars = len(RatingSchema(many=True).dump(
            Rating.query.filter_by(count=3, FoodID=food_id)))

        twotars = len(RatingSchema(many=True).dump(
            Rating.query.filter_by(count=2, FoodID=food_id)))

        oneStars = len(RatingSchema(many=True).dump(
            Rating.query.filter_by(count=1, FoodID=food_id)))
        # print({
        #     'tatalRating': TotalRating, "rating": [
        #         {'5': fiveStars},
        #         {'4': fourStars},
        #         {'3': threeStars},
        #         {'2': twotars},
        #         {'1': oneStars}]})

        return jsonify({
            'tatalRating': TotalRating, "rating": [
                {'5': fiveStars},
                {'4': fourStars},
                {'3': threeStars},
                {'2': twotars},
                {'1': oneStars}]})
    if request.method == 'POST':
        req = request.get_json()
        try:
            # print(req['user'], req['rating'], req['food_id'])
            # return ''
            getUserRating = Rating.query.filter_by(
                UserId=int(req['user']), FoodID=req['food_id']).first()
            if getUserRating:
                getUserRating.count = req['rating']
                db.session.commit()
            else:
                rat = Rating(count=req['rating'],
                             UserId=req['user'], FoodID=req['food_id'])
                db.session.add(rat)
                db.session.commit()
        except KeyError:
            return jsonify({'info': 'you are not registred'}), 401

    return ""
    # print(RatingSchema().dump(getUserRating))
    #     return RatingSchema().dump(getUserRating)
    # else:
    #     # rat = Rating(
    #     #     count=5,
    #     #     UserId=req['userId']
    #     # )
    #     # db.session.add(rat)
    #     # db.session.commit()
    #     return jsonify({'failed': id})

    # rating = Rating.query.all()

    # rating = RatingSchema(many=True).dump(rating)

    # RatingSchema
    # print(getUserRating)
    # return 'rating'


@app.route('/confirmer_deliver', methods=['POST'])
def confirmerDeliver():
    json = request.get_json()
    id = request.get_json().get('id')
    confirm_order = Order.query.get_or_404(id)

    if request.method == "POST":
        if decode_token(json['refrech']):
            identity = decode_token(json['refrech'])['sub']
            client = Customer.query.filter_by(username=identity).first()
            if (client):
                print(client)
                confirm_order.status = 3
                db.session.commit()
                print(Order.query.get_or_404(id).status)

    return ""


@app.route('/checkOrderStatus/<int:id>')
def checkOrderStatus(id):
    status = Order.query.order_by(
        Order.id.desc()).filter_by(customer_id=id).first()

    return jsonify(OrderSchema().dump(status))


@app.route('/api', methods=['GET', 'POST'])
def api():
    categories = Categories.query.all()
    foods = Food.query.all()
    recipes = Recipe.query.all()
    outputs = CategoriesSchema(many=True).dump(categories)
    output2 = FoodSchema(many=True).dump(foods)
    recipes = RecipeSchema(many=True).dump(recipes)
    newOutputs = []
    for output in outputs:
        _id = output['id']
        _name = output['name']
        img = url_for(
            'static', filename=f"images/{output['img_url']}", _external=True)
        icon = url_for(
            'static', filename=f"icons/{output['icon_url']}", _external=True)
        list = []

        for food_id in output['food_category']:
            for out in output2:
                if food_id == out['id']:
                    with_menu = out['with_menu']

                    out['img_url'] = url_for(
                        'static', filename=f"images/{out['img_url']}", _external=True)
                    # print(out['img_url'])

                    list.append(out)
                    lits2 = []
                    for recip in recipes:
                        for r_id in out['_recipes']:
                            if recip['id'] == int(r_id):
                                print(recip)
                                id = recip['id']
                                name = recip['name']
                                isCheked = recip['isCheked']
                                lits2.append(
                                    {'id': id, 'name': name, 'isCheked': isCheked})
                    out['recipes'] = lits2

        for el in list:
            el.pop('_recipes')

        category = {'id': _id, 'name':  str(_name),
                    'img': str(img), 'icon': str(icon), 'list': list, 'with_menu': with_menu}
        newOutputs.append(category)
    # print(recipes)

    return jsonify(newOutputs)


@app.route('/order_status', methods=['POST', 'GET'])
@login_required
def order_status():
    accept = request.args.get('accept')
    reject = request.args.get('reject')
    if accept:
        # print('accpetd', accept)
        selectedOrder = Order.query.get_or_404(accept)
        selectedOrder.status = 2
        db.session.commit()
        return redirect(url_for('orders', order=accept))
    if reject:
        selectedOrder = Order.query.get_or_404(reject)
        selectedOrder.status = 4
        db.session.commit()
        # print('reject', reject)
        return redirect(url_for('orders', order=reject))


@app.route('/orders')
@login_required
def orders():

    selected_order = request.args.get('order')

    final_data = []
    client_orders = Order.query.order_by(desc(Order.id))  #
    for order in client_orders:
        costumer = Customer.query.filter_by(id=order.customer_id).first()
        detaills = ast.literal_eval(order.order)
        full_order_data = []
        recip_arr = []
        montants = []
        for detaill in detaills:
            supp_arr = []
            totalSupp = 0
            if detaill['supplement'] != None:
                for supp in detaill['supplement']:
                    supp_item = ItemSupplement.query.filter_by(
                        id=supp['item_id']).first()
                    print(supp_item)

                    supp_arr.append(
                        {'supp': supp_item, 'count': supp['count']})
                    totalSupp = totalSupp + \
                        (supp_item.Prix * int(supp['count']))

            montants.append(totalSupp * int(detaill['amount']))

            montants.append(float(Food.query.filter_by(
                id=detaill['food_id']).first().prix) * int(detaill['amount']))
            if detaill['isMenu']:
                montants.append(2 * int(detaill['amount']))

            for recip in detaill['unSelectedRecipes']:
                recip_arr.append(Recipe.query.filter_by(id=recip).first())

            obj = {
                "food": Food.query.filter_by(id=detaill['food_id']).first(),
                "isMenu": detaill['isMenu'],
                "amount": detaill['amount'],
                "unSelectedRecipes": recip_arr,
                "supplement": supp_arr,
                "totalSupp": totalSupp
            }

            full_order_data.append(obj)

        total = 0
        for montant in montants:
            total += float(montant)

        order_data = {
            "order_id": order.id,
            "DamandeType": ast.literal_eval(order.DamandeType),
            "date": order.order_date.astimezone(tzlocal()),
            "client": costumer,
            "adress": costumer.adress,
            "montants": total,
            "status": order.status,
            "full_order_data": full_order_data
        }

        final_data.append(order_data)
    # print(final_data)

    try:
        if selected_order != None:
            for el in final_data:
                try:
                    if el['order_id'] == int(selected_order):
                        # dateconv=utc_to_local_datetime
                        return render_template('client_order.html', order_data=el)
                except ValueError:
                    make_response(render_template("404.html"), 404)

    except TypeError:
        # dateconv=utc_to_local_datetime
        return render_template('orders.html', client_orders=final_data)

    # dateconv=utc_to_local_datetime
    return render_template('orders.html', client_orders=final_data)


@app.route('/clients')
@login_required
def clients():
    clients_data = Customer.query.all()
    return render_template('clients.html', clients_data=clients_data, Order=Order)


@app.route('/edit_sup_status', methods=['POST'])
def edit_sup_status():
    data = request.get_json()
    item = ItemSupplement.query.get_or_404(int(data['id']))
    print(ItemSupplementSchema().dump(item))
    item.isAvailable = data['status']
    db.session.commit()
    return ""


@app.route('/delete_supp/<int:id>', methods=['POST'])
def delete_supp(id):
    item_to_delete = ItemSupplement.query.get_or_404(int(id))
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        redirect('/supplement')
    except:
        print('some error')
    return ""


@app.route('/update_supp/<int:id>', methods=['GET', 'POST'])
@login_required
def update_supp(id):
    item_to_update = ItemSupplement.query.get_or_404(id)
    if request.method == 'POST':
        updated_uploaded_image = request.files['image']

        if updated_uploaded_image.filename != '':
            img_filename = updated_uploaded_image.filename

            updated_img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], f'supp_{secure_filename(updated_uploaded_image.filename)}')
            # set the file path

            updated_uploaded_image.save(updated_img_file_path)
            # save the file
        else:
            img_filename = item_to_update.img_url

        item_to_update.name = request.form['name']
        item_to_update.categoryIDs = request.form['category']
        item_to_update.supplementID = request.form['id_supp']
        item_to_update.img_url = img_filename

        db.session.commit()
        try:
            return redirect(url_for('supplement'))
        except:
            print('some erroe in updating')
    else:
        supplement = Supplement.query.all()
        return render_template('update_supp.html', el=item_to_update, supplement=supplement, Categories=Categories)


@app.route('/supplement', methods=['POST', 'GET'])
@login_required
def supplement():
    if request.method == "POST":
        try:
            supp = request.form['supp'].lower().split('_')[1]
        except:
            supp = request.form['supp'].lower()

        name = request.form['nom']
        Prix = request.form['price']
        categoryIDs = request.form['category']
        maxSelect = request.form['max']

        uploaded_image = request.files['photo']
        if uploaded_image.filename != '':
            img_filename = f"supp_{secure_filename(uploaded_image.filename)}"
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], img_filename)
            # set the file path
            uploaded_image.save(img_file_path)

        # img_url = url_for('static', filename=f'images/{img_filename}', _external=True)
        qery = Supplement.query.filter_by(name=supp).first()
        suppId = int
        if not qery:
            supp = Supplement(name=supp)
            db.session.add(supp)
            db.session.flush()
            suppId = supp.id
        else:
            suppId = qery.id

        item = ItemSupplement(
            name=name,
            Prix=Prix,
            img_url=img_filename,
            supplementID=suppId,
            categoryIDs=categoryIDs,
            max=maxSelect,
        )
        db.session.add(item)
        db.session.commit()

    supplement = Supplement.query.all()
    items_supplement_data = ItemSupplement.query.all()

    selected_supp = request.args.get('supp')
    try:
        # if selected_supp:
        items_supplement_data = ItemSupplement.query.filter_by(
            supplementID=int(selected_supp))
        return render_template('supplement.html', supplement=supplement, items_supplement_data=items_supplement_data, Categories=Categories)
    except:
        # return render_template('supplement.html', supplement=supplement, items_supplement_data=items_supplement_data)

        return render_template('supplement.html', supplement=supplement, items_supplement_data=items_supplement_data, Categories=Categories)


@app.route('/getSuppdata', methods=['GET', 'POST'])
def getSuppdata():
    # if data['id'] != -1:
    #     item = ItemSupplement.query.get_or_404(int(data['id']))
    #     print(ItemSupplementSchema().dump(item))
    #     item.isAvailable = data['status']
    #     db.session.commit()

    suppData = Supplement.query.all()
    itemSuppData = ItemSupplement.query.all()

    suppData = SupplementSchema(many=True).dump(suppData)
    itemSuppData = ItemSupplementSchema(many=True).dump(itemSuppData)

    for el in itemSuppData:
        el['img_url'] = url_for(
            'static', filename=f'images/{el["img_url"]}', _external=True)

    finalData = {'suppData': suppData, 'itemSuppData': itemSuppData}

    # emit('getSuppdata', finalData, broadcast=True)
    return (finalData)


@app.route('/categories', methods=['POST', 'GET'])
@login_required
def showCatgeories():
    if request.method == 'POST':

        uploaded_image = request.files['image']
        uploaded_icon = request.files['icon']

        if uploaded_image.filename != '':
            img_filename = secure_filename(uploaded_image.filename)
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], img_filename)
            # set the file path

            uploaded_image.save(img_file_path)
            # save the file
        if uploaded_icon.filename != '':
            icon_filename = secure_filename(uploaded_icon.filename)
            icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], icon_filename)
            # set the file path

            uploaded_icon.save(icon_file_path)

        try:

            db.session.add(Categories(
                name=request.form['name'],
                # url_for('static', filename=f'images/{img_filename}', _external=True),
                img_url=img_filename,
                # url_for('static', filename=f'icons/{icon_filename}', _external=True)
                icon_url=icon_filename
            ))
            db.session.commit()
            return redirect(url_for('showCatgeories'))
        except:
            print('some error')
    dd = Categories.query.order_by(Categories.id).all()
    return render_template('categories.html', data=dd)


@app.route('/category/<int:id>', methods=['POST', 'GET'])
@login_required
def Category(id):
    item_category = Categories.query.get_or_404(id)

    if request.method == 'POST':
        # handle add item  to category requests
        food_name = request.form['name']
        food_price = request.form['price']
        food_recips = request.form['recip']
        try:
            with_menu = True if request.form['menu'] == 'on' else False
        except KeyError:
            with_menu = False
        uploaded_image = request.files['photo']

        if uploaded_image.filename != '':
            food_img_filename = f'food_{secure_filename(uploaded_image.filename)}'
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], food_img_filename)
            # set the file path
            uploaded_image.save(img_file_path)

        try:
            food = Food(
                name=food_name,
                prix=food_price,
                # url_for('static', filename=f'images/{food_img_filename}', _external=True),
                img_url=food_img_filename,
                rating=3,
                categoryID=item_category.id,
                Categorie=item_category.name,
                recipes=food_recips,
                with_menu=with_menu
            )
            db.session.add(food)
            db.session.flush()
            for recip in food_recips.split(','):
                db.session.add(Recipe(
                    name=recip,
                    isCheked=True,
                    FoodID=food.id,
                ))
            db.session.commit()
            return redirect(url_for('Category', id=id))
        except:
            print('some error')
    else:
        print('...')
        # handle add item  to category requests
    food_db_data = Food.query.filter(Food.categoryID == id)

    return render_template('category.html', item=item_category, food_query=food_db_data)


@app.route('/delete/<int:id>')
@login_required
def Delete(id):
    item_to_delete = Categories.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
    except:
        print('some error')

    return redirect(url_for('showCatgeories'))


@app.route('/delete_article/<int:id>')
@login_required
def DeleteArticle(id):
    item_to_delete = Food.query.get_or_404(id)
    recipes_to_delete = Recipe.query.all()

    # try:

    # except:
    # print('some error')
    db.session.delete(item_to_delete)

    for item in recipes_to_delete:
        if item.FoodID == id:
            db.session.delete(item)

    db.session.commit()
    return redirect(url_for('Category', id = item_to_delete.categoryID ))

@app.route('/update_category/<int:id>', methods=['GET', 'POST'])
@login_required
def Update(id):
    item_to_update = Categories.query.get_or_404(id)

    if request.method == 'POST':
        updated_uploaded_image = request.files['image']
        updated_uploaded_icon = request.files['icon']

        if updated_uploaded_image.filename != '':
            # url_for('static', filename=f'images/category_{secure_filename(updated_uploaded_image.filename)}', _external=True)
            img_filename = f'category_{secure_filename(updated_uploaded_image.filename)}'

            updated_img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], img_filename)
            # set the file path

            updated_uploaded_image.save(updated_img_file_path)
            # save the file
        else:
            img_filename = item_to_update.img_url

        if updated_uploaded_icon.filename != '':
            # url_for('static', filename=f'icons/category_{secure_filename(updated_uploaded_icon.filename)}', _external=True)
            icon_filename = f'category_{secure_filename(updated_uploaded_icon.filename)}'

            updated_icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], icon_filename)
            # set the file path

            updated_uploaded_icon.save(updated_icon_file_path)
        else:
            icon_filename = item_to_update.icon_url

        item_to_update.name = request.form['name']
        item_to_update.icon_url = icon_filename
        item_to_update.img_url = img_filename

        db.session.commit()
        try:
            return redirect(url_for('showCatgeories'))
        except:
            print('some erroe in updating')

    else:

        return render_template('updatecategory.html', el=item_to_update)


@app.route('/update_article/<int:id>', methods=['GET', 'POST'])
@login_required
def UpdateArticle(id):
    item_to_update = Food.query.get_or_404(id)

    if request.method == 'POST':

        if request.form:
            food_name = request.form['name']
            food_price = request.form['price']
            food_recips = request.form['recip']
            try:
                with_menu = True if request.form['menu'] == 'on' else False
            except KeyError:
                with_menu = False

            article_uploaded_image = request.files['photo']

            if article_uploaded_image.filename != '':
                filename = f'food_{secure_filename(article_uploaded_image.filename)}'

                article_img_file_path = os.path.join(
                    app.config['IMAGES_FOLDER'], article_uploaded_image.filename)
                # set the file path
                article_uploaded_image.save(article_img_file_path)
            else:
                filename = item_to_update.img_url
                # save the file

            item_to_update.name = food_name
            item_to_update.prix = food_price
            item_to_update.recipes = food_recips
            item_to_update.img_url = filename
            item_to_update.with_menu = with_menu

            recipe_db__data = Recipe.query.all()

            old_recipes = []
            new_recipes = food_recips.strip().split(',')
            for item in recipe_db__data:
                if item.FoodID == id:
                    old_recipes.append(item)
            edited = []
            for new_recipe, old_recipe in zip(new_recipes, old_recipes):
                dited_recip = Recipe.query.get_or_404(old_recipe.id)
                dited_recip.name = new_recipe.strip()
                edited.append(old_recipe.id)

            # print(edited)
            # print(new_recipes)
            # print(old_recipes)
            # print(id)

            if len(new_recipes) > len(old_recipes):
                new_arr = new_recipes[len(edited):]
                # print("items to add:", new_arr)
                for ell in new_arr:
                    r = Recipe(name=ell.strip(), FoodID=id)
                    db.session.add(r)

            if len(new_recipes) < len(old_recipes):
                new_arr = old_recipes[len(edited):]
                # print("items to remove:", new_arr)
                for item_to_delete in new_arr:
                    db.session.delete(item_to_delete)

            try:
                db.session.commit()
                return redirect(url_for('Category',id=item_to_update.categoryID))
            except:
                print('some erroe in updating')

    else:
        return render_template('update_article.html', el=item_to_update, Recipes=item_to_update.recipes)


@app.route('/notifications', methods=["GET", "POST"])
# @login_required
def MyNotification():

    if request.method == "POST":
        data = request.get_json()
        viewedNotif = data.get('viwedArr')
        RededNotif = data.get('readed_notif_id')
        if viewedNotif:
            for el_id in viewedNotif:
                selected_notif = Notification.query.get_or_404(int(el_id))
                try:
                    selected_notif.isViewed = True
                except AttributeError:
                    print('cc')
        if RededNotif:
            selected_notif = Notification.query.get_or_404(int(RededNotif))
            selected_notif.isReaded = True

        db.session.commit()
        # print(data)
        return jsonify(data)

    if request.method == "GET":
        notif = Notification.query.order_by(desc(Notification.id))
        notif_arr = []
        try:
            for el in notif:
                print(NotificationSchema().dump(el))
                obj = {
                    "id": el.id,
                    "isReaded": el.isReaded,
                    "isViewed": el.isViewed,
                    "order": OrderSchema().dump(el.order),
                    "order_id": el.order.id,
                    "order_date": el.order.order_date,
                    "custumer_nom": el.customer.Nom,
                    "custumer_prenom": el.customer.Prenom,
                }
                notif_arr.append(obj)

            return jsonify(notif_arr)
        except AttributeError:
            return jsonify({"res": "nodata"})


# @socketio.on('message', namespace='/test')
# def test(data):
#     emit('message', 'test', broadcast=True)
#     print("recived")


@ app.errorhandler(404)
@ login_required
def not_found(e):
    """Page not found."""
    return make_response(render_template("404.html"), 404)
