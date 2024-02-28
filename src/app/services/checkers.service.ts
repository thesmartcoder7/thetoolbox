import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
HttpClient;

@Injectable({
  providedIn: 'root',
})
export class CheckersService {
  constructor(private http: HttpClient) {}
  
  checkDomain(domain: string): Observable<any> {
    let payload = {
      domain: domain,
    };

    return this.http.post(
      'http://127.0.0.1:8000/webtools/domain_check/',
      payload
    );
  }
}
