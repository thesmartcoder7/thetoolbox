import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'TheToolBox';
  // isTooSmall = false;
  // isMenuOpen = false;

  // toggleMenu() {
  //   if (this.isMenuOpen && this.isTooSmall) {
  //     this.isMenuOpen = false;
  //   } else {
  //     this.isMenuOpen = true;
  //   }
  //   console.log('toggleMenu called', this.isMenuOpen);
  // }

  // constructor(private breakpointObserver: BreakpointObserver) {
  //   this.breakpointObserver.observe([Breakpoints.Small, Breakpoints.Handset]).subscribe(result => {
  //     this.isTooSmall = result.matches;
  //   });
  // }
}
