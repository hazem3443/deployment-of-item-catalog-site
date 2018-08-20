# import Oauth libraries to handle authntication with facebook and google
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
# import some packages to handle some features in the website
import random
import string
import json
import httplib2
import requests
import os
# import database model
from Database_Setup import Base, Category, CategoryItem, User
# import ORM packages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import Flask package
from flask import session as login_session
from flask import Flask, render_template, url_for, request, redirect
from flask import jsonify, make_response, flash

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']

APPLICATION_NAME = "Restaurant Menu Application"
# Connect to Database
engine = create_engine('postgresql://catalog:hazem123@localhost/catalog')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# User Helper Functions to create and get user data


def createUser(login_session):
    session.close()
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one()
    return user.id

# get user data


def getUserInfo(user_id):
    session.close()
    user = session.query(User).filter_by(id=user_id).one()
    return user

# get user ID from Database


def getUserID(email):
    session.close()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# the main page for the website


@app.route('/')
@app.route('/catalog')
def showCategories():
    session.close()
    # Get all categories
    categories = session.query(Category).all()

    # Get lastest 5 category items added
    categoryItems = session.query(CategoryItem).all()

    return render_template('categories.html', categories=categories,
                           categoryItems=categoryItems)


@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCategory(catalog_id):
    session.close()
    # Get all categories
    categories = session.query(Category).all()

    # Get category
    category = session.query(Category).filter_by(id=catalog_id).first()

    # Get name of category
    categoryName = category.name

    # Get all items of a specific category
    categoryItems = session.query(CategoryItem).filter_by(
        category_id=catalog_id).all()

    # Get count of category items
    categoryItemsCount = session.query(
        CategoryItem).filter_by(category_id=catalog_id).count()

    return render_template('category.html', categories=categories,
                           categoryItems=categoryItems,
                           categoryName=categoryName,
                           categoryItemsCount=categoryItemsCount)


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showCategoryItem(catalog_id, item_id):
    session.close()
    # Get category item
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    # Get creator of item
    creator = getUserInfo(categoryItem.user_id)

    return render_template('categoryItem.html', categoryItem=categoryItem,
                           creator=creator)


@app.route('/catalog/add', methods=['GET', 'POST'])
def addCategoryItem():
    session.close()
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        # TODO: Retain data when errors occure

        if not request.form['name']:
            flash('Please add instrument name')
            return redirect(url_for('addCategoryItem'))

        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('addCategoryItem'))

        # Add category item
        newCategoryItem = CategoryItem(name=request.form['name'],
                                       description=request.form['description'],
                                       category_id=request.form['category'],
                                       user_id=login_session['user_id'])
        session.add(newCategoryItem)
        session.commit()
        flash('%s Item Successfully Created' % (newCategoryItem.name))
        return redirect(url_for('showCategories'))
    else:
        # Get all categories
        categories = session.query(Category).all()

        return render_template('addCategoryItem.html', categories=categories)


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(catalog_id, item_id):
    session.close()
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get category item
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    # Get creator of item
    creator = getUserInfo(categoryItem.user_id)

    # Check if logged in user is creator of category item
    if creator.id != login_session['user_id']:
        return redirect('/login')

    # Get all categories
    categories = session.query(Category).all()

    if request.method == 'POST':
        if request.form['name']:
            categoryItem.name = request.form['name']
        if request.form['description']:
            categoryItem.description = request.form['description']
        if request.form['category']:
            categoryItem.category_id = request.form['category']
        session.add(categoryItem)
        session.commit()
        flash('%s Item Successfully Edited' % (categoryItem.name))
        return redirect(url_for('showCategories'))
    else:
        return render_template('editCategoryItem.html',
                               categories=categories,
                               categoryItem=categoryItem)


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(catalog_id, item_id):
    session.close()
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Get category item
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()

    # Get creator of item
    creator = getUserInfo(categoryItem.user_id)

    # Check if logged in user is creator of category item
    if creator.id != login_session['user_id']:
        return redirect('/login')

    user_id = getUserID(login_session['email'])
    login_session['user_id'] = user_id

    if login_session['user_id'] != categoryItem.user_id:
        form = "<script>function myFunction(){alert('You "
        "are not authorized to delete menu items to this "
        "restaurant. Please create your own restaurant in order to "
        "delete items.');}</script><body onload='myFunction()''>"
        return form
    if request.method == 'POST':
        session.delete(categoryItem)
        session.commit()
        flash('%s Successfully Deleted' % categoryItem.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategoryItem.html',
                               categoryItem=categoryItem)


@app.route('/login')
def login():
    session.close()
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    session.close()
    if login_session['provider'] == 'facebook':
        fbdisconnect()
        del login_session['facebook_id']

    if login_session['provider'] == 'google':
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']

    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
    flash('Successfully Logged Out')
    return redirect(url_for('showCategories'))


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    session.close()
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Gets acces token
    access_token = request.data
    print "access token received %s " % access_token

    # Gets info from fb clients secrets
    app_id = json.loads(open('fb_client_secrets.json',
                        'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json',
                            'r').read())['web']['app_secret']

    url1 = 'https://graph.facebook.com/oauth/access_token?grant_type='
    url2 = 'fb_exchange_token&client_id='
    url3 = '%s&client_secret=%s&' % (app_id, app_secret)
    url4 = 'fb_exchange_token=%s' % (access_token)
    url = url1 + url2 + url3 + url4
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.0/me"

    # strip expire tag from access token
    # token = result.split("&")[0]
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url1 = 'https://graph.facebook.com/v3.0/me?access_token'
    url2 = '=%s&fields=name,id,email' % token
    url = url1 + url2
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    print "data IS HERE " + str(data)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    flash('Successfully Logged in as %s' % (login_session['username']))
    # Store token in login_session in order to logout
    login_session['access_token'] = token

    # Get user picture
    url1 = "https://graph.facebook.com/v3.0/me/picture?"
    url2 = "access_token=%s&redirect=0&height=200&width=200" % token
    url = url1 + url2
    print url
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # See if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful!"


@app.route('/fbdisconnect')
def fbdisconnect():
    session.close()
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']

    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    session.close()
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    flash('Successfully Logged in as %s' % (login_session['username']))
    # See if user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful"


@app.route('/gdisconnect')
def gdisconnect():
    session.close()
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/JSON')
def showCategoriesJSON():
    session.close()
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/catalog/<int:catalog_id>/JSON')
def showCategoryJSON(catalog_id):
    session.close()
    categoryItems = session.query(CategoryItem).filter_by(
        category_id=catalog_id).all()
    return jsonify(categoryItems=[categoryItem.serialize
                   for categoryItem in categoryItems])


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/JSON')
def showCategoryItemJSON(catalog_id, item_id):
    session.close()
    categoryItem = session.query(CategoryItem).filter_by(id=item_id).first()
    return jsonify(categoryItem=[categoryItem.serialize])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
