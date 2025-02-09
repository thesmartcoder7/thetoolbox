import { TestBed } from '@angular/core/testing';

import { RepoanalyzerService } from './repoanalyzer.service';

describe('RepoanalyzerService', () => {
  let service: RepoanalyzerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RepoanalyzerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
