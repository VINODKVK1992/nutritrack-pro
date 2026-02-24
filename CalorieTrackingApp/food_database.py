"""
Food Database with Nutrition Information
Contains common Indian, US, and international foods with their nutritional values
"""

FOOD_DATABASE = [
    # PROTEINS
    {"name": "Chicken Breast (100g)", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "image": "🍗"},
    {"name": "Chicken Thigh (100g)", "calories": 209, "protein": 26, "carbs": 0, "fat": 11, "image": "🍗"},
    {"name": "Egg (1 medium)", "calories": 78, "protein": 6.3, "carbs": 0.6, "fat": 5.3, "image": "🥚"},
    {"name": "Paneer (100g)", "calories": 265, "protein": 20, "carbs": 3.2, "fat": 20, "image": "🧀"},
    {"name": "Tofu (100g)", "calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "image": "🟫"},
    {"name": "Fish (Salmon, 100g)", "calories": 208, "protein": 20, "carbs": 0, "fat": 13, "image": "🐟"},
    {"name": "Fish (Tilapia, 100g)", "calories": 96, "protein": 20, "carbs": 0, "fat": 1, "image": "🐟"},
    {"name": "Milk (250ml)", "calories": 149, "protein": 7.7, "carbs": 11.7, "fat": 7.7, "image": "🥛"},
    {"name": "Curd/Yogurt (100g)", "calories": 59, "protein": 10, "carbs": 3.3, "fat": 0.2, "image": "🥛"},
    {"name": "Cottage Cheese (100g)", "calories": 98, "protein": 11, "carbs": 3.4, "fat": 4.3, "image": "🧀"},
    {"name": "Chickpeas (100g cooked)", "calories": 134, "protein": 8.9, "carbs": 23, "fat": 2.1, "image": "🫘"},
    {"name": "Lentils (100g cooked)", "calories": 116, "protein": 9.0, "carbs": 20, "fat": 0.4, "image": "🫘"},
    {"name": "Ground Beef (100g)", "calories": 250, "protein": 26, "carbs": 0, "fat": 15, "image": "🥩"},
    {"name": "Steak (100g)", "calories": 271, "protein": 25, "carbs": 0, "fat": 19, "image": "🥩"},
    {"name": "Pork Chop (100g)", "calories": 231, "protein": 25, "carbs": 0, "fat": 14, "image": "🥓"},
    {"name": "Bacon (2 slices)", "calories": 90, "protein": 6, "carbs": 0.6, "fat": 7, "image": "🥓"},
    {"name": "Turkey Breast (100g)", "calories": 135, "protein": 30, "carbs": 0, "fat": 0.7, "image": "🦃"},
    {"name": "Tuna (100g canned)", "calories": 116, "protein": 26, "carbs": 0, "fat": 0.8, "image": "🐟"},
    {"name": "Shrimp (100g)", "calories": 99, "protein": 24, "carbs": 0.2, "fat": 0.3, "image": "🦐"},
    
    # GRAINS & CARBS
    {"name": "Rice (100g cooked)", "calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "image": "🍚"},
    {"name": "Brown Rice (100g cooked)", "calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9, "image": "🍚"},
    {"name": "Wheat Roti (1 medium)", "calories": 75, "protein": 2.5, "carbs": 14, "fat": 0.8, "image": "🫓"},
    {"name": "Whole Wheat Bread (1 slice)", "calories": 100, "protein": 4, "carbs": 17, "fat": 1.5, "image": "🍞"},
    {"name": "White Bread (1 slice)", "calories": 79, "protein": 2.7, "carbs": 14, "fat": 1, "image": "🍞"},
    {"name": "Pasta (100g cooked)", "calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "image": "🍝"},
    {"name": "Oats (100g cooked)", "calories": 68, "protein": 2.4, "carbs": 12, "fat": 1.4, "image": "🌾"},
    {"name": "Corn (100g cooked)", "calories": 86, "protein": 3.3, "carbs": 19, "fat": 1.2, "image": "🌽"},
    {"name": "Popcorn (3 cups)", "calories": 93, "protein": 3, "carbs": 12, "fat": 4, "image": "🍿"},
    {"name": "Quinoa (100g cooked)", "calories": 120, "protein": 4.4, "carbs": 21, "fat": 1.9, "image": "🌾"},
    {"name": "Bagel (1 medium)", "calories": 245, "protein": 9, "carbs": 48, "fat": 1.5, "image": "🥯"},
    {"name": "English Muffin (1)", "calories": 134, "protein": 4.4, "carbs": 26, "fat": 1, "image": "🍞"},
    {"name": "Tortilla (1 medium)", "calories": 104, "protein": 3, "carbs": 18, "fat": 2.5, "image": "🌮"},
    {"name": "Pancake (1 medium)", "calories": 86, "protein": 2.4, "carbs": 11, "fat": 3.5, "image": "🥞"},
    {"name": "Waffle (1 medium)", "calories": 218, "protein": 6, "carbs": 25, "fat": 11, "image": "🧇"},
    
    # VEGETABLES
    {"name": "Broccoli (100g)", "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "image": "🥦"},
    {"name": "Spinach (100g)", "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "image": "🥬"},
    {"name": "Carrot (100g)", "calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "image": "🥕"},
    {"name": "Tomato (100g)", "calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "image": "🍅"},
    {"name": "Potato (100g boiled)", "calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "image": "🥔"},
    {"name": "Sweet Potato (100g)", "calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "image": "🥔"},
    {"name": "Bell Pepper (100g)", "calories": 31, "protein": 1, "carbs": 6, "fat": 0.3, "image": "🫑"},
    {"name": "Cucumber (100g)", "calories": 16, "protein": 0.7, "carbs": 3.6, "fat": 0.1, "image": "🥒"},
    {"name": "Onion (100g)", "calories": 40, "protein": 1.1, "carbs": 9, "fat": 0.1, "image": "🧅"},
    {"name": "Garlic (1 clove)", "calories": 4, "protein": 0.2, "carbs": 1, "fat": 0, "image": "🧄"},
    {"name": "Capsicum (100g)", "calories": 31, "protein": 1, "carbs": 6, "fat": 0.3, "image": "🫑"},
    {"name": "Cabbage (100g)", "calories": 25, "protein": 1.3, "carbs": 5.8, "fat": 0.1, "image": "🥬"},
    {"name": "Lettuce (100g)", "calories": 15, "protein": 1.4, "carbs": 2.9, "fat": 0.2, "image": "🥬"},
    {"name": "Celery (100g)", "calories": 16, "protein": 0.7, "carbs": 3, "fat": 0.2, "image": "🥬"},
    {"name": "Asparagus (100g)", "calories": 20, "protein": 2.2, "carbs": 3.9, "fat": 0.1, "image": "🥒"},
    {"name": "Green Beans (100g)", "calories": 31, "protein": 1.8, "carbs": 7, "fat": 0.2, "image": "🫛"},
    {"name": "Zucchini (100g)", "calories": 17, "protein": 1.2, "carbs": 3.1, "fat": 0.3, "image": "🥒"},
    
    # FRUITS
    {"name": "Apple (1 medium)", "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "image": "🍎"},
    {"name": "Banana (1 medium)", "calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.3, "image": "🍌"},
    {"name": "Orange (1 medium)", "calories": 62, "protein": 1.2, "carbs": 15, "fat": 0.3, "image": "🍊"},
    {"name": "Mango (100g)", "calories": 60, "protein": 0.8, "carbs": 15, "fat": 0.4, "image": "🥭"},
    {"name": "Papaya (100g)", "calories": 43, "protein": 0.6, "carbs": 11, "fat": 0.3, "image": "🧡"},
    {"name": "Strawberry (100g)", "calories": 32, "protein": 0.8, "carbs": 7.7, "fat": 0.3, "image": "🍓"},
    {"name": "Grapes (100g)", "calories": 67, "protein": 0.7, "carbs": 17, "fat": 0.4, "image": "🍇"},
    {"name": "Watermelon (100g)", "calories": 30, "protein": 0.6, "carbs": 7.6, "fat": 0.2, "image": "🍉"},
    {"name": "Pomegranate (100g)", "calories": 68, "protein": 1.7, "carbs": 17, "fat": 0.3, "image": "❤️"},
    {"name": "Blueberries (100g)", "calories": 57, "protein": 0.7, "carbs": 14, "fat": 0.3, "image": "🫐"},
    {"name": "Pineapple (100g)", "calories": 50, "protein": 0.5, "carbs": 13, "fat": 0.1, "image": "🍍"},
    {"name": "Peach (1 medium)", "calories": 59, "protein": 1.4, "carbs": 14, "fat": 0.4, "image": "🍑"},
    {"name": "Pear (1 medium)", "calories": 101, "protein": 0.6, "carbs": 27, "fat": 0.2, "image": "🍐"},
    {"name": "Cherries (100g)", "calories": 50, "protein": 1, "carbs": 12, "fat": 0.3, "image": "🍒"},
    {"name": "Kiwi (1 medium)", "calories": 42, "protein": 0.8, "carbs": 10, "fat": 0.4, "image": "🥝"},
    
    # NUTS & SEEDS
    {"name": "Almonds (23 nuts, 28g)", "calories": 164, "protein": 6, "carbs": 6, "fat": 14, "image": "🫘"},
    {"name": "Peanuts (1oz)", "calories": 161, "protein": 7, "carbs": 5, "fat": 14, "image": "🥜"},
    {"name": "Cashews (23 nuts, 28g)", "calories": 155, "protein": 5, "carbs": 9, "fat": 12, "image": "🥜"},
    {"name": "Walnuts (14 halves, 28g)", "calories": 185, "protein": 4.3, "carbs": 4, "fat": 18.5, "image": "🌰"},
    {"name": "Pumpkin Seeds (1oz)", "calories": 151, "protein": 5, "carbs": 5, "fat": 13, "image": "🎃"},
    {"name": "Sunflower Seeds (1oz)", "calories": 165, "protein": 5.5, "carbs": 7, "fat": 14, "image": "🌻"},
    {"name": "Chia Seeds (1oz)", "calories": 138, "protein": 4.7, "carbs": 12, "fat": 8.7, "image": "⚫"},
    {"name": "Flax Seeds (1oz)", "calories": 150, "protein": 5, "carbs": 8, "fat": 12, "image": "🟤"},
    {"name": "Pecans (1oz)", "calories": 196, "protein": 2.6, "carbs": 4, "fat": 20, "image": "🌰"},
    {"name": "Pistachios (1oz)", "calories": 159, "protein": 6, "carbs": 8, "fat": 13, "image": "🥜"},
    
    # OILS & FATS
    {"name": "Olive Oil (1 tbsp, 15ml)", "calories": 119, "protein": 0, "carbs": 0, "fat": 13.5, "image": "🫒"},
    {"name": "Coconut Oil (1 tbsp, 15ml)", "calories": 117, "protein": 0, "carbs": 0, "fat": 13.6, "image": "🥥"},
    {"name": "Butter (1 tbsp, 14g)", "calories": 102, "protein": 0.1, "carbs": 0, "fat": 11.5, "image": "🧈"},
    {"name": "Avocado (1/2 medium)", "calories": 120, "protein": 1.5, "carbs": 6, "fat": 11, "image": "🥑"},
    {"name": "Mayonnaise (1 tbsp)", "calories": 94, "protein": 0.1, "carbs": 0.1, "fat": 10, "image": "🥄"},
    
    # CONDIMENTS & SAUCES
    {"name": "Honey (1 tbsp, 21g)", "calories": 64, "protein": 0.1, "carbs": 17, "fat": 0, "image": "🍯"},
    {"name": "Peanut Butter (2 tbsp, 32g)", "calories": 188, "protein": 8, "carbs": 7, "fat": 16, "image": "🥜"},
    {"name": "Ketchup (1 tbsp)", "calories": 17, "protein": 0.2, "carbs": 4.5, "fat": 0, "image": "🍅"},
    {"name": "Mustard (1 tbsp)", "calories": 10, "protein": 0.6, "carbs": 1, "fat": 0.6, "image": "🟡"},
    {"name": "BBQ Sauce (2 tbsp)", "calories": 58, "protein": 0.3, "carbs": 14, "fat": 0.2, "image": "🍖"},
    {"name": "Ranch Dressing (2 tbsp)", "calories": 129, "protein": 0.4, "carbs": 2, "fat": 13, "image": "🥗"},
    
    # INDIAN DISHES
    {"name": "Biryani Rice (150g)", "calories": 220, "protein": 4.5, "carbs": 42, "fat": 4.5, "image": "🍚"},
    {"name": "Chicken Biryani (1 plate)", "calories": 450, "protein": 25, "carbs": 55, "fat": 15, "image": "🍗"},
    {"name": "Mutton Biryani (1 plate)", "calories": 520, "protein": 28, "carbs": 58, "fat": 18, "image": "🍖"},
    {"name": "Veg Biryani (1 plate)", "calories": 380, "protein": 8, "carbs": 62, "fat": 12, "image": "🥗"},
    {"name": "Egg Biryani (1 plate)", "calories": 420, "protein": 18, "carbs": 56, "fat": 14, "image": "🥚"},
    {"name": "Hyderabadi Biryani (1 plate)", "calories": 480, "protein": 26, "carbs": 54, "fat": 16, "image": "🍗"},
    {"name": "Dal Makhani (150ml)", "calories": 150, "protein": 8, "carbs": 15, "fat": 6, "image": "🫘"},
    {"name": "Dal Tadka (150ml)", "calories": 120, "protein": 7, "carbs": 18, "fat": 3, "image": "🫘"},
    {"name": "Butter Chicken (200g)", "calories": 320, "protein": 28, "carbs": 6, "fat": 22, "image": "🍗"},
    {"name": "Chicken Tikka Masala (200g)", "calories": 280, "protein": 26, "carbs": 8, "fat": 18, "image": "🍗"},
    {"name": "Chicken Curry (200g)", "calories": 250, "protein": 24, "carbs": 10, "fat": 14, "image": "🍗"},
    {"name": "Mutton Curry (200g)", "calories": 310, "protein": 26, "carbs": 8, "fat": 20, "image": "🍖"},
    {"name": "Fish Curry (200g)", "calories": 220, "protein": 22, "carbs": 6, "fat": 12, "image": "🐟"},
    {"name": "Paneer Butter Masala (200g)", "calories": 350, "protein": 18, "carbs": 12, "fat": 26, "image": "🧀"},
    {"name": "Palak Paneer (200g)", "calories": 280, "protein": 16, "carbs": 10, "fat": 20, "image": "🥬"},
    {"name": "Chole (Chickpea Curry, 200g)", "calories": 240, "protein": 12, "carbs": 35, "fat": 6, "image": "🫘"},
    {"name": "Rajma (Kidney Beans, 200g)", "calories": 220, "protein": 14, "carbs": 32, "fat": 4, "image": "🫘"},
    {"name": "Samosa (1 piece, 50g)", "calories": 170, "protein": 3, "carbs": 15, "fat": 10, "image": "🥟"},
    {"name": "Pakora (5 pieces)", "calories": 200, "protein": 4, "carbs": 18, "fat": 12, "image": "🥘"},
    {"name": "Dosa (1 piece)", "calories": 110, "protein": 3, "carbs": 18, "fat": 3, "image": "🥙"},
    {"name": "Masala Dosa (1 piece)", "calories": 180, "protein": 5, "carbs": 28, "fat": 6, "image": "🥙"},
    {"name": "Idli (1 piece)", "calories": 39, "protein": 2, "carbs": 8, "fat": 0.1, "image": "🤍"},
    {"name": "Vada (1 piece)", "calories": 90, "protein": 3, "carbs": 10, "fat": 4, "image": "🟤"},
    {"name": "Upma (1 bowl)", "calories": 200, "protein": 5, "carbs": 35, "fat": 5, "image": "🍚"},
    {"name": "Poha (1 bowl)", "calories": 180, "protein": 4, "carbs": 32, "fat": 4, "image": "🍚"},
    {"name": "Naan (1 piece, 90g)", "calories": 262, "protein": 8, "carbs": 40, "fat": 7, "image": "🫓"},
    {"name": "Garlic Naan (1 piece)", "calories": 280, "protein": 8, "carbs": 42, "fat": 8, "image": "🫓"},
    {"name": "Butter Naan (1 piece)", "calories": 290, "protein": 8, "carbs": 41, "fat": 9, "image": "🫓"},
    {"name": "Chapati/Roti (1 piece)", "calories": 75, "protein": 2.5, "carbs": 14, "fat": 0.8, "image": "🫓"},
    {"name": "Paratha (1 piece)", "calories": 150, "protein": 3, "carbs": 18, "fat": 7, "image": "🫓"},
    {"name": "Aloo Paratha (1 piece)", "calories": 200, "protein": 4, "carbs": 25, "fat": 9, "image": "🫓"},
    {"name": "Papad (1 piece fried)", "calories": 50, "protein": 2, "carbs": 6, "fat": 2.5, "image": "📍"},
    {"name": "Raita (150g)", "calories": 65, "protein": 3, "carbs": 6, "fat": 2.5, "image": "🥛"},
    {"name": "Pickle (1 tbsp, 15g)", "calories": 20, "protein": 0.5, "carbs": 3, "fat": 0.5, "image": "🥒"},
    {"name": "Gulab Jamun (2 pieces)", "calories": 150, "protein": 2, "carbs": 25, "fat": 5, "image": "🍡"},
    {"name": "Jalebi (50g)", "calories": 150, "protein": 1, "carbs": 30, "fat": 3, "image": "🟠"},
    {"name": "Kheer (1 bowl)", "calories": 180, "protein": 5, "carbs": 28, "fat": 6, "image": "🍚"},
    
    # US FAST FOOD
    {"name": "Hamburger (1 regular)", "calories": 354, "protein": 20, "carbs": 30, "fat": 17, "image": "🍔"},
    {"name": "Cheeseburger (1 regular)", "calories": 400, "protein": 22, "carbs": 32, "fat": 20, "image": "🍔"},
    {"name": "Big Mac", "calories": 563, "protein": 26, "carbs": 46, "fat": 33, "image": "🍔"},
    {"name": "French Fries (medium)", "calories": 365, "protein": 4, "carbs": 48, "fat": 17, "image": "🍟"},
    {"name": "Pizza Slice (1 slice)", "calories": 285, "protein": 12, "carbs": 36, "fat": 10, "image": "🍕"},
    {"name": "Pizza Margherita (1 slice)", "calories": 250, "protein": 11, "carbs": 33, "fat": 9, "image": "🍕"},
    {"name": "Pizza Pepperoni (1 slice)", "calories": 310, "protein": 13, "carbs": 35, "fat": 13, "image": "🍕"},
    {"name": "Pizza Chicken (1 slice)", "calories": 290, "protein": 15, "carbs": 34, "fat": 11, "image": "🍕"},
    {"name": "Pizza Vegetarian (1 slice)", "calories": 260, "protein": 10, "carbs": 36, "fat": 9, "image": "🍕"},
    {"name": "Pizza BBQ Chicken (1 slice)", "calories": 320, "protein": 16, "carbs": 38, "fat": 12, "image": "🍕"},
    {"name": "Pizza Hawaiian (1 slice)", "calories": 280, "protein": 13, "carbs": 36, "fat": 10, "image": "🍕"},
    {"name": "Pizza Meat Lovers (1 slice)", "calories": 350, "protein": 17, "carbs": 35, "fat": 16, "image": "🍕"},
    {"name": "Hot Dog (1)", "calories": 290, "protein": 10, "carbs": 24, "fat": 17, "image": "🌭"},
    {"name": "Chicken Nuggets (6 pieces)", "calories": 287, "protein": 15, "carbs": 18, "fat": 18, "image": "🍗"},
    {"name": "Taco (1)", "calories": 226, "protein": 10, "carbs": 21, "fat": 11, "image": "🌮"},
    {"name": "Burrito (1)", "calories": 510, "protein": 20, "carbs": 66, "fat": 17, "image": "🌯"},
    {"name": "Sub Sandwich (6 inch)", "calories": 350, "protein": 18, "carbs": 47, "fat": 9, "image": "🥪"},
    {"name": "Chicken Sandwich", "calories": 420, "protein": 28, "carbs": 42, "fat": 16, "image": "🍔"},
    {"name": "Fish Sandwich", "calories": 380, "protein": 16, "carbs": 40, "fat": 18, "image": "🍔"},
    
    # BEVERAGES
    {"name": "Water (250ml)", "calories": 0, "protein": 0, "carbs": 0, "fat": 0, "image": "💧"},
    {"name": "Black Coffee (1 cup)", "calories": 4, "protein": 0.3, "carbs": 0.7, "fat": 0, "image": "☕"},
    {"name": "Green Tea (1 cup)", "calories": 2, "protein": 0.4, "carbs": 0, "fat": 0, "image": "🫖"},
    {"name": "Orange Juice (250ml)", "calories": 112, "protein": 2, "carbs": 26, "fat": 0.5, "image": "🧃"},
    {"name": "Coca-Cola (250ml)", "calories": 105, "protein": 0, "carbs": 29, "fat": 0, "image": "🥤"},
    {"name": "Beer (330ml)", "calories": 154, "protein": 1.6, "carbs": 10.6, "fat": 0, "image": "🍺"},
    {"name": "Red Wine (150ml)", "calories": 125, "protein": 0.1, "carbs": 3.8, "fat": 0, "image": "🍷"},
    {"name": "Latte (250ml)", "calories": 190, "protein": 10, "carbs": 18, "fat": 7, "image": "☕"},
    {"name": "Smoothie (250ml)", "calories": 145, "protein": 3, "carbs": 30, "fat": 1.5, "image": "🥤"},
    {"name": "Energy Drink (250ml)", "calories": 110, "protein": 0, "carbs": 28, "fat": 0, "image": "⚡"},
    
    # SNACKS & PROCESSED
    {"name": "Chips (1oz, 28.35g)", "calories": 155, "protein": 2, "carbs": 15, "fat": 9.6, "image": "🍟"},
    {"name": "Biscuit (25g)", "calories": 130, "protein": 2, "carbs": 18, "fat": 6, "image": "🍪"},
    {"name": "Chocolate (50g)", "calories": 240, "protein": 4, "carbs": 26, "fat": 13, "image": "🍫"},
    {"name": "Ice Cream (100g)", "calories": 207, "protein": 3.5, "carbs": 24, "fat": 11, "image": "🍦"},
    {"name": "Donut (1 piece, 50g)", "calories": 190, "protein": 2, "carbs": 23, "fat": 10, "image": "🍩"},
    {"name": "Candy (10g)", "calories": 39, "protein": 0, "carbs": 10, "fat": 0, "image": "🍬"},
    {"name": "Granola Bar (1)", "calories": 120, "protein": 2, "carbs": 19, "fat": 4, "image": "🍫"},
    {"name": "Pretzels (1oz)", "calories": 108, "protein": 3, "carbs": 23, "fat": 0.8, "image": "🥨"},
    {"name": "Crackers (5)", "calories": 80, "protein": 1, "carbs": 10, "fat": 4, "image": "🍘"},
    {"name": "Protein Bar (1)", "calories": 200, "protein": 20, "carbs": 22, "fat": 7, "image": "🍫"},
]

def search_foods(query: str):
    """Search foods by name"""
    if not query:
        return FOOD_DATABASE
    
    query_lower = query.lower()
    return [food for food in FOOD_DATABASE if query_lower in food['name'].lower()]

def get_food_by_name(name: str):
    """Get a specific food by name"""
    for food in FOOD_DATABASE:
        if food['name'].lower() == name.lower():
            return food
    return None

def get_common_foods(limit: int = 12):
    """Get most common foods for quick selection"""
    common_indices = [0, 1, 5, 12, 13, 18, 20, 24, 32, 34, 36, 38]  # Popular foods
    return [FOOD_DATABASE[i] for i in common_indices if i < len(FOOD_DATABASE)][:limit]
