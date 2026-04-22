import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MinifiersComponent } from './minifiers.component';

describe('MinifiersComponent', () => {
  let component: MinifiersComponent;
  let fixture: ComponentFixture<MinifiersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MinifiersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MinifiersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
