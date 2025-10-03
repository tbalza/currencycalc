// Alternative Node.js script for fetching BCV rate
// Use this instead of Python if you prefer JavaScript

const https = require('https');
const fs = require('fs');
const path = require('path');

// Ensure data directory exists
const dataDir = path.join(__dirname, '..', 'data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
}

// Function to make HTTPS requests
function fetchUrl(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}

// Fetch rate from ExchangeRate-API (free tier)
async function fetchExchangeRateAPI() {
    try {
        const data = await fetchUrl('https://api.exchangerate-api.com/v4/latest/USD');
        const json = JSON.parse(data);
        if (json.rates && json.rates.VES) {
            return json.rates.VES;
        }
    } catch (error) {
        console.error('ExchangeRate-API error:', error.message);
    }
    return null;
}

// Fetch rate from alternative source (DolarToday)
async function fetchDolarToday() {
    try {
        const data = await fetchUrl('https://s3.amazonaws.com/dolartoday/data.json');
        const json = JSON.parse(data);
        if (json.USD && json.USD.promedio_real) {
            return json.USD.promedio_real;
        }
    } catch (error) {
        console.error('DolarToday error:', error.message);
    }
    return null;
}

// Simple BCV scraper (may need adjustment based on site structure)
async function fetchBCVRate() {
    try {
        const html = await fetchUrl('https://www.bcv.org.ve/');
        
        // Look for USD rate in the HTML
        // This regex pattern may need adjustment
        const rateMatch = html.match(/USD.*?(\d+)[,.](\d+)/i);
        if (rateMatch) {
            return parseFloat(`${rateMatch[1]}.${rateMatch[2]}`);
        }
        
        // Alternative pattern
        const altMatch = html.match(/d[oó]lar.*?(\d+)[,.](\d+)/i);
        if (altMatch) {
            return parseFloat(`${altMatch[1]}.${altMatch[2]}`);
        }
    } catch (error) {
        console.error('BCV fetch error:', error.message);
    }
    return null;
}

// Main function
async function updateRates() {
    console.log('🔄 Fetching exchange rates...');
    
    // Try to fetch from multiple sources
    const [bcvRate, exchangeApiRate, dolarTodayRate] = await Promise.all([
        fetchBCVRate(),
        fetchExchangeRateAPI(),
        fetchDolarToday()
    ]);
    
    // Use BCV rate if available, otherwise fall back to alternatives
    let finalRate = bcvRate || exchangeApiRate || dolarTodayRate || 40.50;
    let source = bcvRate ? 'BCV Official' : 
                 exchangeApiRate ? 'ExchangeRate-API' : 
                 dolarTodayRate ? 'DolarToday' : 'Fallback';
    
    const now = new Date();
    
    // Prepare data
    const currentData = {
        bcv: finalRate,
        updated: now.toISOString(),
        date: now.toISOString().split('T')[0]
    };
    
    const fullData = {
        timestamp: now.toISOString(),
        date: now.toISOString().split('T')[0],
        rates: {
            bcv: finalRate,
            source: source,
            last_update: now.toISOString()
        },
        all_rates: {
            bcv_official: bcvRate,
            exchange_api: exchangeApiRate,
            dolar_today: dolarTodayRate
        },
        history: []
    };
    
    // Load existing history
    const historyFile = path.join(dataDir, 'rates.json');
    if (fs.existsSync(historyFile)) {
        try {
            const existing = JSON.parse(fs.readFileSync(historyFile, 'utf8'));
            if (existing.history) {
                fullData.history = existing.history.slice(-29); // Keep last 29 entries
            }
        } catch (e) {
            console.error('Error reading history:', e.message);
        }
    }
    
    // Add current rate to history
    fullData.history.push({
        date: fullData.date,
        bcv: finalRate,
        timestamp: fullData.timestamp
    });
    
    // Save files
    fs.writeFileSync(
        path.join(dataDir, 'current_rate.json'),
        JSON.stringify(currentData, null, 2)
    );
    
    fs.writeFileSync(
        path.join(dataDir, 'rates.json'),
        JSON.stringify(fullData, null, 2)
    );
    
    console.log('✅ Rates updated successfully!');
    console.log(`📊 BCV Rate: ${finalRate.toFixed(2)} Bs/$`);
    console.log(`📍 Source: ${source}`);
    console.log(`🕐 Timestamp: ${now.toISOString()}`);
    
    // Log all rates for debugging
    console.log('\n📈 All fetched rates:');
    console.log(`  BCV Official: ${bcvRate || 'N/A'}`);
    console.log(`  ExchangeRate-API: ${exchangeApiRate || 'N/A'}`);
    console.log(`  DolarToday: ${dolarTodayRate || 'N/A'}`);
}

// Run the update
updateRates().catch(error => {
    console.error('❌ Fatal error:', error);
    process.exit(1);
});