import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from 'src/app/services/authentication.service';
// import { User } from 'src/app/interfaces/user';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.scss',
})
export class LandingComponent implements OnInit {
  currentYear: number = new Date().getFullYear();
  authModal: boolean = false;
  emailInput: string = 'login-email';
  passwordInput: string = 'login-password';
  signUp: boolean = false;
  buttonValue: string = 'login';
  greeting: string = 'Welcome Back!';

  loginFunction: string = 'userLogin(mail.value, pass.value)';
  signUpFunction: string = 'userSignUp(name.value, mail.value, pass.value)';

  constructor(private auth: AuthenticationService) {}

  ngOnInit(): void {
    // this.auth.allUsers();
    // this.auth.logout();
    this.auth.checkSignedUser();
  }

  onFormSubmit(event: Event) {
    event.preventDefault();
    // signup variables
    let fullName = document.getElementById('user-name') as HTMLInputElement;
    let signUpEmail = document.getElementById(
      'signup-email'
    ) as HTMLInputElement;
    let signUpPass = document.getElementById(
      'signup-password'
    ) as HTMLInputElement;

    let loginEmail = document.getElementById('login-email') as HTMLInputElement;
    let loginPassword = document.getElementById(
      'login-password'
    ) as HTMLInputElement;

    if (fullName && signUpEmail && signUpPass) {
      this.userSignUp(fullName.value, signUpEmail.value, signUpPass.value);
    } else {
      this.userLogin(loginEmail.value, loginPassword.value);
    }
  }

  userLogin(email: string, password: string): void {
    // console.log({
    //   email: email,
    //   password: password,
    // });
    this.auth.login(email, password);
  }

  userSignUp(name: string, email: string, password: string): void {
    // console.log({
    //   'full name': name,
    //   email: email,
    //   password: password,
    // });
    this.auth.signUp(name, email, password);
  }

  toggleAuthModal(): void {
    if (this.authModal) {
      this.authModal = false;
    } else {
      this.authModal = true;
    }
  }

  toggleSignUp(): void {
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

  attributeSwitch(): void {
    this.emailInput = 'signup-email';
    this.passwordInput = 'signup-password';
  }
}
