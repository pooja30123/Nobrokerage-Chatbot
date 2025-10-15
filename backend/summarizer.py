import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class SummaryGenerator:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_summary(self, query, results, stats):
        if stats is None or stats['count'] == 0:
            return "Sorry, no properties found matching your criteria. Try different filters."
        
        if self.model is None:
            return self._template_summary(stats)
        
        context = f"""
User searched for: {query}

Results:
- Total: {stats['count']} properties
- Price: ₹{stats['min_price']:.2f} to ₹{stats['max_price']:.2f} Crore
- Average: ₹{stats['avg_price']:.2f} Crore
- Ready: {stats['ready_count']}, Under Construction: {stats['construction_count']}
- Localities: {', '.join(list(stats['localities'].keys())[:3])}
"""
        
        prompt = f"""You are a real estate assistant. Write a friendly 3-4 sentence summary based on this data:

{context}

Be specific with numbers. Keep it natural and helpful."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return self._template_summary(stats)
    
    def _template_summary(self, stats):
        summary = f"I found {stats['count']} properties for you. "
        summary += f"Prices range from ₹{stats['min_price']:.2f} Cr to ₹{stats['max_price']:.2f} Cr (average ₹{stats['avg_price']:.2f} Cr). "
        
        if stats['ready_count'] > 0:
            summary += f"{stats['ready_count']} are ready to move in, "
        if stats['construction_count'] > 0:
            summary += f"{stats['construction_count']} are under construction. "
        
        if stats['localities']:
            top_loc = list(stats['localities'].keys())[0]
            summary += f"Most options available in {top_loc}."
        
        return summary
