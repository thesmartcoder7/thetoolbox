import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  constructor(private http: HttpClient) {}

  allUsers(): void {
    this.http
      .get(`${environment.apiUrl}/users/`, { withCredentials: true })
      .subscribe((res) => {
        console.log(res);
      });
  }

  checkSignedUser(): void {
    this.http
      .get(`${environment.apiUrl}/users/user/`, { withCredentials: true })
      .subscribe((res) => {
        console.log(res);
      });
  }

  signUp(name: string, email: string, password: string): any {
    let payload = {
      name: name,
      email: email,
      password: password,
    };

    this.http
      .post(`${environment.apiUrl}/users/register/`, payload)
      .subscribe((res) => {
        console.log(res);
      });
  }

  login(email: string, password: string): any {
    let payload = {
      email: email,
      password: password,
    };

    this.http
      .post(`${environment.apiUrl}/users/login/`, payload)
      .subscribe((res) => {
        console.log(res);
      });
  }

  logout(): void {
    this.http
      .post(`${environment.apiUrl}/users/logout/`, { withCredentials: true })
      .subscribe((res) => {
        console.log(res);
      });
  }
}
