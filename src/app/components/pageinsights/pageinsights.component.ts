import { Component } from '@angular/core';
import { CheckersService } from 'src/app/services/checkers.service';
import { CommonModule } from '@angular/common';
import { SafeHtmlPipe } from 'src/app/pipes/safe-html.pipe';

@Component({
  selector: 'app-pageinsights',
  standalone: true,
  imports: [SafeHtmlPipe, CommonModule],
  templateUrl: './pageinsights.component.html',
  styleUrl: './pageinsights.component.scss',
})
export class PageinsightsComponent {
  runAnalysis: boolean = false;
  emptyInput: boolean = false;
  results?: any;
  placeHolder: string = 'example.com';
  activeTab: string = 'mobile';
  activeMetric: string = 'Performance';
  green: string = '#0c6';
  orange: string = '#fa3';
  red: string = '#f33';
  scorevalues: string[] = ['metricSavings', 'binary'];
  activeResources: string[] = [];

  metrics: any;

  constructor(private checkers: CheckersService) { }

  ngOnInit() {
    this.results = JSON.parse(localStorage['persistedInsights'])
    console.log(this.results)
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      const inputValue = (event.target as HTMLInputElement).value;
      this.runInsights(inputValue);
    }
  }

  isValidDomain(input: string): boolean {
    // Remove protocol (http:// or https://) and trailing slash (/)
    input = input.replace(/^(https?:\/\/)?/, '').replace(/\/$/, '');
    // Strict domain validation regex
    const domainRegex = /^(?!:\/\/)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$/;
    return domainRegex.test(input);
  }


  cleanDomain(domain: string): string {
    // Remove protocol (http:// or https://)
    domain = domain.replace(/^https?:\/\//, '');
    // Remove trailing slashes
    return domain.replace(/\/+$/, '');
  }


  toggleResources(id: string) {
    if (this.activeResources.includes(id)) {
      let index = this.activeResources.indexOf(id);
      this.activeResources.splice(index, 1);
    } else {
      this.activeResources.push(id);
    }
    // console.log(this.activeResources);
  }

  setBackground(value: string) {
    return `url(${value})`;
  }

  getColor(value: number): string {
    if (value >= 90) {
      return this.green;
    } else if (value >= 50 && value < 90) {
      return this.orange;
    } else {
      return this.red;
    }
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

  runInsights(domain: string): void {
    if (!domain) {
      this.emptyInput = true;
      this.placeHolder = 'Please enter a valid domain name . . .';
    } else {
      if (this.isValidDomain(domain)) {
        this.runAnalysis = true;
        this.results = null;
        this.checkers.getPageInsights(this.cleanDomain(domain)).subscribe((res: any) => {
          this.results = res.deviceData.page_insights;
          localStorage.setItem('persistedInsights', JSON.stringify(this.results))
          this.metrics = this.results.audits;
          this.runAnalysis = false;
        });
      } else {
        this.placeHolder = 'Please enter a valid domain name . . .';
      }

    }
    this.activeResources = [];
  }
}
