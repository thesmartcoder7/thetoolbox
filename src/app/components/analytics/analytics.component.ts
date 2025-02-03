import { Component } from '@angular/core';
import { Response } from 'src/app/interfaces/response';
import { CheckersService } from 'src/app/services/checkers.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [],
  templateUrl: './analytics.component.html',
  styleUrl: './analytics.component.scss',
})
export class AnalyticsComponent {
  constructor(private checkers: CheckersService) {}
  runAnalysis: boolean = false;
  emptyInput: boolean = false;
  results?: Response;
  placeHolder: string = 'example.com';
  activeTab: string = 'tab1';
  inputValue: string = '';

  isValidDomain(input: string): boolean {
    const domainRegex = /^(?!:\/\/)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$/;
    return domainRegex.test(input);
  }

  onEnterPressed(event: KeyboardEvent, element:HTMLInputElement): void {
    // Check if the key pressed is Enter (key code 13)
    if (event.key === 'Enter') {
      const inputValue = (event.target as HTMLInputElement).value;
      this.checkDoman(inputValue, element);
    }
  }

  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }
  getDnsRecords(record: string) {
    return this.results?.dns_info['dns-records'][record] || [];
  }

  checkDoman(domain: string, element: HTMLInputElement): void {
    if (!domain) {
      this.emptyInput = true;
      this.placeHolder = 'Please enter a valid domain name . . .';
    } else {
      this.emptyInput = false;
      if (this.isValidDomain(domain)){
        this.runAnalysis = true;
        this.results = undefined;
        this.checkers.checkDomain(domain).subscribe((res) => {
          this.results = res;
          this.runAnalysis = false;
        });
      } else {
        this.placeHolder = 'Please enter a domain name without the http(s) potocol . . .';
        element.value = '';
      };
      
    }
  }
}
