import { Component } from '@angular/core';
import { Repository } from 'src/app/interfaces/repository';
import { RepoanalyzerService } from 'src/app/services/repoanalyzer.service';

@Component({
  selector: 'app-repoanalyzer',
  standalone: true,
  imports: [],
  templateUrl: './repoanalyzer.component.html',
  styleUrl: './repoanalyzer.component.scss'
})
export class RepoanalyzerComponent {
  runAnalysis: boolean = false;
  emptyInput: boolean = false;
  results?: any;
  activeTab: string = 'main';
  placeHolder: string = 'https://github.com/username/repo-name';
  contributors: any[] = []
  totalContributions = this.contributors?.reduce((sum, user) => sum + user.contributions, 0);

  // colors
  green: string = '#0c6';
  orange: string = '#fa3';
  red: string = '#f33';

  constructor(private repo: RepoanalyzerService) { }

  ngOnInit() {
    if (localStorage['persistedRepo']) {
      this.results = JSON.parse(localStorage['persistedRepo'])
      console.log(this.results)
      this.placeHolder = this.results.repository
      this.contributors = this.results.analysis_results.optionals[5].criteria.top_contributors
    }
  }

  getBarValue(contribution: number){
    let sum = 0
    for(let user of this.contributors){
      sum += user.contributions
    }
    this.totalContributions = sum
    return (contribution / sum) * 12.5
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      const inputValue = (event.target as HTMLInputElement).value;
      this.analyzeRepo(inputValue);
    }
  }


  setBackground(value: string) {
    return `url(${value})`;
  }


  getColor(value: number): string {
    if (value >= 70) {
      return this.green;
    } else if (value >= 40 && value < 70) {
      return this.orange;
    } else {
      return this.red;
    }
  }


  objectKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }


  type(value: any) {
    return typeof (value)
  }

  splitRepoDetails(repo: string){
    return repo.split('/')
  }


  getWidth(value: number) {
    return value.toString() + "%"
  }

  getBorderColor(value: number): any {
    return `border-left: solid 0.3vw ${this.getColor(value)};`;
  }

  getProgressStyle(value: number): any {
    return {
      '--primary-color': this.getColor(value),
      '--value': value,
    };
  }

  roundValue(value: number) {
    return Math.round(value);
  }


  analyzeRepo(repo: string): void {
    if (!repo) {
      this.emptyInput = true;
      this.placeHolder = 'Please enter a valid repository name . . .';
    } else {

      this.runAnalysis = true;
      this.results = null;
      this.repo.runAnalysis(repo).subscribe((res: Repository) => {
        this.results = res
        console.log(this.results)
        this.placeHolder = this.results.repository
        localStorage.setItem('persistedRepo', JSON.stringify(this.results))
        this.contributors = this.results.analysis_results.optionals[5].criteria.top_contributors
        this.runAnalysis = false
      });
    }
  }

}
