from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.
session = DBSession()

restaurants = ['Urban Burger',
			   'Super Stir Fry',
			   'Panda Garden',
			   'Thyme for that Vegetarian Cuisine',
			   "Tony\'s Bistro"]

menu_items = [
	[ # Urban Burger menu
		['Veggie Burger', 'Juicy grilled veggie patty w/ tomato, mayo, and lettuce', '$7.50', 'Entree'],
		['French Fries', 'with garlic and parmesan', '$2.99', 'Appetizer'],
		['Chicken Burger', 'Juicy grilled chicken patty w/ tomato, mayo, and lettuce', '$8.00','Entree'],
		['Chocolate Cake', 'fresh baked and served with ice cream', '$3.99', 'Dessert'],
		['Soda', 'Your choice of Coke products', '$1.49', 'Beverage']
	],
	[ # Super Stir Fry menu
		['Chicken Stir Fry', 'With your choice of noodles, veggies, and sauces', '$7.99', 'Entree'],
		['Peking Duck', 'A famous duck dish from Beijing that has been prepared since the imperial era', '$25', 'Entree'],
		['Beef Noodle Soup', 'A Chinese noodle soup made of stewed or braised beef, beef broth, veggies, and Chinese noodles', '$14', 'Entree'],
		['Iced Tea', 'with Lemon', '$0.99', 'Beverage']
	],
	[ # Panda Garden menu
		['Pho', 'A Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, herbs, and meat', '$8.99', 'Entree'],
		['Stinky Tofu', 'Taiwanese dish, deep fried fermented tofu served with pickled cabbage', '$6.99', 'Entree']
		['Chinese Dumplings', 'A common Chinese dumpling with minced meat and finely chopped vegetables wrapped into a piece of dough skin', '$5.99', 'Appetizer'],
		['Mochi balls', 'A small, round confection consisting of a soft, pounded sticky rice dumpling formed around an ice cream filling', '$4.99', 'Dessert']
	],
	[ # Time for that Vegetarian Cuisine menu
		['Tres Leches Cake', 'Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries', '$2.99', 'Desserst'],
		['Mushroom risotto', 'Portabello mushrooms in a creamy risotto', '$5.99', 'Entree'],
		['Cauliflower Manchurian', 'Golden fried cauliflower florets in a mildly spiced soya, garlic sauce cooked with fresh cilantro, celery, chilies, ginger, and green onions', '$7.99', 'Appetizer'],
		['Aloo Gobi Burrito', 'Burrito filled with rice, garbanzo beans, curry sauce, potatoes, fried cauliflower (gobi) and chutney', '$6.99', 'Entree'],
		['Honey Boba Shaved Snow', 'Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and mochi', '$4.50', 'Dessert']
	],
	[ # Tony's Bistro menu
		['Shellfish Tower', 'Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower', '$14.95', 'Entree'],
		['Chicken and Rice', 'Chicken... and rice', '$8.95', 'Entree'],
		['Moms Spaghetti', 'Hes nervous, but on the surface he looks calm and ready', '$6.95', 'Entree'],
		['Choc Full O Mint ice cream', 'Milk, cream, salt, and liquid nitrogen magic', '$3.99', 'Dessert']
	]
]

for i in range(len(restaurants)):
	session.add(Restaurant(name=restaurants[i]))
	session.commit()

	for item in menu_items[i]:
		session.add(MenuItem(
			name=item[0],
			description=item[1],
			price=item[2],
			course=item[3],
			restauraunt=restaurants[i]
		))
		session.commit()
