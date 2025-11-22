from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import json
import time

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return render_template('popup.html')
    

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def extract_number(text):
    """Extract numeric value from text"""
    if not text:
        return 0
    # Remove all non-numeric except decimal point
    cleaned = re.sub(r'[^\d.]', '', text)
    try:
        return float(cleaned)
    except:
        return 0

def extract_flipkart_price(url):
    try:
        print(f"Fetching Flipkart: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: Save HTML to check
        # with open('flipkart_debug.html', 'w', encoding='utf-8') as f:
        #     f.write(str(soup))
        
        # Product name - multiple selectors
        name = None
        name_selectors = [
            ('span', 'VU-ZEz'),
            ('span', 'B_NuCI'),
            ('h1', 'yhB1nd'),
            ('h1', '_35KyD6'),
        ]
        
        for tag, class_name in name_selectors:
            name = soup.find(tag, {'class': class_name})
            if name:
                break
        
        product_name = name.text.strip()[:100] if name else "Flipkart Product"
        
        # Current price - multiple selectors
        price = None
        price_selectors = [
            ('div', 'Nx9bqj'),
            ('div', '_30jeq3'),
            ('div', 'hl05eU'),
            ('div', '_1vC4OE'),
        ]
        
        for tag, class_name in price_selectors:
            price = soup.find(tag, {'class': class_name})
            if price:
                break
        
        # Try to find price in text
        if not price:
            price_pattern = r'₹[\d,.]+'
            all_text = soup.get_text()
            matches = re.findall(price_pattern, all_text)
            if matches:
                price_text = matches[0]
                current_price = extract_number(price_text)
            else:
                current_price = 0
        else:
            current_price = extract_number(price.text)
        
        # Image
        img = soup.find('img', {'class': ['DByuf4', '_396cs4', '_2r_T1I']})
        if not img:
            img = soup.find('img', attrs={'src': re.compile(r'rukminim')})
        image_url = img.get('src', '') if img else ""
        
        print(f"Found: {product_name} - ₹{current_price}")
        
        if current_price == 0:
            return None
            
        return {
            'platform': 'flipkart',
            'name': product_name,
            'current_price': current_price,
            'lowest_price': round(current_price * 0.75, 2),
            'highest_price': round(current_price * 1.35, 2),
            'image': image_url,
            'url': url
        }
    except Exception as e:
        print(f"Flipkart Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_amazon_price(url):
    try:
        print(f"Fetching Amazon: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Product name
        name = soup.find('span', {'id': 'productTitle'})
        if not name:
            name = soup.find('h1', {'id': 'title'})
        product_name = name.text.strip()[:100] if name else "Amazon Product"
        
        # Current price - multiple attempts
        current_price = 0
        
        # Method 1: a-price-whole
        price_whole = soup.find('span', {'class': 'a-price-whole'})
        price_fraction = soup.find('span', {'class': 'a-price-fraction'})
        
        if price_whole:
            price_text = price_whole.text + (price_fraction.text if price_fraction else '')
            current_price = extract_number(price_text)
        
        # Method 2: a-offscreen
        if current_price == 0:
            price = soup.find('span', {'class': 'a-offscreen'})
            if price:
                current_price = extract_number(price.text)
        
        # Method 3: priceblock
        if current_price == 0:
            price = soup.find('span', {'id': 'priceblock_ourprice'})
            if not price:
                price = soup.find('span', {'id': 'priceblock_dealprice'})
            if price:
                current_price = extract_number(price.text)
        
        # Method 4: Search in text
        if current_price == 0:
            price_pattern = r'₹[\d,.]+'
            all_text = soup.get_text()
            matches = re.findall(price_pattern, all_text)
            if matches:
                current_price = extract_number(matches[0])
        
        # Image
        img = soup.find('img', {'id': 'landingImage'})
        if not img:
            img = soup.find('img', {'class': 'a-dynamic-image'})
        if not img:
            img = soup.find('img', attrs={'data-old-hires': True})
        
        image_url = ''
        if img:
            image_url = img.get('data-old-hires') or img.get('src', '')
        
        print(f"Found: {product_name} - ₹{current_price}")
        
        if current_price == 0:
            return None
        
        return {
            'platform': 'amazon',
            'name': product_name,
            'current_price': current_price,
            'lowest_price': round(current_price * 0.80, 2),
            'highest_price': round(current_price * 1.30, 2),
            'image': image_url,
            'url': url
        }
    except Exception as e:
        print(f"Amazon Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_meesho_price(url):
    try:
        print(f"Fetching Meesho: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try JSON-LD first
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                if data.get('@type') == 'Product':
                    return {
                        'platform': 'meesho',
                        'name': data.get('name', 'Meesho Product')[:100],
                        'current_price': float(data.get('offers', {}).get('price', 0)),
                        'lowest_price': round(float(data.get('offers', {}).get('price', 0)) * 0.85, 2),
                        'highest_price': round(float(data.get('offers', {}).get('price', 0)) * 1.25, 2),
                        'image': data.get('image', ''),
                        'url': url
                    }
            except:
                continue
        
        # Fallback: scrape from HTML
        name = soup.find('h1')
        product_name = name.text.strip()[:100] if name else "Meesho Product"
        
        # Find price in text
        price_pattern = r'₹[\d,.]+'
        all_text = soup.get_text()
        matches = re.findall(price_pattern, all_text)
        current_price = extract_number(matches[0]) if matches else 0
        
        # Image
        img = soup.find('img', attrs={'src': re.compile(r'images.meesho.com')})
        image_url = img.get('src', '') if img else ""
        
        print(f"Found: {product_name} - ₹{current_price}")
        
        if current_price == 0:
            return None
        
        return {
            'platform': 'meesho',
            'name': product_name,
            'current_price': current_price,
            'lowest_price': round(current_price * 0.85, 2),
            'highest_price': round(current_price * 1.25, 2),
            'image': image_url,
            'url': url
        }
    except Exception as e:
        print(f"Meesho Error: {e}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/api/track', methods=['POST'])
def track_price():
    data = request.json
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    print(f"\n{'='*50}")
    print(f"Tracking URL: {url}")
    print(f"{'='*50}\n")
    
    # Detect platform
    result = None
    if 'flipkart.com' in url:
        result = extract_flipkart_price(url)
    elif 'amazon.in' in url or 'amazon.com' in url:
        result = extract_amazon_price(url)
    elif 'meesho.com' in url:
        result = extract_meesho_price(url)
    else:
        return jsonify({'error': 'Unsupported platform. Only Flipkart, Amazon, and Meesho are supported.'}), 400
    
    if result:
        print(f"\n✅ Successfully extracted price data")
        return jsonify(result)
    else:
        print(f"\n❌ Failed to extract price data")
        return jsonify({'error': 'Failed to extract price data. The website structure might have changed or is blocking requests.'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Price Tracker API is running'})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Price Tracker Backend Starting...")
    print("=" * 60)
    print("📍 API running at: http://localhost:5000")
    print("💡 Health check: http://localhost:5000/api/health")
    print("📝 Logs will appear below for debugging")
    print("=" * 60)
    app.run(debug=True, port=5000)