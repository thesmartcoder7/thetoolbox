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

  onEnterPressed(event: KeyboardEvent): void {
    // Check if the key pressed is Enter (key code 13)
    if (event.key === 'Enter') {
      const inputValue = (event.target as HTMLInputElement).value;
      // Call your function here
      this.checkDoman(inputValue);
    }
  }

  checkDoman(domain: string): void {
    if (!domain) {
      this.emptyInput = true;
      this.placeHolder = 'Please enter a valid domain name . . .';
    } else {
      this.runAnalysis = true;
      this.checkers.checkDomain(domain).subscribe((res) => {
        console.log(res.domain_check.emails_check);
        this.results = res;
        this.runAnalysis = false;
      });
    }
  }
}
