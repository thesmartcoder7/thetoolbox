import { Component } from '@angular/core';
import { Response } from 'src/app/interfaces/response';
import { CheckersService } from 'src/app/services/checkers.service';

@Component({
  selector: 'app-domaincheck',
  standalone: true,
  imports: [],
  templateUrl: './domaincheck.component.html',
  styleUrl: './domaincheck.component.scss'
})
export class DomaincheckComponent {
  constructor(private checkers: CheckersService) { }
  runAnalysis: boolean = false;
  emptyInput: boolean = false;
  results?: Response;
  placeHolder: string = 'example.com';
  activeTab: string = 'tab1';
  inputValue: string = '';
  categories: string[] = ["Essential", "Optional", "Advanced"];
  securityLevels: string[] = ['Critical', 'High', 'Medium']
  activeRecord = 0;

  ngOnInit() {
    this.results = JSON.parse(localStorage['persistedDNS'])
    if (typeof (this.results?.whois_check['whois-info'].domain_name) == 'string') {
      this.placeHolder = String(this.results?.whois_check['whois-info'].domain_name).toLowerCase()
    } else {
      this.placeHolder = String(this.results?.whois_check['whois-info'].domain_name[0]).toLowerCase()
    }
    // console.log(this.results)
  }

  // Called when an accordion header is clicked.
  setActive(index: number): void {
    this.activeRecord = index;
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

  onEnterPressed(event: KeyboardEvent, element: HTMLInputElement): void {
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
      if (this.isValidDomain(domain)) {
        this.runAnalysis = true;
        this.results = undefined;
        this.checkers.checkDomain(this.cleanDomain(domain)).subscribe((res) => {
          this.results = res;
          localStorage.setItem('persistedDNS', JSON.stringify(this.results))
          // console.log(this.results)
          this.runAnalysis = false;
          if (typeof (this.results?.whois_check['whois-info'].domain_name) == 'string') {
            this.placeHolder = String(this.results?.whois_check['whois-info'].domain_name).toLowerCase()
          } else {
            this.placeHolder = String(this.results?.whois_check['whois-info'].domain_name[0]).toLowerCase()
          }
        });
      } else {
        this.placeHolder = 'Please enter a Valid domain . . .';
        element.value = '';
      };

    }
  }
}
