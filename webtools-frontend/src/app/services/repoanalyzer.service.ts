import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Repository } from '../interfaces/repository';

@Injectable({
  providedIn: 'root'
})
export class RepoanalyzerService {

  constructor(private http: HttpClient) { }

  runAnalysis(repo: string): Observable<Repository> {
    console.log(' sending url to backend . . . ')
    let payload = {
      repository: repo,
    };
    return this.http.post<Repository>('http://127.0.0.1:8000/git-tools/analyze/', payload)
  }

}
