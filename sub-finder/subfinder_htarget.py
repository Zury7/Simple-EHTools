import requests

def fetch_hackertarget(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return {line.split(',')[0] for line in response.text.splitlines()}
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching data from HackerTarget: {e}")
    return set()

if __name__ == "__main__":
    target_domain = input("Enter the target domain: ").strip()
    subdomains = fetch_hackertarget(target_domain)
    
    print(f"\n[+] Subdomains found for {target_domain}:\n")
    for sub in sorted(subdomains):
        print(sub)
