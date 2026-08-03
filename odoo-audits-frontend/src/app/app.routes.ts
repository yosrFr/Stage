import { Routes } from '@angular/router';
import { AuditsTableComponent } from './components/audits-table/audits-table';
import { CategoriesComponent } from './components/categories/categories';

export const routes: Routes = [
  { path: '', component: AuditsTableComponent },
  { path: 'categories/:norm/:opportunityId', component: CategoriesComponent }
];