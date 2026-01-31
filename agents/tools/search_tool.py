import os
import serpapi
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class SearchInput(BaseModel):
    query: str = Field(description='Query to search for (e.g. "grocery stores near...").')

class SearchInputSchema(BaseModel):
    params: SearchInput

@tool(args_schema=SearchInputSchema)
def search_tool(params: SearchInput):
    '''
    Start a general search using the Google Search engine. Useful for finding grocery stores, train tickets, activities, etc.
    '''
    search_params = {
        'api_key': os.environ.get('SERPAPI_API_KEY'),
        'engine': 'google',
        'q': params.query,
        'google_domain': 'google.com',
        'gl': 'us',
        'hl': 'en',
    }
    
    try:
        search = serpapi.search(search_params)
        results = search.data
        
        # Extract organic results
        organic_results = results.get('organic_results', [])
        formatted_results = []
        for res in organic_results[:5]:
            formatted_results.append({
                'title': res.get('title'),
                'link': res.get('link'),
                'snippet': res.get('snippet')
            })
            
        # Extract local places if available (good for grocery stores)
        local_results = results.get('local_results', {}).get('places', [])
        if local_results:
             for res in local_results[:5]:
                formatted_results.append({
                    'title': res.get('title'),
                    'address': res.get('address'),
                    'rating': res.get('rating'),
                    'reviews': res.get('reviews')
                })
                
        return formatted_results
    except Exception as e:
        return str(e)
