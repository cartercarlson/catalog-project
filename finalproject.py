from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON API endpoint 1
@app.route('restaurants/JSON/')
def showRestaurantsJson(restaurant_id):
	restaurants = session.query(Restaurant).filter_by(id=restaurant_id).all()
	return jsonify(restaurants = restaurants.serialize)


# JSON API endpoint 2
@app.route('restaurants/<int:restaurant_id>/menu/JSON/')
def showMenuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# JSON API endpoint 3
@app.route('restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def MenuItemJson(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem = MenuItem.serialize)


# show all restaurants
# done
@app.route('/')
@app.route('/restaurants/')
def showRestaurants(restaurant_id):
	items = session.query(Restaurant).filter_by(id=restaurant_id).all()
	return render_template('restaurants.html', restaurant_id = restaurant_id, items = items)


# page to make a new restaurant
# done
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant(restaurant_id):
	if request.method =='POST':
		newRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
		session.add(newRestaurant)
		session.commit()
		flash("New Restaurant Created")
		return render_template('newRestaurant.html', restaurant_id = restaurant_id)
	else:
		return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))


# page to edit restaurant 
# done
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedItem = session.query(Restaurant).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
			session.add(editedItem)
			session.commit()
			flash("Restaurant Successfully Edited")
		return render_template('editRestaurant.html', restaurant_id = restaurant_id)
	else:
		return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))


# page to delete restaurant
# done
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	itemToDelete = session.query(Restaurant).filter_by(id=menu_id).one()
	if request.method = 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Menu Item Successfully Deleted (restaurants.html)")
		return render_template('deleteRestaurant.html', restaurant_id = restaurant_id)
	else:
		return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))


# page of menu at restaurant (restaurant_id)
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(id=restaurant_id).all()
	return render_template('menu.html', restaurant_id = restaurant_id, menu_id = menu_id, items = items)


# page to make a new menu at restaurant (restaurant_id)
# done
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem():
	if request.method =='POST':
		newItem = MenuItem(name = request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'],restaurant_id = restaurant_id)
		return render_template('newMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id)
	else:
		return redirect(url_for('showMenu', restaurant_id = restaurant_id, menu_id = menu_id))


# page to edit item (item_id) at restaurant (restaurant_id)
# done
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
			session.add(editedItem)
			session.commit()
			flash("Menu Item Successfully Edited (menu.html)")
		return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id)
	else:
		return redirect(url_for('showMenu', restaurant_id = restaurant_id, menu_id = menu_id))


# page to delete item (item_id) at restaurant (restaurant_id)
# done
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method = 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Menu Item Successfully Deleted (restaurants.html)")
		return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id)
	else:
		return redirect(url_for('showMenu', restaurant_id = restaurant_id, menu_id = menu_id))





if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)