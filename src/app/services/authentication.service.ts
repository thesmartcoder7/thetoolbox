import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
HttpClient;

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  constructor(private http: HttpClient) {}

  allUsers(): void {
    this.http
      .get('http://127.0.0.1:8000/users', { withCredentials: true })
      .subscribe((res) => {
        console.log(res);
      });
  }

  checkSignedUser(): void {
    this.http
      .get('http://127.0.0.1:8000/users/user', { withCredentials: true })
      .subscribe((res) => {
        console.log(res);
      });
  }

  logout(): void {
    this.http
      .post('http://127.0.0.1:8000/users/logout/', { withCredentials: true })
      .subscribe((res) => {
        console.log(res);
      });
  }
}
