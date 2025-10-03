#!/usr/bin/env python3
"""
Fetches the current BCV (Banco Central de Venezuela) exchange rate
and saves it to a JSON file for the calculator to use.
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import sys

def fetch_bcv_rate():
    """
    Fetches the current USD/VES exchange rate from BCV website
    """
    try:
        # BCV website URL
        url = "https://www.bcv.org.ve/"
        
        # Headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the dollar rate - BCV usually shows it prominently
        # The selector might need adjustment based on BCV's current layout
        
        # Method 1: Look for "dolar" text and find nearby number
        dollar_element = soup.find(text=re.compile(r'[Dd][oó]lar', re.IGNORECASE))
        if dollar_element:
            parent = dollar_element.parent
            # Look for rate in parent or siblings
            rate_text = parent.get_text()
            # Extract number with comma as decimal separator (Venezuelan format)
            match = re.search(r'(\d+),(\d+)', rate_text)
            if match:
                rate = float(f"{match.group(1)}.{match.group(2)}")
                return rate
        
        # Method 2: Look for specific div/span with rate
        rate_divs = soup.find_all('div', class_=['centrado', 'pull-right', 'field-content'])
        for div in rate_divs:
            text = div.get_text().strip()
            # Look for pattern like "40,50" or "40.50"
            match = re.search(r'(\d+)[,.](\d+)', text)
            if match:
                rate = float(f"{match.group(1)}.{match.group(2)}")
                if 30 < rate < 100:  # Sanity check for Venezuelan bolivar range
                    return rate
        
        # Method 3: Alternative selector
        strong_tags = soup.find_all('strong')
        for tag in strong_tags:
            text = tag.get_text().strip()
            if 'USD' in text or '$' in text:
                match = re.search(r'(\d+)[,.](\d+)', text)
                if match:
                    rate = float(f"{match.group(1)}.{match.group(2)}")
                    return rate
        
        return None
        
    except Exception as e:
        print(f"Error fetching BCV rate: {e}")
        return None

def fetch_alternative_rates():
    """
    Fetch rates from alternative reliable sources as backup
    """
    rates = {}
    
    # Try to get from exchangerate-api (free tier)
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'rates' in data and 'VES' in data['rates']:
            rates['exchangerate_api'] = data['rates']['VES']
    except:
        pass
    
    # Try to get from another source (example with DolarToday - parallel rate)
    try:
        url = "https://s3.amazonaws.com/dolartoday/data.json"
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'USD' in data and 'dolartoday' in data['USD']:
            rates['dolartoday'] = data['USD']['dolartoday']
    except:
        pass
    
    return rates

def update_rate_file():
    """
    Main function to update the rate file
    """
    # Fetch BCV rate
    bcv_rate = fetch_bcv_rate()
    
    # Fetch alternative rates
    alt_rates = fetch_alternative_rates()
    
    # Prepare data
    data = {
        'timestamp': datetime.utcnow().isoformat(),
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'rates': {
            'bcv': bcv_rate,
            'source': 'BCV Official' if bcv_rate else 'Alternative',
            'last_update': datetime.utcnow().isoformat()
        }
    }
    
    # Add alternative rates if BCV failed
    if not bcv_rate and alt_rates:
        if 'exchangerate_api' in alt_rates:
            data['rates']['bcv'] = alt_rates['exchangerate_api']
            data['rates']['source'] = 'ExchangeRate-API'
    
    # Add all available rates for reference
    data['all_rates'] = {
        'bcv_official': bcv_rate,
        **alt_rates
    }
    
    # Load previous data to maintain history
    try:
        with open('data/rates.json', 'r') as f:
            previous_data = json.load(f)
            if 'history' in previous_data:
                data['history'] = previous_data['history'][-30:]  # Keep last 30 days
            else:
                data['history'] = []
    except:
        data['history'] = []
    
    # Add current rate to history
    data['history'].append({
        'date': data['date'],
        'bcv': bcv_rate if bcv_rate else data['rates']['bcv'],
        'timestamp': data['timestamp']
    })
    
    # Save to JSON file
    with open('data/rates.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Rate updated successfully!")
    print(f"BCV Rate: {data['rates']['bcv']} Bs/$")
    print(f"Source: {data['rates']['source']}")
    print(f"Timestamp: {data['timestamp']}")
    
    # Also save a simple version for easy access
    with open('data/current_rate.json', 'w') as f:
        simple_data = {
            'bcv': data['rates']['bcv'],
            'updated': data['timestamp'],
            'date': data['date']
        }
        json.dump(simple_data, f, indent=2)
    
    return data

if __name__ == "__main__":
    try:
        import os
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Update rates
        update_rate_file()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)