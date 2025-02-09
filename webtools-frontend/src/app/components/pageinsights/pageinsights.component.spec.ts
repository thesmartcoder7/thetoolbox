import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageinsightsComponent } from './pageinsights.component';

describe('PageinsightsComponent', () => {
  let component: PageinsightsComponent;
  let fixture: ComponentFixture<PageinsightsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PageinsightsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PageinsightsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
