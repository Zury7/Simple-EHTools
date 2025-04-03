import itertools
import os
import random
import string

def generate_typosquatting(domain):
    name, ext = domain.rsplit('.', 1)
    phishing_names = set()
    
    # Common typo patterns
    replacements = {'a': ['@', '4'], 'o': ['0'], 'e': ['3'], 'l': ['1', 'i'], 's': ['5', '$'], 'g': ['9'], 'b': ['8', 'd'], 'd': ['b']}
    
    # Character omission
    for i in range(len(name)):
        phishing_names.add(name[:i] + name[i+1:])
    
    # Character repetition
    for i in range(len(name)):
        phishing_names.add(name[:i] + name[i] + name[i:] )
    
    # Substituting characters with lookalikes
    for i, char in enumerate(name):
        if char in replacements:
            for replacement in replacements[char]:
                phishing_names.add(name[:i] + replacement + name[i+1:])
    
    # Swapping adjacent characters
    for i in range(len(name) - 1):
        swapped = list(name)
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        phishing_names.add("".join(swapped))
    
    # Adding extra characters
    for _ in range(10):  # Generate a few random extra character variations
        extra_char = random.choice(string.ascii_lowercase + string.digits)
        phishing_names.add(name + extra_char)
    
    return list(phishing_names)


def generate_domains_with_tlds(phishing_names, original_tld):
    alternative_tlds = ['com', 'net', 'org', 'info', 'biz', 'co', 'io', 'xyz', 'edu', 'us', 'uk', 'ca', 'au', 'de', 'fr', 'in', 'jp', 'cn']
    phishing_domains = set()
    
    for name in phishing_names:
        for tld in alternative_tlds:
            phishing_domains.add(name + '.' + tld)
        phishing_domains.add(name + '.' + original_tld)
    
    return list(phishing_domains)


def save_to_file(domain, phishing_list):
    filename = f"{domain.replace('.', '_')}_phishing.txt"
    with open(filename, 'w') as file:
        for phishing_name in phishing_list:
            file.write(phishing_name + '\n')
    print(f"Generated phishing names saved to {filename}")


def main():
    domain = input("Enter a domain name (e.g., example.com): ").strip()
    name, ext = domain.rsplit('.', 1)
    phishing_names = generate_typosquatting(domain)
    phishing_domains = generate_domains_with_tlds(phishing_names, ext)
    save_to_file(domain, phishing_domains)


if __name__ == "__main__":
    main()
