import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
HttpClient;

@Injectable({
  providedIn: 'root',
})
export class GeneratorsService {
  constructor(private http: HttpClient) {}

  generateSitemap(domain: string): Observable<any> {
    let payload = {
      domain: domain,
    };

    return this.http.post(
      'http://127.0.0.1:8000/webtools/get_sitemap/',
      payload
    );
  }
}
