import requests

def fetch_alienvault(domain):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return {entry["hostname"] for entry in data.get("passive_dns", []) if "hostname" in entry}
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching data from AlienVault: {e}")
    return set()

if __name__ == "__main__":
    target_domain = input("Enter the target domain: ").strip()
    subdomains = fetch_alienvault(target_domain)
    
    print(f"\n[+] Subdomains found for {target_domain}:\n")
    for sub in sorted(subdomains):
        print(sub)
