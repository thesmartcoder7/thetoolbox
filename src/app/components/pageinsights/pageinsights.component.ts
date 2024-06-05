import { Component } from '@angular/core';
import { CheckersService } from 'src/app/services/checkers.service';

@Component({
  selector: 'app-pageinsights',
  standalone: true,
  imports: [],
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

  metrics: any;

  constructor(private checkers: CheckersService) {}

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      const inputValue = (event.target as HTMLInputElement).value;
      this.runInsights(inputValue);
    }
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
      this.runAnalysis = true;
      this.results = null;
      this.checkers.getPageInsights(domain).subscribe((res: any) => {
        this.results = res.deviceData.page_insights;
        console.log(this.results);
        this.metrics = this.results.audits;
        this.runAnalysis = false;
      });
    }
  }
}
