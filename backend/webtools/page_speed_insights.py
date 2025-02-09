import requests
import json
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv('GOOGLE_DEV_KEY')
URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'


def convert_timestamp(timestamp):
    # Parse the original timestamp
    dt = datetime.fromisoformat(timestamp[:-1])
    
    # Define suffixes for day of the month
    suffixes = {1: 'st', 2: 'nd', 3: 'rd', 21: 'st', 22: 'nd', 23: 'rd', 31: 'st'}
    suffix = suffixes.get(dt.day, 'th')
    
    # Format the date
    date_str = dt.strftime(f"%a, %B {dt.day}{suffix}, %Y")
    
    # Format the time
    time_str = dt.strftime("%I:%M%p").lower()
    
    # Combine date and time
    formatted_str = f"{date_str} at {time_str}"
    
    return formatted_str


def fetch_psi_data(domain, strategy):
    print(f'fetching data for {strategy}')
    try:
        params = {
            'url': f'https://{domain}' if 'https://' not in domain else domain,
            'key': API_KEY,
            'strategy': strategy,
            'category': ['performance', 'accessibility', 'seo', 'best-practices', 'pwa']
        }
        response = requests.get(URL, params=params)
    except Exception:
        params = {
            'url': f'http://{domain}' if 'http://' not in domain else domain,
            'key': API_KEY,
            'strategy': strategy,
            'category': ['performance', 'accessibility', 'seo', 'best-practices', 'pwa']
        }
        response = requests.get(URL, params=params)
    return response.json()


def calculate_overall_score(categories):
    total_score = 0
    count = 0
    for category in categories.values():
        if 'score' in category:
            total_score += category['score'] * 100  # Scores are between 0 and 1
            count += 1
    return total_score / count if count else 0


def custom_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def categorize_audits(audits, categories):
    # Create a dictionary for quick lookup of audit data by their IDs
    audit_lookup = {audit_id: audit for audit_id, audit in audits.items()}

    categorized_audits = {}
    for cat_key, cat_value in categories.items():
        categorized_audits[cat_value['title']] = []
        for audit_ref in cat_value['auditRefs']:
            audit_id = audit_ref['id']
            if audit_id in audit_lookup:
                audit = audit_lookup[audit_id]
                if audit['scoreDisplayMode'] == 'numeric' and 'score' in audit:
                    audit['score'] = audit['score'] * 100
                categorized_audits[cat_value['title']].append(audit)
    return categorized_audits


def extract_main_categories(categories):
    main_categories = {}
    for cat_key, cat_value in categories.items():
        main_categories[cat_key] = {
            'id': cat_value['id'],
            'title': cat_value['title'],
            'score': cat_value['score'] * 100,  # Convert to percentage
            'description': cat_value.get('description', ''),
            'manualDescription': cat_value.get('manualDescription', '')
        }
    return main_categories


def process_psi_data(domain):
    # Use ThreadPoolExecutor to run mobile and desktop API calls concurrently.
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_mobile = executor.submit(fetch_psi_data, domain, 'mobile')
        future_desktop = executor.submit(fetch_psi_data, domain, 'desktop')
        mobile_data = future_mobile.result()
        desktop_data = future_desktop.result()

    overall_mobile = calculate_overall_score(mobile_data['lighthouseResult']['categories'])
    overall_desktop = calculate_overall_score(desktop_data['lighthouseResult']['categories'])
    overall_avg = (overall_mobile + overall_desktop) / 2

    final_results = {
        'domain': domain,
        'checkTime': convert_timestamp(datetime.utcnow().isoformat() + 'Z'),
        'overalScore': overall_avg,
        'grade': custom_grade(overall_avg),
        'screenshots': [
            mobile_data['lighthouseResult']['audits']['final-screenshot']['details']['data'],
            desktop_data['lighthouseResult']['audits']['final-screenshot']['details']['data']
        ],
        'results': {
            'mobile': extract_main_categories(mobile_data['lighthouseResult']['categories']),
            'desktop': extract_main_categories(desktop_data['lighthouseResult']['categories'])
        },
        'audits': {
            'mobile': categorize_audits(mobile_data['lighthouseResult']['audits'],
                                         mobile_data['lighthouseResult']['categories']),
            'desktop': categorize_audits(desktop_data['lighthouseResult']['audits'],
                                          desktop_data['lighthouseResult']['categories'])
        }
    }

    return final_results


if __name__ == "__main__":
    domain = 'https://samuel-martins.com'
    final_results = process_psi_data(domain)
    print(json.dumps(final_results, indent=2))
