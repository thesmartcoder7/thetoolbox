import ssl
import socket
import requests
import dns.resolver
import smtplib
from datetime import datetime
import whois
import os
import json
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
from dotenv import load_dotenv, find_dotenv
from webtools.datafile import dnsrecords, security_headers

load_dotenv(find_dotenv())


def get_ssl_certificate(domain):
    print("ssl has started working")
    try:
        # Create a socket
        sock = socket.create_connection((domain, 443))

        # Wrap the socket with SSL context
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            # Retrieve the SSL certificate
            cert = ssock.getpeercert()
            return cert
    except Exception as e:
        error = {
            'error': f"Error retrieving SSL certificate for {domain}: {e}"
        }
        return error


def check_cipher_suites(cert):
    print("runing cipher checks")
    try:
        # Get the list of cipher suites supported by the certificate
        cipher_suites = cert.get('cipher')
        
        if cipher_suites:
            return {"suites": cipher_suites}
        else:
            return {'not-found': 'No cipher suites found in the certificate.'}
    except Exception as e:
        return {'error': f"Error checking cipher suites: {e}"}


def check_security_headers(domain):
    print("checking headers")
    # A dictionary mapping header names to their descriptions.
    expected_headers = security_headers.keys()
    unformatted_headers = security_headers
    all_headers={}
    
    try:
        # Send an HTTPS GET request.
        response = requests.get(f"https://{domain}", timeout=10)
        # Check if the request was successful.
        if response.status_code != 200:
            return {'error': f'Request returned status code {response.status_code}'}
        
        # Using response.headers (a case-insensitive dict) to check for headers.
        for header in expected_headers:
            if header in response.headers:
                unformatted_headers[header]['present']='True' 
            else:
                unformatted_headers[header]['present']='False'
            
            all_headers[header] = {
                "header": header,
                "details": unformatted_headers[header]
            }

        return all_headers

    except Exception as e:
        return {'error': f'Error checking security headers: {e}'}


def get_dns_configuration(domain):
    print("checking dns config")
    try:
        # Initialize DNS resolver
        resolver = dns.resolver.Resolver()

        # Define DNS record types to query
        record_types = dnsrecords.keys()

        # Extended details for each record type, including description, importance,
        dns_record_details = dnsrecords
        
        # Store DNS records
        records = {}
        extended_records = {}

        for record_type in record_types:
            try:
                response = resolver.resolve(domain, record_type)
                record_values = [str(rdata) for rdata in response]
                records[record_type] = record_values
            except dns.resolver.NoAnswer:
                records[record_type] = ["No records found"]
            except dns.resolver.NXDOMAIN:
                return {"error": f"Domain {domain} does not exist."}
            except Exception as e:
                records[record_type] = [f"Error retrieving {record_type} Records!"]

            # Combine the actual records with the extended details.
            extended_records[record_type] = {
                "records": records[record_type],
                "details": dns_record_details.get(record_type, {
                    "description": "No details available.",
                    "importance": "N/A",
                    "configuration": "N/A",
                    "resource": "N/A",
                    "security_risks": "N/A"
                })
            }

        return {'dns-records': extended_records}

    except Exception as e:
        return {"error": f"Error retrieving DNS configuration: {e}"}


