import pandas as pd

class PropertySearch:
    def __init__(self, df):
        self.df = df
    
    def search(self, filters):
        results = self.df.copy()
        
        if 'bhk' in filters:
            bhk_value = filters['bhk']
            if bhk_value == 'RK':
                results = results[results['type'].str.contains('RK', case=False, na=False)]
            else:
                results = results[results['bhk_number'] == float(bhk_value)]
        
        if 'max_price_crore' in filters:
            max_price = filters['max_price_crore']
            results = results.dropna(subset=['price_crore'])
            results = results[results['price_crore'] <= float(max_price)]
        
        if 'status' in filters:
            results = results[results['status'] == filters['status']]
        
        if 'location' in filters:
            location = filters['location'].lower()
            results = results[
                results['landmark'].str.lower().str.contains(location, na=False) |
                results['fullAddress'].str.lower().str.contains(location, na=False)
            ]
        
        if 'bathrooms' in filters:
            req_bathrooms = filters['bathrooms']
            results = results[pd.to_numeric(results['bathrooms'], errors='coerce') >= req_bathrooms]
        
        results = results.dropna(subset=['projectName', 'price'])
        results = results.sort_values('price_crore')
        
        return results
    
    def get_stats(self, results):
        if len(results) == 0:
            return None
        
        stats = {
            'count': len(results),
            'min_price': results['price_crore'].min(),
            'max_price': results['price_crore'].max(),
            'avg_price': results['price_crore'].mean(),
            'localities': results['landmark'].value_counts().head(3).to_dict(),
            'ready_count': results['is_ready'].sum(),
            'construction_count': (~results['is_ready']).sum()
        }
        
        return stats
