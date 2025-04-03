import os
import socket

def check_domain(domain):
    try:
        # Attempt to resolve the domain name to an IP address
        socket.gethostbyname(domain)
        return True  # Domain exists
    except socket.gaierror:
        return False  # Domain does not exist

def process_domains(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    
    results = []
    for domain in domains:
        exists = check_domain(domain)
        results.append((domain, "Exists" if exists else "Does not exist"))
    
    # Sort so existing domains appear first
    results.sort(key=lambda x: x[1], reverse=True)
    
    with open(output_filename, 'w') as file:
        for domain, status in results:
            file.write(f"{domain} - {status}\n")
    
    print(f"Results saved to {output_filename}")

def main():
    input_filename = input("Enter the path to the domain list file: ").strip()
    
    if not os.path.exists(input_filename):
        print(f"Error: {input_filename} not found.")
        return

    # Extract domain name without TLD for the output file
    domain_name = input_filename.split("\\")[-1].split(".")[0]
    output_filename = os.path.join(os.path.dirname(input_filename), f"{domain_name}_existence_check.txt")
    
    process_domains(input_filename, output_filename)

if __name__ == "__main__":
    main()
