Accompanying [blog post](https://medium.com/@analyticsoul/eb0e968b00c1)

## Step -1: Environment setup
```bash
python3 -m venv venv
source venv/Scripts/activate
pip install -r .\requirements.txt

mkdir driver profile_html scraped_data clean_data
```

Download the Selenium Chrome webdriver from [here](https://chromedriver.chromium.org/downloads) and store it to the *"driver"* folder.

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

## Step 4: Data Visualization
You can find the Tableau workbook [here](https://medium.com/r/?url=https%3A%2F%2Fpublic.tableau.com%2Fviews%2FLinkedInProfileAnalysis_16541209594500%2FDashboard%3F%3Alanguage%3Den-US%26%3Adisplay_count%3Dn%26%3Aorigin%3Dviz_share_link)
