from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random
import string
import httplib2
import json
import requests


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu App"

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
	if 'username' not in login_session:
		return render_template('publicRestaurants.html', restaurants=restaurants)
	else:
		return render_template('restaurants.html', restaurants=restaurants)


# Create a new restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
	if 'username' not in login_session:
		return redirect('/login')

	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'], user_id=login_session['user_id'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')


# Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedRestaurant.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"

	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

	if request.method == 'POST':
		editedRestaurant.name = request.form['name']
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html',restaurant=editedRestaurant)


# Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/',
		   methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if 'username' not in login_session:
		return redirect('/login')

	if restaurantToDelete.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"

	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)


# Show restaurant menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	creator = getUserInfo(restaurant.user_id)

	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicMenu.html', items=items, restaurant=restaurant, creator=creator)
	else:
		return render_template('menu.html', restaurant=restaurant, items=items, creator=creator)


# Create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if 'username' not in login_session:
		return redirect('/login')

	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if login_session['user_id'] != restaurant.user_id:
		return "<script>function myFunction() {alert('You are not authorized to add menu items to this restaurant. Please create your own restaurant in order to add items.');}</script><body onload='myFunction()'>"

	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],
						   description=request.form['description'],
						   price=request.form['price'],
						   course=request.form['course'],
						   restaurant_id=restaurant_id)

		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	if 'username' not in login_session:
		return redirect('/login')

	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

	if login_session['user_id'] != restaurant.user_id:
		return "<script>function myFunction() {alert('You are not authorized to edit menu items to this restaurant. Please create your own restaurant in order to edit items.');}</script><body onload='myFunction()'>"

	if request.method == 'POST':
		editedItem.name = request.form['name']
		editedItem.description = request.form['description']
		editedItem.price = request.form['price']
		editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	if 'username' not in login_session:
		return redirect('/login')

	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()

	if login_session['user_id'] != restaurant.user_id:
		return "<script>function myFunction() {alert('You are not authorized to delete menu items to this restaurant. Please create your own restaurant in order to delete items.');}</script><body onload='myFunction()'>"

	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

	else:
		return render_template('deleteMenuItem.html', item=itemToDelete)


# API endpoint 1
@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants=[r.serialize for r in restaurants])


# API endpoint 2
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJson(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


# API endpoint 3
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJson(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)


# User Helper Functions
def createUser(login_session):
	newUser = User(name=login_session['username'],
				   email=login_session['email'],
				   picture=login_session['picture'])

	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id


def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user


def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return


# Create anti-forgery state token
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


# Connect to Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	code = request.data

	try:
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)

	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = json.loads(answer.text)

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	login_session['provider'] = 'google'

	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = '<h1>Welcome, ' + login_session['username'] + '!</h1>'
	output += '<img src="' + login_session['picture'] + '" style="width: 300px; height: 300px;border-radius: 150px;">'
	return output


# Disconnect from Google
@app.route('/gdisconnect')
def gdisconnect():
	access_token = login_session.get('access_token')
	if access_token is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		# Reset the user's session
		# del login_session['access_token']
		# del login_session['gplus_id']
		# del login_session['username']
		# del login_session['email']
		# del login_session['picture']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
			gdisconnect()
			del login_session['gplus_id']
			del login_session['access_token']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		return redirect(url_for('showRestaurants'))
	else:
		return redirect(url_for('showRestaurants'))


if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'password'
	app.run(host='0.0.0.0', port=5000)
