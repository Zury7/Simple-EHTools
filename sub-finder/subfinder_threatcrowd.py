import requests

def fetch_threatcrowd(domain):
    url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
    
    try:
        response = requests.get(url, timeout=10, verify=False)
        
        # Print the HTTP status code and response content for debugging
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response Text: {response.text[:500]}")  # Print first 500 characters of the response
        
        # Check if the response was successful
        if response.status_code == 200:
            try:
                # Try to parse the JSON data
                data = response.json()
                
                # Print the parsed JSON to check its structure
                print(f"JSON Data: {data}")
                
                # Extract subdomains if available
                return set(data.get("subdomains", []))
            except ValueError:
                print("Error: Failed to parse JSON response.")
        else:
            print(f"Error: Received status code {response.status_code} from ThreatCrowd API.")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching data from ThreatCrowd: {e}")
    
    # Return an empty set if there was an issue
    return set()

if __name__ == "__main__":
    target_domain = input("Enter the target domain: ").strip()
    subdomains = fetch_threatcrowd(target_domain)
    
    print(f"\n[+] Subdomains found for {target_domain}:\n")
    for sub in sorted(subdomains):
        print(sub)
