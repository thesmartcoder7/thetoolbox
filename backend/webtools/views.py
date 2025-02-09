from rest_framework.decorators import api_view
from rest_framework.response import Response
from webtools.sitemap import SitemapGenerator
from webtools.domain import *
from webtools.page_speed_insights import process_psi_data
from concurrent.futures import ThreadPoolExecutor


@api_view(['POST'])
def generate_sitemap(request):
    generator = SitemapGenerator()
    domain = request.data['domain']
    print(f"Generating Sitemap for {domain}\n")

    sitemap_xml = generator.generate_sitemap(domain)

    print(f"The Sitemap for {domain} has been successfully generated \n")
    return Response({
        "xml": sitemap_xml
    })


@api_view(['POST'])
def domain_check(request):
    domain = request.data['domain']
    print(f'Performing Domain Check on {domain}')
    
    # Create a thread pool to execute tasks concurrently.
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Submit tasks that are independent.
        future_ssl      = executor.submit(get_ssl_certificate, domain)
        future_headers  = executor.submit(check_security_headers, domain)
        future_dns      = executor.submit(get_dns_configuration, domain)
        future_health   = executor.submit(domain_health_check, domain)
        future_whois    = executor.submit(doman_whois, domain)
        # future_icann    = executor.submit(domain_icann_lookup, domain)
        
        # Wait for the SSL certificate result and then process cipher suites.
        ssl_certificate = future_ssl.result()
        cipher_suites = check_cipher_suites(ssl_certificate) if 'error' not in ssl_certificate else {'error': 'Could not retrieve cipher suites'}
        
        security_headers = future_headers.result()
        dns_info         = future_dns.result()
        domain_health    = future_health.result()
        whois_info       = future_whois.result()
        # icann_info       = future_icann.result()
    
    response = {
        'ssl_certificate': ssl_certificate,
        'cipher_suites': cipher_suites,
        'security_headers': security_headers,
        'dns_info': dns_info,
        'domain_check': domain_health,
        'whois_check': whois_info,
        # 'icann_lookup': icann_info
    }
    
    print(f'Domain Check on {domain} has been successfully completed')
    return Response(response)


@api_view(['POST'])
def page_insights(request):
    domain =  request.data['domain']
    response = {}

    print(f'Performing PageSpeed analysis Check on {domain}')

    response = {
        'page_insights': process_psi_data(domain)
    }

    print(f'PageSpeed analysis on {domain} has been successfully completed')

    return Response(response)

