import { Component } from '@angular/core';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.scss',
})
export class LandingComponent {
  currentYear: number = new Date().getFullYear();
  authModal: boolean = false;
  emailInput: string = 'login-email';
  passwordInput: string = 'login-password';
  signUp: boolean = false;
  buttonValue: string = 'login';
  greeting: string = 'Welcome Back!';

  toggleAuthModal() {
    if (this.authModal) {
      this.authModal = false;
    } else {
      this.authModal = true;
    }
  }

  toggleSignUp() {
    if (this.signUp) {
      this.signUp = false;
      this.buttonValue = 'Login';
    } else {
      this.signUp = true;
      this.greeting = 'Hello Stranger . . . ';
      this.emailInput = 'signup-email';
      this.passwordInput = 'signup-password';
      this.buttonValue = 'Sign Up';
    }
  }

  attributeSwitch() {
    this.emailInput = 'signup-email';
    this.passwordInput = 'signup-password';
  }
}
