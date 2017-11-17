from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app=Flask(__name__)

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine

DBSession=sessionmaker(bind=engine)
session=DBSession()
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Show all restaurants
@app.route('/')
app.route('/restaurants/')
def showRestaurants():
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=sesion.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return render_template('restaurants.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


# Create a new restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant(restaurant_id):
	if request.method=='POST':
		newRestaurant=Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("Created Restaurant '%s'" % newRestaurant)
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')


# Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedItem=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		if request.form['name']:
			editedItem.name=request.form['name']
			session.add(editedItem)
			session.commit()
			flash("Successfully Edited %s" % editedItem.name)
		return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('editRestaurant.html', restaurant_id=restaurant_id, item=editedItem)


# Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	itemToDelete=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Successfully Deleted %s" % itemToDelete.name)
		return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, item=itemToDelete)


# Show menu of restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	return render_template('menu.html', restaurant=restaurant, items=items)


# Create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method=='POST':
		newItem=MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New Menu %s Item Successfully Created!" % (newItem.name))
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method=='POST':
		if request.form['name']:
			editedItem.name=request.form['name']
			session.add(editedItem)
			session.commit()
			flash("Successfully Edited %s" %editedItem)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id, menu_id=menu_id))
	else:
		return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	itemToDelete=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method=='POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Menu Item Successfully Deleted (restaurants.html)")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id, menu_id=menu_id))
	else:
		return render_template('deleteMenuItem.html', item=itemToDelete)


# Making an API Endpoint (GET Request)
@app.route('restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# ADD API endpoint here
@app.route('restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJson(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)















if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9000)