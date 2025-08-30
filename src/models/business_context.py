"""
Business Type Context Dataset for Review Legitimacy Detection
Provides context-aware topic detection based on business type
"""

class BusinessContext:
    def __init__(self):
        # Comprehensive business type mapping with relevant and irrelevant topics
        self.business_types = {
            # Food & Dining
            'restaurant': {
                'relevant': ['food', 'meal', 'dish', 'cuisine', 'menu', 'chef', 'dining', 'taste', 'flavor', 'service', 'waiter', 'waitress', 'table', 'reservation', 'atmosphere', 'ambiance', 'price', 'portion', 'appetizer', 'entree', 'dessert', 'wine', 'beer', 'cocktail', 'drink', 'beverage'],
                'irrelevant': ['book', 'clothing', 'electronics', 'car', 'phone', 'computer', 'software', 'medicine', 'haircut', 'massage', 'gym', 'workout', 'hotel', 'room']
            },
            'fast_food': {
                'relevant': ['burger', 'fries', 'chicken', 'sandwich', 'combo', 'meal', 'drive-thru', 'quick', 'fast', 'takeout', 'delivery', 'sauce', 'soda', 'shake', 'nuggets', 'wrap', 'salad'],
                'irrelevant': ['alcohol', 'wine', 'beer', 'cocktail', 'book', 'clothing', 'electronics', 'car', 'phone', 'computer', 'medicine', 'haircut', 'massage', 'gym', 'hotel']
            },
            'coffee_shop': {
                'relevant': ['coffee', 'espresso', 'latte', 'cappuccino', 'americano', 'mocha', 'frappuccino', 'tea', 'pastry', 'muffin', 'croissant', 'wifi', 'study', 'laptop', 'barista', 'beans', 'roast', 'milk', 'sugar', 'cream'],
                'irrelevant': ['alcohol', 'wine', 'beer', 'cocktail', 'burger', 'pizza', 'steak', 'book', 'clothing', 'electronics', 'car', 'medicine', 'haircut', 'massage', 'gym']
            },
            'bar': {
                'relevant': ['beer', 'wine', 'cocktail', 'whiskey', 'vodka', 'rum', 'gin', 'tequila', 'alcohol', 'drink', 'bartender', 'happy hour', 'draft', 'bottle', 'shot', 'mixer', 'appetizer', 'snack', 'music', 'atmosphere', 'nightlife'],
                'irrelevant': ['book', 'clothing', 'electronics', 'car', 'phone', 'computer', 'medicine', 'haircut', 'massage', 'gym', 'hotel', 'room', 'coffee', 'tea']
            },
            'pizza': {
                'relevant': ['pizza', 'slice', 'topping', 'cheese', 'pepperoni', 'sausage', 'mushroom', 'crust', 'dough', 'sauce', 'delivery', 'takeout', 'oven', 'italian', 'calzone', 'breadsticks'],
                'irrelevant': ['book', 'clothing', 'electronics', 'car', 'phone', 'computer', 'medicine', 'haircut', 'massage', 'gym', 'hotel', 'sushi', 'chinese']
            },
            
            # Retail & Shopping
            'bookstore': {
                'relevant': ['book', 'novel', 'author', 'reading', 'literature', 'fiction', 'non-fiction', 'textbook', 'magazine', 'newspaper', 'bookmark', 'chapter', 'story', 'library', 'study', 'education', 'knowledge'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'wine', 'beer', 'clothing', 'electronics', 'car', 'medicine', 'haircut', 'massage', 'gym']
            },
            'clothing_store': {
                'relevant': ['shirt', 'pants', 'dress', 'shoes', 'jacket', 'sweater', 'jeans', 'skirt', 'blouse', 'suit', 'tie', 'belt', 'hat', 'fashion', 'style', 'size', 'fit', 'fabric', 'color', 'brand', 'designer'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'electronics', 'car', 'medicine', 'haircut', 'massage', 'gym', 'hotel']
            },
            'electronics_store': {
                'relevant': ['phone', 'computer', 'laptop', 'tablet', 'tv', 'camera', 'headphones', 'speaker', 'charger', 'cable', 'battery', 'screen', 'keyboard', 'mouse', 'software', 'app', 'technology', 'digital', 'wireless'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'car', 'medicine', 'haircut', 'massage', 'gym', 'hotel']
            },
            'grocery_store': {
                'relevant': ['groceries', 'produce', 'vegetables', 'fruits', 'meat', 'dairy', 'bread', 'milk', 'eggs', 'cheese', 'frozen', 'canned', 'organic', 'fresh', 'checkout', 'cashier', 'cart', 'aisle', 'shopping'],
                'irrelevant': ['clothing', 'electronics', 'car', 'phone', 'computer', 'medicine', 'haircut', 'massage', 'gym', 'hotel', 'book', 'alcohol', 'bar']
            },
            'pharmacy': {
                'relevant': ['medicine', 'prescription', 'medication', 'pills', 'pharmacy', 'pharmacist', 'health', 'drug', 'vitamin', 'supplement', 'treatment', 'doctor', 'illness', 'pain', 'relief', 'dosage'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'haircut', 'massage', 'gym', 'hotel']
            },
            
            # Services
            'hair_salon': {
                'relevant': ['haircut', 'hairstyle', 'hair', 'stylist', 'shampoo', 'conditioner', 'color', 'dye', 'highlights', 'perm', 'blow-dry', 'trim', 'layers', 'bangs', 'salon', 'beauty', 'appointment'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'medicine', 'gym', 'hotel']
            },
            'spa': {
                'relevant': ['massage', 'facial', 'spa', 'relaxation', 'therapy', 'treatment', 'wellness', 'skin', 'body', 'aromatherapy', 'hot stone', 'deep tissue', 'swedish', 'manicure', 'pedicure', 'sauna'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'medicine', 'gym', 'hotel']
            },
            'gym': {
                'relevant': ['workout', 'exercise', 'fitness', 'gym', 'weights', 'cardio', 'treadmill', 'trainer', 'muscle', 'strength', 'endurance', 'yoga', 'pilates', 'membership', 'equipment', 'locker', 'shower'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'medicine', 'haircut', 'massage', 'hotel']
            },
            'bank': {
                'relevant': ['account', 'deposit', 'withdrawal', 'loan', 'credit', 'debit', 'atm', 'teller', 'banking', 'finance', 'money', 'cash', 'check', 'savings', 'checking', 'interest', 'fee'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'medicine', 'haircut', 'massage', 'gym', 'hotel']
            },
            
            # Automotive
            'car_dealership': {
                'relevant': ['car', 'vehicle', 'auto', 'truck', 'suv', 'sedan', 'coupe', 'engine', 'transmission', 'dealer', 'salesperson', 'financing', 'lease', 'warranty', 'test drive', 'mileage', 'fuel'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'medicine', 'haircut', 'massage', 'gym', 'hotel']
            },
            'gas_station': {
                'relevant': ['gas', 'fuel', 'gasoline', 'diesel', 'pump', 'station', 'convenience', 'snacks', 'drinks', 'lottery', 'cigarettes', 'car wash', 'oil', 'windshield', 'receipt'],
                'irrelevant': ['restaurant', 'dining', 'book', 'clothing', 'electronics', 'medicine', 'haircut', 'massage', 'gym', 'hotel', 'alcohol', 'bar']
            },
            
            # Hospitality
            'hotel': {
                'relevant': ['room', 'bed', 'bathroom', 'shower', 'towel', 'pillow', 'blanket', 'tv', 'wifi', 'breakfast', 'lobby', 'front desk', 'check-in', 'check-out', 'housekeeping', 'concierge', 'pool', 'gym'],
                'irrelevant': ['car', 'phone', 'computer', 'book', 'clothing', 'medicine', 'haircut', 'massage', 'grocery', 'pharmacy']
            },
            'movie_theater': {
                'relevant': ['movie', 'film', 'cinema', 'theater', 'screen', 'seat', 'ticket', 'popcorn', 'candy', 'soda', 'preview', 'trailer', 'actor', 'director', 'plot', 'sound', 'picture'],
                'irrelevant': ['car', 'phone', 'computer', 'book', 'clothing', 'medicine', 'haircut', 'massage', 'grocery', 'pharmacy', 'alcohol', 'bar']
            },
            
            # Healthcare
            'hospital': {
                'relevant': ['doctor', 'nurse', 'patient', 'treatment', 'surgery', 'emergency', 'room', 'bed', 'medical', 'health', 'care', 'medicine', 'prescription', 'diagnosis', 'therapy', 'recovery'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'haircut', 'gym', 'hotel']
            },
            'dental_office': {
                'relevant': ['teeth', 'tooth', 'dental', 'dentist', 'cleaning', 'filling', 'cavity', 'crown', 'root canal', 'braces', 'orthodontist', 'hygienist', 'floss', 'brush', 'mouth', 'gums'],
                'irrelevant': ['food', 'meal', 'burger', 'pizza', 'coffee', 'alcohol', 'book', 'clothing', 'electronics', 'car', 'haircut', 'massage', 'gym', 'hotel']
            }
        }
        
        # Business type aliases for flexible matching
        self.business_aliases = {
            'mcdonalds': 'fast_food',
            'burger king': 'fast_food',
            'kfc': 'fast_food',
            'subway': 'fast_food',
            'taco bell': 'fast_food',
            'wendys': 'fast_food',
            'starbucks': 'coffee_shop',
            'dunkin': 'coffee_shop',
            'barnes noble': 'bookstore',
            'borders': 'bookstore',
            'walmart': 'grocery_store',
            'target': 'grocery_store',
            'cvs': 'pharmacy',
            'walgreens': 'pharmacy',
            'best buy': 'electronics_store',
            'apple store': 'electronics_store',
            'macys': 'clothing_store',
            'gap': 'clothing_store',
            'zara': 'clothing_store',
            'h&m': 'clothing_store',
            'planet fitness': 'gym',
            'la fitness': 'gym',
            'marriott': 'hotel',
            'hilton': 'hotel',
            'holiday inn': 'hotel',
            'amc': 'movie_theater',
            'regal': 'movie_theater'
        }
    
    def get_business_type(self, business_name):
        """
        Determine business type from business name
        """
        if not business_name:
            return None
            
        business_name_lower = business_name.lower().strip()
        
        # Check direct aliases first
        if business_name_lower in self.business_aliases:
            return self.business_aliases[business_name_lower]
        
        # Check for partial matches in aliases
        for alias, business_type in self.business_aliases.items():
            if alias in business_name_lower or business_name_lower in alias:
                return business_type
        
        # Check for keywords in business name
        business_keywords = {
            'restaurant': ['restaurant', 'bistro', 'cafe', 'diner', 'eatery', 'grill', 'kitchen'],
            'fast_food': ['fast food', 'quick service', 'drive thru', 'takeaway'],
            'coffee_shop': ['coffee', 'espresso', 'brew', 'roastery'],
            'bar': ['bar', 'pub', 'tavern', 'lounge', 'brewery', 'nightclub'],
            'pizza': ['pizza', 'pizzeria'],
            'bookstore': ['bookstore', 'books', 'library'],
            'clothing_store': ['clothing', 'apparel', 'fashion', 'boutique'],
            'electronics_store': ['electronics', 'tech', 'computer', 'phone'],
            'grocery_store': ['grocery', 'supermarket', 'market', 'food store'],
            'pharmacy': ['pharmacy', 'drugstore', 'medical'],
            'hair_salon': ['salon', 'hair', 'barber'],
            'spa': ['spa', 'wellness', 'massage'],
            'gym': ['gym', 'fitness', 'health club'],
            'bank': ['bank', 'credit union', 'financial'],
            'car_dealership': ['dealership', 'auto', 'car sales'],
            'gas_station': ['gas', 'fuel', 'petrol', 'shell', 'exxon', 'bp'],
            'hotel': ['hotel', 'inn', 'resort', 'motel'],
            'movie_theater': ['theater', 'cinema', 'movies'],
            'hospital': ['hospital', 'medical center', 'clinic'],
            'dental_office': ['dental', 'dentist', 'orthodontist']
        }
        
        for business_type, keywords in business_keywords.items():
            for keyword in keywords:
                if keyword in business_name_lower:
                    return business_type
        
        return None
    
    def check_topic_relevance(self, business_type, review_text):
        """
        Check if review content is relevant to the business type
        Returns: (is_relevant, irrelevant_topics_found)
        """
        if not business_type or business_type not in self.business_types:
            return True, []  # If we can't determine business type, assume relevant
        
        business_data = self.business_types[business_type]
        review_lower = review_text.lower()
        
        irrelevant_topics = []
        
        # Check for irrelevant topics
        for irrelevant_topic in business_data['irrelevant']:
            if irrelevant_topic in review_lower:
                irrelevant_topics.append(irrelevant_topic)
        
        # If irrelevant topics found, check if there are also relevant topics
        if irrelevant_topics:
            relevant_topics_found = []
            for relevant_topic in business_data['relevant']:
                if relevant_topic in review_lower:
                    relevant_topics_found.append(relevant_topic)
            
            # If only irrelevant topics and no relevant topics, it's off-topic
            if not relevant_topics_found:
                return False, irrelevant_topics
            
            # If both relevant and irrelevant topics, it might be a mixed review
            # We'll be lenient and consider it relevant if there are relevant topics
            return True, []
        
        return True, []
    
    def get_business_context_info(self, business_type):
        """
        Get information about what topics are relevant/irrelevant for a business type
        """
        if not business_type or business_type not in self.business_types:
            return None
        
        return {
            'business_type': business_type,
            'relevant_topics': self.business_types[business_type]['relevant'][:10],  # First 10 for brevity
            'irrelevant_topics': self.business_types[business_type]['irrelevant'][:10]
        }

