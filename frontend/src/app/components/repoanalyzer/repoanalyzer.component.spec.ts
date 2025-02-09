import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RepoanalyzerComponent } from './repoanalyzer.component';

describe('RepoanalyzerComponent', () => {
  let component: RepoanalyzerComponent;
  let fixture: ComponentFixture<RepoanalyzerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RepoanalyzerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RepoanalyzerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
