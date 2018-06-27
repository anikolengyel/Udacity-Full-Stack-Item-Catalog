from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Category, Item, Base, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# imports for authentication
from flask import session as login_session
import random, string
# created client secret json file
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
from flask import make_response
import requests

app = Flask(__name__, template_folder='static')

# get the client id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connect to Database and create database session
def create_session():
    engine = create_engine('sqlite:///items_catalog.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


# creating a flask app
app = Flask(__name__, template_folder='static')


@app.route('/login')
def showLogin():
    # generating a token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for i in range(32))
    # creating a login session state
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['GET','POST'])
def gConnect():
    # if the token code that the server sent to the client and the token that the client sent
    # to the server, do not match:
    if str(request.args.get('state')) != login_session['state']:
        # make an error message
        response = make_response(json.dumps('invalid state paramater'), 401)
        print(response)
        #specify the content type for the headers
        response.headers['Content-Type'] = 'application/json'
        return response
    # get the code from the server
    request.get_data()
    code = request.data
    # try to exchange the code for the credentials
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        print("client_id: ", oauth_flow.client_id)
        print(oauth_flow.client_secret)
        oauth_flow.redirect_uri='postmessage'
        print('code: ', code)
        credentials = oauth_flow.step2_exchange(code)
        print(credentials)
    except FlowExchangeError:
        response = make_response(json.dumps('We could not upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #1. checking the validity of the access token
    # get the access token from the credentials
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # making a request
    result = json.loads(h.request(url, 'GET')[1])
    #in case of error, stop the process
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 2. verify if the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    # compare the user ids
    # if they don't match, create and error message
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 3. verify if the access token is valid for the application
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match the application."), 401)
        print("Token's client ID does not match the application.")
        # create the response headers and return it
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # store the access token and gplus_id in the login session object
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # get the user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # get the answer in a json format
    data = answer.json()

    # store the user info in a login_session object - username, picture and email
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


    # creating a response for the user
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    # welcome the user
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("The login is done.")
    return output

    # if the application doesn't have the users id, create a new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        createUser(login_session)
    login_session['user_id']=user_id

# reset the login session to disconnect the user
@app.route('/logout')
@app.route('/gdisconnect')
def gDisconnect():
    # get the credentials
    credentials=login_session.get('credentials')
    # if there are not any credentials, the user is not connected
    # send a message
    if credentials is None:
        response=make_response(json.dumps('Curent user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # get the access token
    access_token= credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %access_token
    h = httplib2.Http()
    # make a request with the url
    result = h.request(url, 'GET')[0]

    # if the request is successfull, create the data from the login_session
    if result['status']=='200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # write a response for the user
        response = make_response(json.dumps("We disconnected you."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# create a session to manipulate the database
def create_session():
    engine = create_engine('sqlite:///items_catalog.db')
    Base.metadata.bind = engine

    #binding the session with the database engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

# creating a JSON functionality to give the raw data in JSON format
@app.route('/categories/JSON')
def categoryJson():
    session = create_session()
    # query all the category data
    categories = session.query(Category).all()
    # looping through the category objects, get the data for each column
    return jsonify(category= [i.serialize for i in categories])

# creating a JSON functionality to get the item data in JSON format
@app.route('/category/<int:category_id>/items/JSON')
def categoryItemJson(category_id):
    session = create_session()
    # query and return all the items
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return jsonify(items= [i.serialize for i in items])

@app.route('/main')
# show all the category names and items
def showMainPage():
    session = create_session()
    categories = session.query(Category).all()
    items = session.query(Item).all()
    # if user not logged in, show the public template (without deleting and editing options)
    if 'username' not in login_session:
        return render_template('publicMain.html', categories=categories, items=items)
    return render_template('main.html', categories=categories, items=items)

# if the user click on one category, show the items for the particular cetegory on the main page
@app.route('/main/<int:category_id>/items')
def showItemsForCategory(category_id):
    session = create_session()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id = category.id)
    # if user not logged in, show the public template
    if 'username' not in login_session:
        return render_template('publicShowItemsForCategory.html', categories= categories, items = items, category=category)
    return render_template('mainItemsForCategory.html', categories= categories, items = items, category=category)

# show all the category names
@app.route('/categories')
def showCategories():
    session = create_session()
    categories = session.query(Category).all()
    # if user not logged in, show the public template
    if 'username' not in login_session:
        return render_template('publicCategories.html', categories = categories)
    return render_template('categories.html', categories = categories)

# show all items for a category
@app.route('/category/<int:category_id>/items', methods=['GET'])
# show all the items
def showItems(category_id):
    session = create_session()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id = category.id)
    creator = getUserInfo(category.user_id)
    # if user not logged in or the user is not owner of the category, show the public template
    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('publicItems.html', items = items, category=category)
    return render_template('items.html', items = items, category=category)

# show one  item
@app.route('/category/<int:category_id>/item/<int:item_id>', methods=['GET'])
def showOneItem(category_id, item_id):
    session = create_session()
    category = session.query(Category).filter_by(id=category_id).one()
    oneItem = session.query(Item).filter_by(id=item_id, category_id=category.id).one()
    creator = getUserInfo(category.user_id)
    # if user not logged in or the user is not owner of the category, show the public template
    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('publicOneItem.html', item = oneItem, category=category)
    return render_template('oneItem.html', item = oneItem, category=category)


# create new categories
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    # if the user is not logged in, show the login page
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    categories = session.query(Category).all()
    # after posting, create new data and show the categories template
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(name = request.form['name'], user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
            return redirect(url_for('showCategories'))
    # render the template to create new category
    else:
        return render_template('newCategory.html')

# create new item
@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
    # if the user is not logged in, redirect to the login page
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    category = session.query(Category).filter_by(id=category_id).one()
    # if the user is not the owner of the category, he can't create a new item for it
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to create new item in this category.');}' \
               '</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            newItem = Item(name = request.form['name'], category_id = category.id, user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('showItems', category_id = category.id))
    else:
        return render_template('newItem.html', category = category)

# edit category data
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    # if the user is not owner of the category, send an alert
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this category.');}' \
               '</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category = editedCategory)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    category = session.query(Category).filter_by(id=category_id).one()
    editedItem = session.query(Item).filter_by(id = item_id, category_id=category.id).one()
    # if the logged-in user is not owner of the category, send an alert
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this item." \
               "Create your ow category.');}' \
               '</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['price']:
            editedItem.name = request.form['name']
            editedItem.price = request.form['price']
            session.add(editedItem)
            session.commit()
        return redirect(url_for('showItems', category_id = category.id))

    else:
        return render_template('editItem.html', category = category, item = editedItem)

# delete category
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    deletedItems = session.query(Item).filter_by(category_id=deletedCategory.id).all()
    if deletedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this category.');}' \
               '</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        # deleting all the items for the category too
        for item in deletedItems:
            session.delete(item)
            session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategories.html', category = deletedCategory)

# delete item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    session = create_session()
    category = session.query(Category).filter_by(id=category_id).one()
    deletedItem = session.query(Item).filter_by(id = item_id, category_id=category.id).one()
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this item.');}' \
               '</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('showItems', category_id = category.id))
    else:
        return render_template('deleteItem.html', category = category, item = deletedItem)

# create user function
def createUser(login_session):
    session = create_session()
    user = User(name= login_session['username'], picture=login_session['picture'], email=login_session['email'])
    session.add(user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email'].one())
    return user.id

# get the user object
def getUserInfo(user_id):
    session = create_session()
    user = session.query(User).filter_by(id=user_id).one()
    return user

# get the user's id
def getUserID(user_email):
    session = create_session()
    try:
        user=session.query(User).filter_by(email=user_email)
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'E-VvYUhdCpuva814-tKc5HsZ'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

