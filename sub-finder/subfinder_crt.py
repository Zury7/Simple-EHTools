import requests
from bs4 import BeautifulSoup

def find_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        subdomains = set(entry["name_value"] for entry in data)
        
        print(f"\n[+] Subdomains found for {domain}:\n")
        for sub in sorted(subdomains):
            print(sub)
    
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching data: {e}")

if __name__ == "__main__":
    target_domain = input("Enter the target domain: ").strip()
    find_subdomains(target_domain)
