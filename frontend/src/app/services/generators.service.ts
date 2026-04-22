import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
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
      `${environment.apiUrl}/webtools/get_sitemap/`,
      payload,
    );
  }
}
