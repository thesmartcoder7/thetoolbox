import { Component } from '@angular/core';

@Component({
  selector: 'app-minifiers',
  standalone: true,
  imports: [],
  templateUrl: './minifiers.component.html',
  styleUrl: './minifiers.component.scss',
})
export class MinifiersComponent {
  selectedTab: 'html' | 'css' | 'js' = 'html'; // Default selected tab
  outputText: string = ''; // Minified output text

  selectTab(tab: 'html' | 'css' | 'js'): void {
    this.selectedTab = tab;
    this.outputText = '';
  }

  // Functions for HTML, CSS, and JavaScript minifiers go here
  htmlMinifier(input: string): void {
    // Implement HTML minifier logic
    // Remove comments
    this.outputText = input.replace(/<!--[\s\S]*?-->/g, '');
    // Remove whitespace between tags
    this.outputText = this.outputText.replace(/>\s+</g, '><');
    // Remove leading and trailing whitespace
    this.outputText = this.outputText.trim();
  }

  cssMinifier(input: string): void {
    // Implement CSS minifier logic
    // Remove comments
    this.outputText = input.replace(/\/\*[\s\S]*?\*\//g, '');
    // Remove whitespace and newlines
    this.outputText = this.outputText.replace(/\s+/g, ' ');
    // Remove leading and trailing whitespace
    this.outputText = this.outputText.trim();
  }

  jsMinifier(input: string): void {
    // Implement JavaScript minifier logic
    // Remove single-line comments
    this.outputText = input.replace(/\/\/.*/g, '');
    // Remove multi-line comments
    this.outputText = this.outputText.replace(/\/\*[\s\S]*?\*\//g, '');
    // Remove whitespace and newlines
    this.outputText = this.outputText.replace(/\s+/g, ' ');
    // Remove leading and trailing whitespace
    this.outputText = this.outputText.trim();
  }

  onSubmitClick(input: string): void {
    if (this.selectedTab === 'html') {
      this.htmlMinifier(input);
    } else if (this.selectedTab === 'css') {
      this.cssMinifier(input);
    } else {
      this.jsMinifier(input);
    }
  }

  onEnterPressed(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      const inputValue = (event.target as HTMLInputElement).value;
      this.onSubmitClick(inputValue);
    }
  }
}
