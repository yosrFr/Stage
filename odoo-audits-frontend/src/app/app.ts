import { Component } from '@angular/core';
import { AuditsTableComponent } from './components/audits-table/audits-table';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AuditsTableComponent],
  template: `<app-audits-table></app-audits-table>`
})
export class App {}