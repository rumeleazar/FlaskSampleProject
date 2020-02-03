import sqlite3


#Open database
conn = sqlite3.connect('database.db')

#Create table

conn.execute('''DROP TABLE IF EXISTS user''') 
conn.execute('''DROP TABLE IF EXISTS recipe''') 
conn.execute('''DROP TABLE IF EXISTS readinglist''') 
conn.execute('''DROP TABLE IF EXISTS comments''') 

conn.execute('''CREATE TABLE user(id INTEGER  PRIMARY KEY, username VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, firstname VARCHAR(100) NOT NULL, lastname VARCHAR(100) NOT NULL )''')

conn.execute('''CREATE TABLE recipe(id INTEGER  PRIMARY KEY, dishname VARCHAR(100) NOT NULL, description TEXT NOT NULL, ingredients TEXT NOT NULL, directions TEXT NOT NULL, imagename VARCHAR(100) NOT NULL, author VARCHAR(100) NOT NULL, datetoday VARCHAR(100) NOT NULL) ''')

conn.execute('''CREATE TABLE readinglist(id INTEGER PRIMARY KEY, dishname VARCHAR(100) NOT NULL, author VARCHAR(100) NOT NULL, user VARCHAR(100) NOT NULL)''')

conn.execute('''CREATE TABLE  comments(comments TEXT NOT NULL, id INTEGER NOT NULL, user VARCHAR(100) NOT NULL, datetoday VARCHAR(100) NOT NULL)''')


#Create a user
conn.execute('''INSERT INTO user(username, password, email, firstname, lastname) VALUES("ryanulysses", "qweqwe", "ryanulysses@yahoo.com", "Ryan", "Eleazar")''')
conn.commit()

#Create a list of sample recipes
conn.execute('''INSERT INTO recipe(dishname,description,ingredients,directions,imagename,author,datetoday) VALUES("Garlic Butter Steak" , "This quick-and-easy skillet entree is definitely restaurant-quality and sure to become a staple at your house, too! ", "2 tablespoons butter, softened, divided\r\n1 teaspoon minced fresh parsley\r\n1/2 teaspoon minced garlic\r\n1/4 teaspoon reduced-sodium soy sauce\r\n1 beef flat iron steak or boneless top sirloin steak (3/4 pound)\r\n1/8 teaspoon salt\r\n1/8 teaspoon pepper", "Mix 1 tablespoon butter, parsley, garlic and soy sauce.\r\nSprinkle steak with salt and pepper. In a large skillet, heat remaining butter over medium heat. Add steak; cook until meat reaches desired doneness (for medium-rare, a thermometer should read 135°; medium, 140°; medium-well, 145°), 4-7 minutes per side. Serve with garlic butter.", "GarlicButterSteak.jpg", "ryanulysses" ,"February 03, 2020")''')                  
conn.commit()

conn.execute('''INSERT INTO recipe(dishname,description,ingredients,directions,imagename,author,datetoday) VALUES("Crispy Fried Chicken" , "When it comes to chicken there just isn’t anything more delicious than a juicy, crusty piece of finger-licking good fried chicken. It might seem intimidating to fry your own chicken, but it’s actually pretty straightforward and it puts grocery store and fast food fried chicken to shame.  If you have a thermometer for the oil and a timer, you can produce fail-proof fried chicken.  If you’ve ever wanted to make your own fried chicken, now is the time to try! ", "6 chicken thighs\r\n6 chicken drumsticks\r\n3 cups buttermilk\r\n1/2 cup Buffalo Hot Sauce (optional)\r\n2 teaspoons salt\r\n1/8 teaspoon salt\r\n1 teaspoon pepper","In a large mixing bowl, whisk together buttermilk, hot sauce (optional, for added flavor), salt, and pepper in a mixing bowl. Add in chicken pieces. Cover the bowl with plastic wrap and refrigerate 4 hours.\r\nWhen ready to cook, pour the vegetable oil in a skillet until it is about 3/4 inch deep. Heat to 350 degrees.\r\nPrepare the breading by combining the flour, cornstarch, onion powder, garlic powder, oregano, basil, white pepper, cayenne pepper, paprika, and salt in a gallon sized resealable plastic bag or shallow dish. Mix it thoroughly.\r\nWorking one at a time, remove chicken pieces from buttermilk mixture. Shake it gently to remove the excess. Place it in the breading mix and coat thoroughly. Tap off the excess.\r\nPlace the breaded chicken into the 350 degree oil. Fry 3 or 4 pieces at a time. The chicken will drop the temperature of the oil so keep it as close to 350 degrees as possible. Fry each piece for 14 minutes, turning each piece over about every 2 minutes, until the chicken reaches an internal temperature of 165 degrees F.\r\nRemove from the oil and place on paper towels. Let them rest for at least 10 minutes before serving. ", "FriedChicken.jpg", "ryanulysses" ,"February 03, 2020")''')                  
conn.commit()

conn.execute('''INSERT INTO recipe(dishname,description,ingredients,directions,imagename,author,datetoday) VALUES("Carbonara" , "When you're craving a comfort food, nothing—I repeat, NOTHING—will cure you like creamy carbonara. Here's everything to remember:", "12 oz. spaghetti\r\nKosher salt\r\n3 large eggs\r\n1 c. freshly grated Parmesan\r\n8 slices bacon\r\n2 cloves garlic, minced\r\nFreshly ground black pepper\r\nExtra-virgin olive oil (optional), for garnish\r\nFlaky sea salt (optional), for garnish\r\nFreshly chopped parsley, for garnish","In a large pot of salted boiling water, cook spaghetti according to package directions until al dente. Drain, reserving 1 cup pasta water.\r\nIn a medium bowl, whisk eggs and Parmesan until combined. \r\nMeanwhile, in a large skillet over medium heat, cook bacon until crispy, about 8 minutes. Reserve fat in skillet and transfer slices to a paper towel-lined plate to drain. \r\nTo the same skillet, add garlic and cook until fragrant, about 1 minutes. Add cooked spaghetti and toss until fully coated in bacon fat. Remove from heat. Pour over egg and cheese mixture and stir vigorously until creamy (be careful not to scramble eggs). Add pasta water a couple tablespoons a time to loosen sauce if necessary. \r\nSeason generously with salt and pepper and stir in cooked bacon.\r\nDrizzle with olive oil and garnish with flaky sea salt, Parmesan, and parsley before serving. ", "Carbonara.jpg", "ryanulysses","February 03, 2020")''')
conn.commit()
#Close database cursor
conn.close()