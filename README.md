
## Step -1: Python environment setup with venv
```bash
python3 -m venv venv
source venv/Scripts/activate
pip install -r .\requirements.txt
```

## Step 0: Store LinkedIn authentication in a config file
- Rename "sample.ini" to "config.ini"
- Update username and password config variables with your LinkedIn profile credentials

## Step 1: Download interesting profiles
```bash
cd scraper
python3 fetch_profile_urls.py
python3 download_profile_pages.py
```

After this step, you should have html profile pages downloaded in the "profile_html" directory.

## Step 2: Scrap profile data with BeautifulSoup
```bash
python3 scrap_profile_data.py
```

## Step 3: Data preparation
For data cleaning and preparation I used the "data-preparation.ipynb" jupyter notebook.
