# subfinder-final.py

import re
from subfinder_alienvault import fetch_alienvault
from subfinder_crt import find_subdomains
from subfinder_htarget import fetch_hackertarget
from subfinder_threatcrowd import fetch_threatcrowd

def save_subdomains_to_file(domain, subdomains):
    # Use a set to remove duplicates before saving
    unique_subdomains = set(subdomains)
    
    # Sanitize domain name to be used as a valid file name (remove invalid characters)
    sanitized_domain = re.sub(r'[^a-zA-Z0-9_-]', '_', domain)

    # Create the file name dynamically based on the domain name
    filename = f"{sanitized_domain}_subdomains.txt"
    
    with open(filename, "w") as f:  # Use "w" to overwrite the file for each new domain
        f.write(f"Subdomains for {domain}:\n")
        for subdomain in unique_subdomains:
            f.write(f"{subdomain}\n")
        f.write("\n")  # Newline after each domain's subdomains

def main():
    domain = input("Enter the target domain: ")

    # Initialize an empty list to store all subdomains
    all_subdomains = []

    # Get subdomains from AlienVault
    subdomains_alienvault = fetch_alienvault(domain)
    if subdomains_alienvault:
        print(f"Found subdomains from AlienVault for {domain}:")
        print(subdomains_alienvault)
        all_subdomains.extend(subdomains_alienvault)

    # Get subdomains from CRT.sh
    subdomains_crt = find_subdomains(domain)
    if subdomains_crt:
        print(f"Found subdomains from CRT.sh for {domain}:")
        print(subdomains_crt)
        all_subdomains.extend(subdomains_crt)

    # Get subdomains from HackerTarget
    subdomains_htarget = fetch_hackertarget(domain)
    if subdomains_htarget:
        print(f"Found subdomains from HackerTarget for {domain}:")
        print(subdomains_htarget)
        all_subdomains.extend(subdomains_htarget)

    # Get subdomains from ThreatCrowd
    subdomains_threatcrowd = fetch_threatcrowd(domain)
    if subdomains_threatcrowd:
        print(f"Found subdomains from ThreatCrowd for {domain}:")
        print(subdomains_threatcrowd)
        all_subdomains.extend(subdomains_threatcrowd)

    # Save the subdomains to a file, ensuring no duplicates
    if all_subdomains:
        save_subdomains_to_file(domain, all_subdomains)

    print(f"Results saved to {domain}_subdomains.txt")

if __name__ == "__main__":
    main()
