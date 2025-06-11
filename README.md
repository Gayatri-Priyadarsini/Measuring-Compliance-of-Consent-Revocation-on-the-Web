# Measuring Compliance of Consent Revocation on the Web

<link rel="stylesheet" href="assets/css/custom.css">

_Accepted at [PETS 2025](https://petsymposium.org/2025/), Washington DC, July 14–19, 2025_  
[Read the full paper](https://arxiv.org/abs/2411.15414)


Our new study reveals widespread non-compliance with GDPR consent revocation requirements. Just 22.7% of Top 200 sites get consent revocation right! 

### Our Study

Our legal-empirical research paper addressed this gap by analysing consent revocation mechanisms on 200 websites. We assessed their compliance and we have found that: 
- **48%** of websites offer non-compliant revocation interfaces, 
- **57%** of websites continue to store advertising and analytics cookies even after consent has been revoked.

Among the top 200 websites, only 22.7% (36 sites) fully comply with GDPR and ePD in how they handle consent revocation and cookies. Compliance is more common on sites that use Consent Management Platforms (CMPs), so we took a closer look at those.

Out of 281 websites with CMPs, 251 allowed users to revoke consent. We then checked whether:
(1) The website still stored positive consent after revocation, and (2) If they informed third parties of the revocation. 

- **66%** of these 251 websites either kept positive consent after revocation or failed to notify third parties that the consent had been withdrawn.

[Read more about the results on our website](https://gayatri-priyadarsini.github.io/Measuring-Compliance-of-Consent-Revocation-on-the-Web-in-EU/)
---

### Setup

- Clone the repository
```bash
git clone https://github.com/Gayatri-Priyadarsini/Measuring-Compliance-of-Consent-Revocation-on-the-Web.git
```
#### Data collection script: Selenium-Based Setup and Instructions to run fetch_[preferred_OS].py

These scripts are available in the crawler_scripts folder in the repository.

Prerequisites:
- `CookieBlock 1.1.0.0.crx` — Chrome extension for cookie management
- Requirements:
  - Google Chrome browser (with profile support)
  - ChromeDriver binary
  - Python 3.8+
  - Chrome user profile directory (Default)

Setup Instrutions: 
- Ensure Python 3.8+ is installed. Then install required Python packages:
```bash
pip install selenium webdriver-manager
```
- Edit the paths for chrome executable and chromedriver
- Place the extension file CookieBlock 1.1.0.0.crx in the same directory as fetch_linux.py

Running the script:

- python fetch_linux.py
- You will be prompted to enter a target URL (you can also uncomment the script to include a file with list of websites)
- Interact with consent banners manually (e.g., accept, reject, revoke).
- Provide input after each step e.g, (b1, j1, s1, w1, etc.) based on the prompts on the terminal annd the observations made on the website. 

The script: 
- Opens Chrome with the Default profile.
- Collects data (cookies, IndexedDB, localStorage, logs).
- Takes screenshots.
- Saves network requests.
- Repeats this across different consent states.

All results are stored in a new folder named after the domain you entered.

#### Data analysis scripts (available in util_scripts folder)

We use different scripts for analysis purpose (please refer to Fig 2 in the paper for a better picture): 
- The parse_path.py script makes a CSV file from the data collected discussed in the previous section about the interaction with the website. These CSVs were used for data analysis for RQ1 
- The parse_cookies_category_wise.py and cookies_diff.py was used to create CSV files with number of categorised cookies for each website. This CSV was further used to find the difference between the categorised cookies at each stage(initial, acceptance, revocation and rejection) for the data analysis for RQ2.
- The inconsistencies.py produces CSV file with all the data collected discussed in the previous section , specifically, network requests and responses containing TCStrings, cookies and localstorage containing TCStrings and the TCString being returned by the tcfapi(). This CSV was further used for analysis for RQ3 and RQ4. 
