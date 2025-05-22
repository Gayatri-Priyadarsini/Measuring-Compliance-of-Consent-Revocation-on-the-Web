
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

---

### Why This Matters

The General Data Protection Regulation (GDPR) and the ePrivacy Directive (ePD) set out the requirements for obtaining a valid consent when tracking technologies are used on a website. While numerous studies assessed the compliance of consent, one key aspect has been largely overlooked by the research community: consent revocation. According to the GDPR (Art. 7(3), Rec. 42), users have the right to withdraw their consent at any time. Consequently, websites are required to offer a straightforward way to revoke consent. However, it remains unclear whether websites actually provide users with compliant methods to revoke their consent, whether revoked consent is properly recorded, and whether this decision is effectively communicated to third-parties that previously collected the user’s data.

# Key Research Findings

## Finding #1: Non-compliant Revocation Interfaces (48%)
We discovered three major types of non-compliance:

### ❌ 1.1 Absence of Revocation Mechanism (5.6%)

- 9 out of 158 websites provided no way to revoke consent
- 4 websites stored advertising/analytics cookies without consent mechanisms
- Legal impact: Renders entire consent collection invalid

### ⚠️ 1.2 Different, More Complex Interface (20%)

- 32 out of 158 websites used different interfaces for revocation
- Common violations: Email contact required, external platforms, browser settings delegation
- Example: "The only available options are to delete cookies from browser settings"
<p align="center">
  <img src="/images/figure1.png" alt="Figure 1: Different interface to revoke consent " width="500"/>
  <br>
  <em> Consent revocation on https://apple.com, accessed on 20th May 2025. The user can only revoke consent by visiting a privacy policy page and searching for “cookie”, where the only available options are to delete cookies from the browser settings to revoke consent.
</em>
</p>

### ⚠️ 1.3 Different effort to revoke consent than to grant consent (22%)

- 35 out of 158 websites required significantly more steps for revocation
- Typical pattern: One-click consent vs. multi-step revocation through privacy policies
- Creates friction discouraging users from exercising their rights

<p align="center">
  <img src="/images/figure2.png" alt="Figure 2: Different effort to revoke consent than to grant consent " width="500"/>
  <br>
  <em>Consent revocation on http://goo.gl, accessed on 20th May 2025. The user can only revoke consent by visiting a privacy policy page and searching for “cookies”(Step 3), to further look for an option to modify or revoke their consent. In step 7, the user finally reaches the link to open a banner(screenshot not included), which is different from the initial banner(step 1).</em>
</p>

## Finding #2: Cookies Persist Despite Revocation (57.5%)

- ❌ 69 out of 120 websites kept advertising and analytics cookies after revocation
- Indicates continued data collection despite explicit withdrawal of consent due to failure in deletion of existing cookies after revocation action.

## Finding #3: Storage and Communication Issues (66%)

### ⚠️ 3.1 Incorrect Registration (24.6%)

- 47 out of 191 websites showed inconsistent consent registration
- 12-15% continued storing "positive consent" after revocation
- 9-11% never updated consent strings after revocation

### ❌ 3.2 Third-Party Communication Failures (74.2%)

- 101 out of 136 websites failed to notify third parties about revocation
- Third parties continued operating with outdated consent information
- Creates ongoing privacy violations despite user revocation

# Resources

## Research Materials

- **Full Research Paper**: "Measuring Compliance of Consent Revocation on the Web" [Download PDF]
- **Dataset**: Anonymized research data [Download]
- **Presentation Slides**: PETS 2025 Conference [Coming soon]


## About

Will be presenting at **[PETS 2025](https://petsymposium.org/2025/)**  
Washington DC, July 14–19, 2025  
Authors: *Gayatri Priyadarsini Kancherla*, *Nataliia Bielova*, *Cristiana Santos*, *Abhishek Bichhawat*   
[Read the full paper](https://arxiv.org/abs/2411.15414)
