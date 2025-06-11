# Artifact Appendix

Paper title: **Johnny Can’t Revoke Consent Either:Measuring Compliance of Consent Revocation on the Web**

Artifacts HotCRP Id: **39** (not your paper Id, but the artifacts id)

Requested Badge: **Available**

## Description
This repository contains the scripts and datasets(links incase of bigger datasets) and results discussed in our paper. 

### Security/Privacy Issues and Ethical Concerns (All badges)
None

## Basic Requirements (Only for Functional and Reproduced badges)
A standard laptop or desktop with at least 4 GB RAM and a 1-core CPU.

### Hardware Requirements
None

### Software Requirements
Code for Linux and Windows is available.Should be easily reproduced for MAC as well. 

### Estimated Time and Storage Consumption
Crawling a website takes around 1 minute on average. The data being collected per website is around 50-80MB. Total space and time would vary based on the number of websites being crawled.  


## Environment 


### Accessibility (All badges)
https://github.com/Gayatri-Priyadarsini/Measuring-Compliance-of-Consent-Revocation-on-the-Web/tree/main


### Set up the environment (Only for Functional and Reproduced badges)

- Clone the repository
```bash
git clone https://github.com/Gayatri-Priyadarsini/Measuring-Compliance-of-Consent-Revocation-on-the-Web.git
```
#### Data collection script: Selenium-Based Setup and Instructions to run fetch_[preferred_OS].py

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

#### Data analysis scripts

### Testing the Environment (Only for Functional and Reproduced badges)
Verifying the setup:
- Chrome launches with your profile and the extension loaded.
- A new folder (named after the domain) is created.
- Files generated:
- - browsing_data0.json to browsing_data3.json
- - res0.json to res3.json
- - screenshot0.png to screenshot3.png
- - path.txt

## Artifact Evaluation (Only for Functional and Reproduced badges)

Our work analyses consent revocation mechanisms on 200 websites. We assessed their compliance and we have found that: 
- **48%** of websites offer non-compliant revocation interfaces (**RQ1**), 
- **57%** of websites continue to store advertising and analytics cookies even after consent has been revoked (**RQ2**).

Among the top 200 websites, only 22.7% (36 sites) fully comply with GDPR and ePD in how they handle consent revocation and cookies. Compliance is more common on sites that use Consent Management Platforms (CMPs), so we took a closer look at those.

Out of 281 websites with CMPs, 251 allowed users to revoke consent. We then checked whether:
(1) The website still stored positive consent after revocation(**RQ3**), and (2) If they informed third parties of the revocation (**RQ4**).

- **66%** of these 251 websites either kept positive consent after revocation or failed to notify third parties that the consent had been withdrawn.

We include the list of websites, per violation in the "possible violations" folder. 

### Experiments 

We use different scripts(available in util_scripts folder) for analysis purpose (please refer to Fig 2 in the paper for a better picture): 
- The parse_path.py script makes a CSV file from the data collected discussed in the previous section about the interaction with the website. These CSVs were used for data analysis for RQ1 
- The parse_cookies_category_wise.py and cookies_diff.py was used to create CSV files with number of categorised cookies for each website. This CSV was further used to find the difference between the categorised cookies at each stage(initial, acceptance, revocation and rejection) for the data analysis for RQ2.
- The inconsistencies.py produces CSV file with all the data collected discussed in the previous section , specifically, network requests and responses containing TCStrings, cookies and localstorage containing TCStrings and the TCString being returned by the tcfapi(). This CSV was further used for analysis for RQ3 and RQ4. 
...


## Notes on Reusability (Only for Functional and Reproduced badges)

While the legal results are specific to GDPR, we believe that the work provides insights on how websites handle revocation, generally. With a legal expert in other regulations, the results may be used to identify compliance. However, websites behave differently under different regulations, which would require data collection for which our interface analysis methodology can still be used.
