import re

class QueryParser:
    def __init__(self):
        self.cities = ['mumbai', 'pune', 'thane', 'delhi', 'bangalore', 'chennai', 'hyderabad', 
                      'kolkata', 'ahmedabad', 'lucknow', 'surat', 'jaipur', 'indore', 'nagpur']
        
        self.locations = ['chembur', 'andheri', 'bandra', 'dadar', 'borivali', 'kandivali', 
                         'malad', 'sakinaka', 'mazgaon', 'goregaon', 'jogeshwari', 'khar',
                         'sindhi society', 'lodha xperia mall', 'mamburi', 'kothrud', 'baner',
                         'hinjewadi', 'shreepati arcade']
        
        self.number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
    
    def extract_bhk(self, query):
        query_lower = query.lower()
        bhk_pattern = r'(\d+)\s*(?:bhk|bedroom|bed)'
        match = re.search(bhk_pattern, query_lower)
        
        if match:
            return int(match.group(1))
        
        for word, num in self.number_words.items():
            if f"{word} bedroom" in query_lower or f"{word} bhk" in query_lower:
                return num
        
        if any(word in query_lower for word in ['rk', '1rk', 'room kitchen']):
            return 'RK'
            
        if 'flat' in query_lower or 'apartment' in query_lower:
            num_match = re.search(r'(\d+)\s+(?:flat|apartment)', query_lower)
            if num_match:
                return int(num_match.group(1))
            
            for word, num in self.number_words.items():
                if f"{word} flat" in query_lower or f"{word} apartment" in query_lower:
                    return num
        
        return None
    
    def extract_budget(self, query):
        query_lower = query.lower()
        safe_query = re.sub(r'\bready\b', 'available', query_lower)
        
        cr_pattern = r'(?:under|below|within|upto|max|less than|around|about|of|at)\s*₹?\s*(\d+\.?\d*)\s*(?:cr|crore|crores|cr\.)'
        match = re.search(cr_pattern, safe_query)
        if match:
            return float(match.group(1))
        
        lakh_pattern = r'(?:under|below|within|upto|max|less than|around|about|of|at)\s*₹?\s*(\d+\.?\d*)\s*\b(?:l|lakh|lakhs|lac)\b'
        match = re.search(lakh_pattern, safe_query)
        if match:
            return float(match.group(1)) / 100
        
        direct_cr_pattern = r'₹?\s*(\d+\.?\d*)\s*\bcr(?:\.\b|o?re?)\b'
        match = re.search(direct_cr_pattern, safe_query)
        if match:
            return float(match.group(1))
        
        price_cr_pattern = r'₹?\s*(\d+\.?\d*)\s*(?=\s*\b(?:cr|crore|cr\.))'
        match = re.search(price_cr_pattern, safe_query)
        if match:
            return float(match.group(1))
        
        price_lakh_pattern = r'₹?\s*(\d+\.?\d*)\s*(?=\s*\b(?:l|lakh|lac)\b)'
        match = re.search(price_lakh_pattern, safe_query)
        if match:
            amount = float(match.group(1))
            if amount < 1000:
                return amount / 100
            else:
                return amount
        
        return None
    
    def extract_status(self, query):
        query_lower = query.lower()
        if re.search(r'\b(?:ready|immediate|move in|move-in|available now)\b', query_lower):
            return 'READY_TO_MOVE'
        
        if re.search(r'\b(?:under construction|upcoming|new launch|not ready|future project)\b', query_lower):
            return 'UNDER_CONSTRUCTION'
        
        return None
    
    def extract_location(self, query):
        query_lower = query.lower()
        for city in self.cities:
            if city in query_lower:
                return {'type': 'city', 'value': city.title()}
        
        for location in self.locations:
            if location in query_lower:
                return {'type': 'landmark', 'value': location.title()}
        
        return None
    
    def extract_bathrooms(self, query):
        query_lower = query.lower()
        bath_pattern = r'(\d+)\s*(?:bathroom|bath|washroom|toilet)'
        match = re.search(bath_pattern, query_lower)
        
        if match:
            return int(match.group(1))
        
        for word, num in self.number_words.items():
            if f"{word} bathroom" in query_lower or f"{word} bath" in query_lower:
                return num
        
        return None
    
    def is_relevant_query(self, query):
        query_lower = query.lower().strip()
        relevant_keywords = [
            'bhk', 'bedroom', 'flat', 'apartment', 'property', 'home', 'house',
            'budget', 'price', 'under', 'below', 'within', 'upto', 'max', 'around', 'about', 'of', 'at',
            'lakh', 'cr', 'crore', 'rs', '₹', 'cr.',
            'ready', 'move', 'construction', 'location', 'in', 'near', 'area', 'close to',
            'room', 'rk', 'studio', 'penthouse', 'builder', 'project', 'building',
            'floor', 'carpet', 'area', 'sqft', 'square feet', 'bathroom', 'toilet',
            'washroom', 'balcony', 'lift', 'parking', 'furnished', 'unfurnished',
            'possession', 'available', 'immediate', 'under', 'upcoming', 'new'
        ]
        
        relevant_keywords.extend(self.cities)
        relevant_keywords.extend(self.locations)
        
        for keyword in relevant_keywords:
            if keyword in query_lower:
                return True
        
        if re.search(r'\d+', query_lower):
            return True
        
        return False
    
    def parse(self, query):
        if not self.is_relevant_query(query):
            return {'invalid_query': True}
        
        filters = {}
        bhk = self.extract_bhk(query)
        if bhk:
            filters['bhk'] = bhk
        
        budget = self.extract_budget(query)
        if budget:
            filters['max_price_crore'] = budget
        
        status = self.extract_status(query)
        if status:
            filters['status'] = status
        
        location = self.extract_location(query)
        if location:
            filters['location'] = location['value']
        
        bathrooms = self.extract_bathrooms(query)
        if bathrooms:
            filters['bathrooms'] = bathrooms
        
        return filters
