import { Component } from '@angular/core';
import { FieldsComponent } from './components/fields/fields';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FieldsComponent],
  template: `<app-fields></app-fields>`
})
export class App {}