def domain_health_check(domain):
    print("checking domain health")
    result = {}
    try:
        # DNS resolution check
        dns_resolution = dns.resolver.resolve(domain, 'A')
        result['dns-resolution'] = f"{dns_resolution.response.answer}"

        # SSL certificate check
        with socket.create_connection((domain, 443)) as sock:
            ssl_context = ssl.create_default_context()
            try:
                with ssl_context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        check = {'status': 'success', 'message': 'Certificate Available!'}
                    else:
                        check = {'status': 'fail', 'message': f'Certificate NOT Available! - but SSL handshake was successful!'}
            except ssl.SSLError as e:
                check = {'status': 'fail', 'message': f'Fail! {e}'}

        
        result['ssl-check'] = check

        # Email deliverability check
        mx_records = dns.resolver.resolve(domain, 'MX')
        emails_check = []
        for mx in mx_records:
            try:
                smtp_server = smtplib.SMTP(mx.exchange.to_text(), timeout=10)
                smtp_server.quit()
                emails_check.append({'mx': f'email deliverability to {mx.exchange.to_text()}', 'status': 'success', 'message': 'Success!'}) 
            except Exception as e:
                emails_check.append({'mx': f'email deliverability to {mx.exchange.to_text()}', 'status': 'fail', 'message': f'Error - {e}'})

        result['emails_check'] = emails_check

        # Website accessibility check
        protocols = ["https", "http"]  # Check both HTTPS and HTTP
        response = None

        # Try both protocols and handle exceptions accordingly
        for protocol in protocols:
            try:
                # Perform HEAD request with a specific timeout
                response = requests.head(f"{protocol}://{domain}", timeout=10)
                
                # Check if the status code indicates successful access or redirection
                if response.status_code in [200, 301, 302]:  # Success or redirection status codes
                    result['website-accessibility'] = {
                        'status': 'success',
                        'message': f'Available! Status Code: {response.status_code}'
                    }
                    break  # Exit the loop if the website is accessible
            except Timeout:
                result['website-accessibility'] = {
                    'status': 'fail',
                    'message': f"Timeout Error: Unable to reach {protocol}://{domain} within the time limit."
                }
                break
            except ConnectionError:
                result['website-accessibility'] = {
                    'status': 'fail',
                    'message': f"Connection Error: Unable to establish a connection to {protocol}://{domain}."
                }
            except HTTPError as http_err:
                result['website-accessibility'] = {
                    'status': 'fail',
                    'message': f"HTTP Error: {http_err} while accessing {protocol}://{domain}."
                }
                break  # Exit the loop on HTTP error
            except RequestException as req_err:
                result['website-accessibility'] = {
                    'status': 'fail',
                    'message': f"Request Error: {req_err} while trying to access {protocol}://{domain}."
                }
                break

        # If no success response after trying both protocols, mark as failure
        if not response or response.status_code not in [200, 301, 302]:
            result['website-accessibility'] = {
                'status': 'fail',
                'message': f"Error - HTTP Status Code: {response.status_code if response else 'Unknown'}"
            }

        # Additional checks (you can add more as needed)
        result['error'] = {'status': 'success', 'message': 'Domain check successful'}

    except:
        result['error'] = {'status': 'failed', 'message': 'Domain check failed'}
        ...

    return result
   

def doman_whois(domain):
    print("Running WHOIS lookup...")
    try:
        whois_info = whois.whois(domain)

        # Convert lists to sets to remove duplicates, then back to lists for JSON serialization
        cleaned_whois_info = {
            key: list(set(value)) if isinstance(value, list) else value
            for key, value in whois_info.items()
            if value  # Remove empty values
        }

        return {"whois-info": cleaned_whois_info}
    except Exception as e:
        return {"whois-info": f"No WHOIS info available. Error: {str(e)}"}

def insights(domain):
    print("checking insights")
    url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    results = {}

    response = requests.head(f"https://{domain}", timeout=10)

    if response.status_code == 200 or response.status_code == 301 :
        try:
            
            params = {
                'url': f'https://{domain}' if 'https://' not in domain else domain ,
                'strategy': 'mobile',
                'key': os.getenv('GOOGLE_DEV_KEY'),
                'category': ['performance', 'seo', 'accessibility', 'best-practices']
            }

            res = requests.get(url=url, params=params)
            with open('data.json', 'w') as file:
                json.dump(res.json(), file, indent=4)

            results['mobile'] = res.json()['lighthouseResult']['categories']

            deskparams = {
                'url': f'https://{domain}',
                'strategy': 'desktop',
                'key': os.getenv('GOOGLE_DEV_KEY'),
                'category': ['performance', 'seo', 'accessibility', 'best-practices']
            }
            res = requests.get(url=url, params=deskparams)
            results['desktop'] = res.json()['lighthouseResult']['categories']

            return results
        except:
            return 'error fetching page insights'

    else:
        return None
        


if __name__ == "__main__":
    print("this is not the main file")
    # domain = "samuel-martins.com"
    # certificate = get_ssl_certificate(domain)
    # check_cipher_suites(certificate)
    # check_security_headers(domain)
    # get_dns_configuration(domain)
    # domain_health_check(domain)