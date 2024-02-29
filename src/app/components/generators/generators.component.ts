import { Clipboard } from '@angular/cdk/clipboard';
import { Component } from '@angular/core';
import { GeneratorsService } from 'src/app/services/generators.service';

@Component({
  selector: 'app-generators',
  standalone: true,
  imports: [],
  templateUrl: './generators.component.html',
  styleUrl: './generators.component.scss',
})
export class GeneratorsComponent {
  password: string = '';
  sitemapXML: string = '';
  xmlProcess: boolean = false;
  changeIcon: boolean = false;
  activeTab: string = 'tab1';

  constructor(
    private generators: GeneratorsService,
    private clipboard: Clipboard
  ) {}

  copyPasswordToClipboard() {
    if (this.password) {
      this.clipboard.copy(this.password);
      this.changeIcon = true;
    }
  }

  generatePassword() {
    const uppercaseChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const lowercaseChars = 'abcdefghijklmnopqrstuvwxyz';
    const numberChars = '0123456789';
    const specialChars = '!@#$%^&*()+{}[]|;:<>?';

    this.changeIcon = false;

    const passwordLength = 16;

    let password = '';

    // Generate random characters
    for (let i = 0; i < passwordLength; i++) {
      const charType = Math.floor(Math.random() * 4); // Randomly select character type
      switch (charType) {
        case 0: // Uppercase letter
          password += uppercaseChars.charAt(
            Math.floor(Math.random() * uppercaseChars.length)
          );
          break;
        case 1: // Lowercase letter
          password += lowercaseChars.charAt(
            Math.floor(Math.random() * lowercaseChars.length)
          );
          break;
        case 2: // Number
          password += numberChars.charAt(
            Math.floor(Math.random() * numberChars.length)
          );
          break;
        case 3: // Special character
          password += specialChars.charAt(
            Math.floor(Math.random() * specialChars.length)
          );
          break;
      }
    }

    // Shuffle the password characters
    password = password
      .split('')
      .sort(() => Math.random() - 0.5)
      .join('');

    this.password = password;
  }

  generateSitemap(domain: string) {
    let parser: DOMParser = new DOMParser();
    this.sitemapXML = '';
    this.xmlProcess = true;
    this.generators.generateSitemap(domain).subscribe((res) => {
      this.sitemapXML = res.xml;
    });
  }
}
