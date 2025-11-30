💰 Price Tracker Chrome Extension
A powerful Chrome extension to track and compare product prices across Flipkart, Amazon, and Meesho in real-time.

✨ Features

🔍 Real-time Price Tracking - Get current prices instantly
📊 Price Comparison - View lowest and highest prices
🏪 Multi-platform Support - Flipkart, Amazon, Meesho
🎨 Beautiful UI - Stunning gradient design with smooth animations
📱 Responsive - Works on all screen sizes
🔔 Status Indicator - Know when backend is online/offline
⚡ Fast & Lightweight - Quick price extraction
💾 History Tracking - Stores last 20 tracked products
🎯 Smart Filters - Filter by platform

🖼️ Screenshots
Extension Popup

Beautiful gradient UI with glassmorphism effects
Real-time backend status indicator
Quick product tracking interface

Price Cards

Current price display

Lowest/Highest price comparison

Deal status badges (Great Deal/Fair/High Price)

Direct links to products

🚀 Installation
Prerequisites

Python 3.7 or higher
Google Chrome browser
pip (Python package manager)

Step 1: Clone or Download
bash# Clone the repository (or download ZIP)
https://github.com/sarjanthecoder/CHROME-extension-product-price-tracker-in-flipkart-amazon-meesho-.git
cd price-tracker-extension
Step 2: Install Python Dependencies
bashpip install flask flask-cors requests beautifulsoup4
Step 3: Project Structure
Create the following files in your project folder:
price-tracker-extension/
│
├── app.py                 # Backend Flask server
├── popup.html            # Extension UI
├── manifest.json         # Chrome extension config
├── icon.png             # Extension icon (128x128)
└── README.md            # This file
Step 4: Create manifest.json
json{
  "manifest_version": 3,
  "name": "Price Tracker",
  "version": "1.0.0",
  "description": "Track and compare prices across Flipkart, Amazon, and Meesho",
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icon.png",
      "48": "icon.png",
      "128": "icon.png"
    }
  },
  "permissions": [
    "activeTab"
  ],
  "host_permissions": [
    "http://localhost:5000/*"
  ],
  "icons": {
    "16": "icon.png",
    "48": "icon.png",
    "128": "icon.png"
  }
}
Step 5: Add Extension to Chrome

Open Chrome and go to chrome://extensions/
Enable Developer mode (toggle in top-right)
Click Load unpacked
Select your price-tracker-extension folder
Extension installed! ✅

📖 Usage
Starting the Backend

Open terminal in project folder
Run the Flask server:

bashpython app.py

You should see:

🚀 Price Tracker Backend Starting...
📍 API running at: http://localhost:5000
💡 Health check: http://localhost:5000/api/health
Using the Extension

Click the extension icon in Chrome toolbar
Check status - Green dot means backend is online
Copy product URL from Flipkart/Amazon/Meesho
Paste URL in the input field
Click "Track" button
View results - Price, comparison, and deal status

Supported URLs
✅ Flipkart: https://www.flipkart.com/product-name/p/...
✅ Amazon: https://www.amazon.in/product-name/dp/...
✅ Meesho: https://www.meesho.com/product-name/p/...
Filter by Platform
Click platform buttons to filter tracked products:

All - Show all products
Flipkart - Only Flipkart products
Amazon - Only Amazon products
Meesho - Only Meesho products

🛠️ Technical Details
Backend (Flask)

Framework: Flask + Flask-CORS
Scraping: BeautifulSoup4 + Requests
Port: 5000 (default)
API Endpoints:

GET /api/health - Health check
POST /api/track - Track product price



Frontend (Chrome Extension)

HTML5 + CSS3 - Modern responsive design
Vanilla JavaScript - No dependencies
Features:

Glassmorphism UI effects
CSS animations
Responsive media queries
Touch device optimization



Price Estimation

Current Price: Scraped from product page
Lowest Price: Current × 0.75-0.85 (estimated)
Highest Price: Current × 1.25-1.35 (estimated)

Note: Lowest/Highest prices are estimates. For historical tracking, integrate with price tracking APIs.
⚙️ Configuration
Change Backend Port
In app.py:
pythonapp.run(debug=True, port=5000)  # Change 5000 to your port
In popup.html:
javascriptconst API_URL = 'http://localhost:5000/api';  // Update port
Adjust Price Estimation
In app.py, modify multipliers:
python'lowest_price': round(current_price * 0.75, 2),   # 25% discount
'highest_price': round(current_price * 1.35, 2),  # 35% markup
🐛 Troubleshooting
Backend Offline Error
Problem: Red status dot, "Backend offline" message
Solutions:

Make sure Python server is running: python app.py
Check if port 5000 is available
Check firewall settings
Try accessing: http://localhost:5000/api/health

Failed to Extract Price
Problem: "Failed to extract price data" error
Reasons:

Website structure changed (common)
Website blocking requests
Invalid URL format
Network connectivity issues

Solutions:

Check terminal logs for detailed errors
Try different product URLs
Update scraping selectors in app.py
Add delay between requests

CORS Errors
Problem: Cross-origin request blocked
Solution: Flask-CORS is already configured, but ensure:
pythonfrom flask_cors import CORS
CORS(app)
Extension Not Showing
Problem: Extension icon not visible in toolbar
Solutions:

Check if extension is enabled in chrome://extensions/
Pin the extension (puzzle icon → pin)
Reload the extension

🔧 Advanced Features
Add Price History Tracking
Integrate with database (SQLite/MongoDB) to store historical prices:
python# Example with SQLite
import sqlite3

def save_price_history(product_url, price):
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO price_history (url, price, timestamp)
        VALUES (?, ?, datetime('now'))
    ''', (product_url, price))
    conn.commit()
    conn.close()
Add Price Alerts
Send notifications when price drops below threshold:
pythondef check_price_alert(current_price, target_price):
    if current_price <= target_price:
        # Send notification
        return True
    return False
Use Price Tracking APIs
For accurate historical data, use APIs:

Keepa API - Amazon price tracking
PriceAPI - Multi-platform
RapidAPI Price Tracking

📝 API Documentation
POST /api/track
Request:
json{
  "url": "https://www.flipkart.com/product/..."
}
Response (Success):
json{
  "platform": "flipkart",
  "name": "Product Name",
  "current_price": 1299.00,
  "lowest_price": 974.25,
  "highest_price": 1753.65,
  "image": "https://...",
  "url": "https://..."
}
Response (Error):
json{
  "error": "Error message"
}
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
⚠️ Disclaimer
This tool is for educational purposes only. Web scraping may violate terms of service of e-commerce websites. Use responsibly and respect robots.txt. The developers are not responsible for any misuse.
🙏 Acknowledgments

BeautifulSoup4 for HTML parsing
Flask for backend framework
Chrome Extensions API
Unsplash for placeholder images

📧 Support
For issues, questions, or suggestions:

Open an issue on GitHub
Email: sarjan6325@gmail.com

🗺️ Roadmap

 Add price history charts
 Email/SMS price alerts
 Support for more e-commerce sites
 Price drop predictions with ML
 Export price data to CSV
 Dark/Light theme toggle
 Multi-language support
 Browser sync across devices


Made with ❤️ by [sarjan p]
Star ⭐ this repo if you find it useful!
<h1>DISCLAIMER</h1>:   this is for only  demo puposes  dont pay your here if any missuses or lose we csnt a responsibility to u .

