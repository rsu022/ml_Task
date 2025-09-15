import json                     #to read json file
import os                        #environment variables
import re                       #regular expressions to extract numbers
import google.generativeai as genai   #gemini model

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Please set GOOGLE_API_KEY environment variable")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# opens json and list dic jasari
with open("daraz_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

#converts price query to min/max tuple
def parse_price_query(query: str):
    """
    Detect price-related info from the user query.
    Supports keywords: under, below, less than, around
    Returns (min_price, max_price) tuple
    """
    query = query.lower()    #insensitive banaucha
    numbers = [int(n) for n in re.findall(r'\d{3,6}', query)]   #3 to 6 digit number haru find garera list ma convert garne
    if not numbers:
        return (None, None)
    
    if ("between" in query or "to" in query) and len(numbers) >= 2:
        return (numbers[0], numbers[1])

    num = numbers[0]  #picks the 1st given num

    if "under" in query or "below" in query or "less than" in query:
        return (0, num)
    elif "around" in query or "about" in query:
        return (num - 2000, num + 2000)            #deko price ma aagadi pachi 2000 ko range
    else:                         # exact or default +/-2000
        return (num - 2000, num + 2000)

def recommend_products(query: str):      #takes user query and returns string
    """
    Recommend products based on price/features and answer any question dynamically
    """
    min_price, max_price = parse_price_query(query)         #parse_price_query bata min max price aauxa

    # Iterates in products list, price from string to int, within min-max range , yo sabai check ani adds to filtered list
    filtered = []
    for p in products:
        try:
            price_int = int(p.get("price", 0))
            if (min_price is None or price_int >= min_price) and (max_price is None or price_int <= max_price):
                filtered.append(p)
        except:
            continue

    if not filtered:
        filtered = products  # fallback: consider all products

    # Sort by rating then sold count (descending), higher rating and sold count first
    def safe_int(x):
        try: return int(x)
        except: return 0
    filtered = sorted(filtered, key=lambda x: (safe_int(x['rating']), safe_int(x['sold'])), reverse=True)

    # Prepare top 10 products context
    context_text = "\n".join([
        f"Title: {p['title']}, Specs: {p['specs']}, Price: {p['price']}, Sold: {p['sold']}, Rating: {p['rating']}, Location: {p['location']}, Link: {p['link']}"
        for p in filtered[:10]
    ])

    prompt = f"""
You are a Daraz product expert assistant. Based on the following product information, answer the user's question or recommend products.

Product data:
{context_text}

User request: {query}

Answer with recommendations or relevant info:
"""
#Generate response from Gemini model
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

#interactive loop 
def interactive_recommend():
    print("Daraz Product Recommender (type 'quit' to exit)")
    while True:
        query = input("\nAsk anything or request recommendations: ").strip()
        if query.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        answer = recommend_products(query)
        print(f"\n{answer}")

if __name__ == "__main__":
    interactive_recommend()
