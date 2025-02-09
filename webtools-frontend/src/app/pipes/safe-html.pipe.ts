import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'safeHtml',
  standalone: true,
})
export class SafeHtmlPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) return this.sanitizer.bypassSecurityTrustHtml('');

    const markdownLinkRegex = /\[([^\]]+)\]\((https?:\/\/[^\s]+)\)/g;
    const transformedValue = value.replace(
      markdownLinkRegex,
      (match, text, url) => {
        return `<a href="${url}" target="_blank">${text}</a>`;
      }
    );

    return this.sanitizer.bypassSecurityTrustHtml(transformedValue);
  }
}
