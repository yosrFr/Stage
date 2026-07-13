import { TestBed } from '@angular/core/testing';

import { Opportunities } from './opportunities';

describe('Opportunities', () => {
  let service: Opportunities;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Opportunities);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
