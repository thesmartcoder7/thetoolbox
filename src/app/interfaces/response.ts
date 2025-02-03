// Interface for SSL Certificate
interface SSLCertificate {
  subject: [string[]];
  issuer: [string[], string[], string[]];
  version: number;
  serialNumber: string;
  notBefore: string;
  notAfter: string;
  subjectAltName: [string[]];
  OCSP: string[];
  caIssuers: string[];
}

// Interface for Security Headers
interface SecurityHeaders {
  [key: string]: string[];
}


// Interface for DNS Records
interface DNSRecords {
  [key: string]: string[] | undefined;
}

// Interface for Domain Check
interface DomainCheck {
  'dns-resolution': string;
  'ssl-check': { status: string; message: string };
  emails_check: [{ mx: string; status: string; message: string }];
  'website-accessibility': { status: string; message: string };
}

// Interface for WHOIS Info
interface WHOISInfo {
  domain_name: string[];
  registrar: string;
  whois_server: string;
  referral_url: string | null;
  updated_date: string;
  creation_date: string;
  expiration_date: string;
  name_servers: string[];
  status: string;
  emails: string;
  dnssec: string;
  org: string;
  name: string | null;
  city: string | null;
  country: string;
}

// Interface for the response data structure
export interface Response {
  ssl_certificate: SSLCertificate;
  cipher_suites: { 'not-found': string };
  security_headers: SecurityHeaders;
  dns_info: { 'dns-records': DNSRecords };
  domain_check: DomainCheck;
  whois_check: { 'whois-info': WHOISInfo };
}
