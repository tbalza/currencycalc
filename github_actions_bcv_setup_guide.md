# Auto-Updating BCV Rate with GitHub Actions - Complete Setup Guide

## 🚀 What This Does

Your calculator will automatically:
1. **Fetch the official BCV exchange rate daily** (8 AM Venezuelan time)
2. **Store it in your GitHub repo** (free hosting)
3. **Load it automatically** when someone uses your calculator
4. **Work offline** with cached rates

All of this runs **100% FREE** using GitHub Actions!

## 📁 Repository Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── update-bcv.yml          # GitHub Actions workflow
├── scripts/
│   └── update_rate.py              # Python script to fetch rates
├── data/
│   ├── rates.json                  # Full rate history
│   └── current_rate.json           # Simple current rate
├── index.html                      # Your calculator
└── README.md                        # Documentation
```

## 🔧 Step-by-Step Setup

### Step 1: Create a New GitHub Repository

1. Go to https://github.com/new
2. Name it: `venezuela-calculator` (or any name)
3. Make it **Public** (required for GitHub Pages)
4. Initialize with README
5. Create repository

### Step 2: Enable GitHub Pages

1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main
4. Folder: / (root)
5. Save

Your site will be at: `https://yourusername.github.io/venezuela-calculator/`

### Step 3: Create the Folder Structure

In your repository, create these folders:
- Click "Create new file"
- Type: `.github/workflows/update-bcv.yml` (this creates both folders)
- Type: `scripts/update_rate.py`
- Type: `data/current_rate.json`

### Step 4: Add the GitHub Actions Workflow

Create `.github/workflows/update-bcv.yml`:

```yaml
name: Update BCV Exchange Rate

on:
  schedule:
    # Runs at 12:00 PM UTC (8:00 AM VET)
    - cron: '0 12 * * *'
  workflow_dispatch: # Manual trigger button
  push:
    branches: [ main ]

jobs:
  update-rate:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
        
    - name: Install dependencies
      run: |
        pip install requests beautifulsoup4 lxml
        
    - name: Run update script
      run: python scripts/update_rate.py
      
    - name: Commit and push if changed
      run: |
        git config --global user.name 'GitHub Actions Bot'
        git config --global user.email 'actions@github.com'
        git add -A
        timestamp=$(date -u)
        git diff --quiet && git diff --staged --quiet || (git commit -m "Update BCV rate: ${timestamp}" && git push)
```

### Step 5: Add the Python Script

Copy the `update_rate.py` script to `scripts/update_rate.py`

### Step 6: Initialize Data File

Create `data/current_rate.json` with initial data:

```json
{
  "bcv": 40.50,
  "updated": "2025-01-01T12:00:00Z",
  "date": "2025-01-01"
}
```

### Step 7: Add Your Calculator

1. Copy the calculator HTML to `index.html`
2. **IMPORTANT**: Update these lines in the calculator:

```javascript
const CONFIG = {
    githubUser: 'YOUR_USERNAME',     // ← Change to your GitHub username
    githubRepo: 'venezuela-calculator', // ← Change to your repo name
    branch: 'main'
};
```

### Step 8: Test the Workflow

1. Go to Actions tab in your repo
2. Click on "Update BCV Exchange Rate"
3. Click "Run workflow" → "Run workflow"
4. Watch it execute (takes ~30 seconds)
5. Check `data/current_rate.json` - it should be updated!

## 🎯 How It Works

### The Flow:
1. **Every day at 8 AM (VE time)**: GitHub Actions wakes up
2. **Runs Python script**: Fetches BCV rate from multiple sources
3. **Updates JSON file**: Saves to `data/current_rate.json`
4. **Commits changes**: GitHub bot commits the new rate
5. **Calculator fetches**: When opened, reads from your GitHub repo
6. **Falls back gracefully**: Uses cached/default rates if offline

### The Magic:
- **No server needed**: GitHub hosts everything
- **No API keys**: Uses public data sources
- **No costs**: GitHub Actions free tier = 2,000 minutes/month
- **Always current**: Updates automatically every day
- **Works offline**: Caches last known rate

## 🛠️ Customization Options

### Change Update Time
Edit the cron schedule in `.github/workflows/update-bcv.yml`:
```yaml
- cron: '0 12 * * *'  # Current: 12 PM UTC (8 AM VET)
- cron: '0 0 * * *'   # Midnight UTC
- cron: '0 */6 * * *' # Every 6 hours
```

### Add More Exchange Rates
Modify `update_rate.py` to fetch additional sources:
- DolarToday (parallel rate)
- Monitor Dolar
- ExchangeRate-API
- Your bank's rate

### Style Your Calculator
The calculator is fully customizable:
- Change colors in CSS
- Add your logo
- Modify layout
- Add more features

## 🚨 Troubleshooting

### "Actions workflow not running"
- Check Actions tab → May need to enable Actions in Settings
- Workflow only runs on the default branch (main/master)

### "Rate not updating"
- Check Actions tab for error logs
- BCV website might have changed structure
- Fallback to alternative sources in script

### "Calculator shows old rate"
- Browser cache: Hard refresh (Ctrl+F5)
- Check if `data/current_rate.json` is updated in repo
- Verify GitHub username/repo in calculator CONFIG

### "Permission denied error"
Add this to your workflow:
```yaml
permissions:
  contents: write
```

## 📱 Mobile Usage

### For iPhone:
1. Open calculator in Safari
2. Tap Share button
3. "Add to Home Screen"
4. Now it's an app!

### For Android:
1. Open in Chrome
2. Menu → "Add to Home screen"
3. Works like native app

## 🔒 Security Notes

- The bot uses GitHub's token automatically (safe)
- No API keys or secrets needed
- All data sources are public
- Rate limiting: Actions run max once per hour

## 📈 Enhancements You Can Add

1. **Historical Chart**: Show rate trends over time
2. **Multiple Rates**: Add parallel market rates
3. **Notifications**: Email/SMS when rate changes significantly
4. **API Endpoint**: Serve your data as an API
5. **PWA Features**: Make it installable as an app

## 🎉 Success Checklist

- [ ] Repository created and public
- [ ] GitHub Pages enabled
- [ ] Workflow file added
- [ ] Python script added
- [ ] Initial data file created
- [ ] Calculator HTML with your GitHub info
- [ ] Workflow tested manually
- [ ] Calculator loads current rate
- [ ] Bookmarked on phone

## 💡 Pro Tips

1. **Star your repo** - Makes it easy to find
2. **Watch the repo** - Get notified of rate updates
3. **Fork for friends** - They can have their own calculator
4. **Add custom domain** - Use the free domains guide
5. **Create multiple calculators** - One for each currency pair

## 🆘 Need Help?

1. Check the Actions tab for error logs
2. Enable Issues in your repo for troubleshooting
3. The fallback mechanisms ensure it always works
4. Share your repo URL for community help

---

**That's it!** You now have a self-updating currency calculator that:
- Updates daily automatically ✅
- Costs $0 to run ✅  
- Works on any device ✅
- Never needs maintenance ✅

The BCV rate will update every day at 8 AM, and your calculator will always have the latest rate!