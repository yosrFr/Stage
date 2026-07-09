import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuditsTable } from './audits-table';

describe('AuditsTable', () => {
  let component: AuditsTable;
  let fixture: ComponentFixture<AuditsTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuditsTable],
    }).compileComponents();

    fixture = TestBed.createComponent(AuditsTable);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
