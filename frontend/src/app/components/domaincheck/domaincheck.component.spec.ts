import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DomaincheckComponent } from './domaincheck.component';

describe('DomaincheckComponent', () => {
  let component: DomaincheckComponent;
  let fixture: ComponentFixture<DomaincheckComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DomaincheckComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DomaincheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
