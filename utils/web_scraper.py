from duckduckgo_search import DDGS
import logging
import time

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def scrape_web(query, num_results=5, retries=3, delay=2):
    """
    Scrapes the web for a given query using DuckDuckGo's search API and returns the combined text of the results.

    Parameters:
    - query (str): The search query to be used.
    - num_results (int): The number of search results to fetch (default is 5).
    - retries (int): The number of retries in case of failure (default is 3).
    - delay (int): The delay in seconds between retries (default is 2).

    Returns:
    - str: A combined string of the body text from the search results, or a message if no results are found.
    
    Logs:
    - Logs messages for errors, retries, and the final result.
    """
    attempt = 0
    while attempt < retries:
        try:
            with DDGS() as ddgs:
                logger.info(f"Scraping web for query: {query} with {num_results} results.")
                results = ddgs.text(query, max_results=num_results)
                
                if not results:
                    logger.warning("No results found for the query.")
                    return "No relevant results found."
                
                # Extract the 'body' from each result and join them into a single string
                combined = "\n".join([r['body'] for r in results if 'body' in r])
                return combined

        except Exception as e:
            logger.error(f"Error while scraping web: {e}")
            attempt += 1
            if attempt < retries:
                logger.info(f"Retrying... Attempt {attempt}/{retries}")
                time.sleep(delay)
            else:
                logger.critical("Max retries reached. Could not fetch results.")
                return f"Error: {e}"