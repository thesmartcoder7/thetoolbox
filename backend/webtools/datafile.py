dnsrecords = {
    'A': {
        'description': "Maps a domain name to an IPv4 address.",
        'importance': "Essential for basic connectivity.",
        'configuration': "Ensure this record points to the correct public IPv4 address.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-a-record/",
        'security_risks': "Incorrect A records can lead to misdirected traffic or service disruption.",
        'category': "Essential"
    },
    'AAAA': {
        'description': "Maps a domain name to an IPv6 address.",
        'importance': "Necessary for IPv6 connectivity.",
        'configuration': "Ensure this record points to the correct public IPv6 address.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-aaaa-record/",
        'security_risks': "Misconfiguration may cause connectivity issues for IPv6 users.",
        'category': "Essential"
    },
    'CNAME': {
        'description': "Aliases one domain name to another.",
        'importance': "Used for subdomain aliasing and simplifying DNS management.",
        'configuration': "Should point to the canonical (primary) domain name.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-cname-record/",
        'security_risks': "Improper CNAME setup can cause redirection errors or downtime.",
        'category': "Optional"
    },
    'MX': {
        'description': "Specifies mail exchange servers for email delivery.",
        'importance': "Critical for ensuring email delivery.",
        'configuration': "Include proper priority and ensure the mail server hostname is correct.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-mx-record/",
        'security_risks': "Misconfigured MX records can lead to email delivery failures or spam vulnerabilities.",
        'category': "Essential"
    },
    'TXT': {
        'description': "Contains arbitrary text information, commonly used for SPF, DKIM, and other verifications.",
        'importance': "Important for email authentication and various verification purposes.",
        'configuration': "Should include the correct SPF, DKIM, or other policy strings.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-txt-record/",
        'security_risks': "Incorrect TXT records can weaken email security and validation.",
        'category': "Essential"
    },
    'NS': {
        'description': "Lists the authoritative name servers for the domain.",
        'importance': "Fundamental for DNS resolution.",
        'configuration': "Must point to the correct nameservers provided by your DNS host.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-ns-record/",
        'security_risks': "Faulty NS records can cause complete DNS resolution failures.",
        'category': "Essential"
    },
    'SOA': {
        'description': "Start of Authority record containing administrative information for the domain.",
        'importance': "Used to define zone properties and manage DNS synchronization.",
        'configuration': "Ensure proper serial number and refresh values are set.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-soa-record/",
        'security_risks': "Incorrect SOA values can lead to issues with DNS propagation and synchronization.",
        'category': "Essential"
    },
    'PTR': {
        'description': "Maps an IP address to a domain name (reverse DNS lookup).",
        'importance': "Important for email server verification and reducing spam.",
        'configuration': "Should correctly map the IP address to the domain name.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-ptr-record/",
        'security_risks': "Misconfigured PTR records can affect email reputation and deliverability.",
        'category': "Optional"
    },
    'SRV': {
        'description': "Specifies the location of servers for specific services (e.g., VoIP, IM).",
        'importance': "Enables clients to locate services like SIP or XMPP.",
        'configuration': "Include priority, weight, port, and target in the record.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-srv-record/",
        'security_risks': "Improper SRV records can disrupt specialized service operations.",
        'category': "Optional"
    },
    'CAA': {
        'description': "Specifies which Certificate Authorities (CAs) are permitted to issue certificates for the domain.",
        'importance': "Enhances security by restricting unauthorized certificate issuance.",
        'configuration': "List the approved CAs using the correct syntax.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dns-caa-record/",
        'security_risks': "A missing or incorrect CAA record could lead to rogue certificate issuance.",
        'category': "Essential"
    },
    'DNSKEY': {
        'description': "Stores public keys used for DNSSEC (DNS Security Extensions).",
        'importance': "Critical for validating DNS responses and ensuring data integrity.",
        'configuration': "Ensure the public key is correctly configured for DNSSEC.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/dnskey-record/",
        'security_risks': "Incorrect DNSKEY records can compromise DNSSEC validation.",
        'category': "Advanced"
    },
    'DS': {
        'description': "Delegation Signer record, used in DNSSEC to link a parent zone to a child zone.",
        'importance': "Ensures the authenticity of DNS data across zones.",
        'configuration': "Must include the correct key tag, algorithm, and digest.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/ds-record/",
        'security_risks': "Misconfigured DS records can break DNSSEC chain of trust.",
        'category': "Advanced"
    },
    'NAPTR': {
        'description': "Name Authority Pointer, used for dynamic delegation in telephony and other applications.",
        'importance': "Supports advanced routing and service discovery.",
        'configuration': "Include order, preference, flags, service, regexp, and replacement fields.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/naptr-record/",
        'security_risks': "Improper NAPTR records can disrupt service discovery and routing.",
        'category': "Advanced"
    },
    'TLSA': {
        'description': "Used in DANE (DNS-Based Authentication of Named Entities) to associate certificates with domain names.",
        'importance': "Enhances TLS/SSL security by binding certificates to DNS.",
        'configuration': "Include the correct certificate usage, selector, and matching type.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/tlsa-record/",
        'security_risks': "Incorrect TLSA records can weaken TLS/SSL security.",
        'category': "Advanced"
    },
    'SPF': {
        'description': "Sender Policy Framework record, used to specify authorized email servers for a domain.",
        'importance': "Helps prevent email spoofing and phishing.",
        'configuration': "Include the list of authorized IP addresses or domains.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/spf-record/",
        'security_risks': "Misconfigured SPF records can lead to email delivery issues or spoofing vulnerabilities.",
        'category': "Optional"
    },
    'CERT': {
        'description': "Stores public key certificates for encryption and authentication.",
        'importance': "Used for secure communication and identity verification.",
        'configuration': "Ensure the certificate is correctly formatted and up-to-date.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/cert-record/",
        'security_risks': "Incorrect CERT records can compromise secure communication.",
        'category': "Advanced"
    },
    'LOC': {
        'description': "Stores geographic location information for a domain.",
        'importance': "Useful for location-based services and mapping.",
        'configuration': "Include latitude, longitude, altitude, and precision values.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/loc-record/",
        'security_risks': "Misconfigured LOC records can lead to incorrect location data.",
        'category': "Advanced"
    },
    'HINFO': {
        'description': "Host Information record, provides hardware and OS details for a host.",
        'importance': "Rarely used, but can provide system information.",
        'configuration': "Include hardware type and operating system details.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/hinfo-record/",
        'security_risks': "Exposing HINFO records can reveal sensitive system information.",
        'category': "Advanced"
    },
    'RP': {
        'description': "Responsible Person record, identifies the person responsible for the domain.",
        'importance': "Provides contact information for administrative purposes.",
        'configuration': "Include the email address of the responsible person.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/rp-record/",
        'security_risks': "Misconfigured RP records can expose personal information.",
        'category': "Advanced"
    },
    'AFSDB': {
        'description': "Andrew File System Database record, used for AFS cell database servers.",
        'importance': "Supports AFS file system operations.",
        'configuration': "Include the server subtype and hostname.",
        'resource': "https://www.cloudflare.com/learning/dns/dns-records/afsdb-record/",
        'security_risks': "Misconfigured AFSDB records can disrupt AFS operations.",
        'category': "Advanced"
    }
}

