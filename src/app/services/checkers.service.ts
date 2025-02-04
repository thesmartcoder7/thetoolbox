import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { Response } from '../interfaces/response';
import { AuditResult } from '../interfaces/insights';

@Injectable({
  providedIn: 'root',
})
export class CheckersService {
  constructor(private http: HttpClient) { }

  private processResponse(response: any): Response {
    // Implement processing logic here
    console.log(response)
    const processedData: Response = {
      ssl_certificate: response.ssl_certificate,
      cipher_suites: { 'not-found': response.cipher_suites?.['not-found'] },
      security_headers: {
        'present': response.security_headers?.present,
        'absent': response.security_headers?.absent,
      },
      dns_info: { 'dns-records': response.dns_info?.['dns-records'] || {} },
      domain_check: response.domain_check || {},
      whois_check: { 'whois-info': response.whois_check?.['whois-info'] || [] },
    };

    return processedData;
  }

  checkDomain(domain: string): Observable<Response> {
    let payload = {
      domain: domain,
    };

    return this.http
      .post<Response>('http://127.0.0.1:8000/webtools/domain_check/', payload)
      .pipe(map((response) => this.processResponse(response)));
  }

  private processInsights(response: any): AuditResult {
    // Implement processing logic here
    const processedData: any = {
      deviceData: response,
    };

    return processedData;
  }

  getPageInsights(domain: string) {
    let payload = {
      domain: domain,
    };

    return this.http
      .post<AuditResult>('http://127.0.0.1:8000/webtools/page_insights/', payload)
      .pipe(map((res) => this.processInsights(res)));
  }
}