security_headers = {
    "Strict-Transport-Security": {
        "description": "Instructs browsers to use HTTPS for all future requests, ensuring secure connections.",
        "importance": "Critical",
        "configuration": "Set a max-age (in seconds), and optionally include 'includeSubDomains' and 'preload' directives.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
        "security_risks": "An incorrect max-age value can lock users out if HTTPS is misconfigured; omitting this header exposes the site to downgrade attacks.",
    },
    "Content-Security-Policy": {
        "description": "Defines which content sources (scripts, styles, images, etc.) are allowed to be loaded, mitigating risks like XSS.",
        "importance": "Critical",
        "configuration": "Set directives such as 'default-src', 'script-src', 'style-src', etc. to restrict resource origins.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy",
        "security_risks": "A too-permissive policy can allow injection of malicious code; an overly strict policy may break legitimate functionality.",
    },
    "Access-Control-Allow-Origin": {
        "description": "Specifies which origins are permitted to access resources via CORS.",
        "importance": "Critical",
        "configuration": "Set to a specific domain (e.g. 'https://example.com') or use '*' (not recommended for sensitive data).",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS",
        "security_risks": "Using a wildcard or misconfigured value may allow unauthorized domains to access sensitive resources.",
    },
    "X-Content-Type-Options": {
        "description": "Prevents browsers from MIME type sniffing by enforcing the declared Content-Type.",
        "importance": "High",
        "configuration": "Set the header value to 'nosniff'.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options",
        "security_risks": "Without this header, browsers might execute files in unintended ways if MIME types are misinterpreted.",
    },
    "X-Frame-Options": {
        "description": "Prevents the webpage from being framed by other sites, reducing the risk of clickjacking.",
        "importance": "High",
        "configuration": "Set to 'DENY' to block all framing, or 'SAMEORIGIN' to allow framing only from the same origin.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
        "security_risks": "Lack of proper framing controls can expose the site to clickjacking attacks.",
    },
    "Expect-CT": {
        "description": "Enforces Certificate Transparency by requiring that TLS/SSL certificates are logged, helping detect misissued certificates.",
        "importance": "High",
        "configuration": "Set a max-age and optionally add the 'enforce' directive.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT",
        "security_risks": "Without CT enforcement, fraudulent certificates might go undetected; misconfiguration can lead to unexpected connection failures.",
    },
    "X-XSS-Protection": {
        "description": "Enables the browser's built-in XSS filtering to help prevent cross-site scripting attacks.",
        "importance": "Medium",
        "configuration": "Typically set to '1; mode=block' so that the browser will block the response if an attack is detected.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection",
        "security_risks": "Reliance solely on this header is discouraged, as its protection may be limited or not supported in all browsers.",
    },
    "Referrer-Policy": {
        "description": "Controls how much referrer information is sent with requests, which can help protect user privacy.",
        "importance": "Medium",
        "configuration": "Choose from policies such as 'no-referrer', 'origin', 'strict-origin-when-cross-origin', etc., based on your privacy needs.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy",
        "security_risks": "An inappropriate setting can leak sensitive URL information or hinder analytics.",
    },
    "Permissions-Policy": {
        "description": "Specifies which browser features are allowed to be used (or disabled) on your site and its embedded frames.",
        "importance": "Medium",
        "configuration": "Define a list of allowed features and the domains permitted to use them (e.g., 'geolocation=(self)').",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy",
        "security_risks": "Overly permissive policies may enable misuse of sensitive browser features like camera or location.",
    },
    "Cross-Origin-Opener-Policy": {
        "description": "Ensures that a browsing context is isolated from cross-origin documents, which helps prevent side-channel attacks.",
        "importance": "Medium",
        "configuration": "Set to 'same-origin' or 'same-origin-allow-popups' to control cross-origin interactions.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy",
        "security_risks": "A weak or missing policy may allow cross-origin interactions that expose the site to certain attacks.",
    },
    "Cross-Origin-Embedder-Policy": {
        "description": "Restricts which cross-origin resources can be loaded by the document, enforcing a higher level of resource isolation.",
        "importance": "Medium",
        "configuration": "Set to 'require-corp' to enforce that only resources explicitly marked as loadable can be embedded.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy",
        "security_risks": "If not set or misconfigured, untrusted resources may be loaded, increasing the risk of injection or leakage.",
    },
    "Cross-Origin-Resource-Policy": {
        "description": "Controls which origins can load a given resource, thereby protecting against unwanted resource sharing.",
        "importance": "Medium",
        "configuration": "Common settings include 'same-origin' or explicitly listing allowed domains.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy",
        "security_risks": "A misconfigured policy might inadvertently expose sensitive resources to external sites.",
    },
    "Cache-Control": {
        "description": "Specifies directives for caching mechanisms in both browsers and intermediary caches, ensuring that sensitive data is not stored unintentionally.",
        "importance": "Medium",
        "configuration": "Use directives like 'no-store', 'no-cache', or 'private' based on the content’s sensitivity.",
        "resource": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control",
        "security_risks": "Inadequate cache controls may lead to sensitive data being stored and served inappropriately.",
    }
}
