import { Component, OnInit, Inject, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformServer } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

interface Category {
  category_id: number;
  category_name: string;
  display_id?: string;
  checked?: boolean;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './categories.html',
  styleUrls: ['./categories.css']
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];
  filteredCategories: Category[] = [];
  searchTerm = '';
  loading = true;
  error = '';
  norm = '';
  opportunityId = '';
  private baseUrl: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.baseUrl = isPlatformServer(this.platformId)
      ? 'http://backend:8000'
      : 'http://127.0.0.1:8000';
  }

  ngOnInit(): void {
    this.norm = this.route.snapshot.paramMap.get('norm') || '';
    this.opportunityId = this.route.snapshot.paramMap.get('opportunityId') || '';

    this.http.get<Category[]>(`${this.baseUrl}/categories/${this.norm}`).subscribe({
      next: (data) => {
        const savedRaw = sessionStorage.getItem(`unchecked_categories_${this.opportunityId}`);
        const uncheckedIds: number[] = savedRaw ? JSON.parse(savedRaw) : [];

        this.categories = data.map(cat => ({
          ...cat,
          checked: !uncheckedIds.includes(cat.category_id)
        }));
        this.filteredCategories = this.categories;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Error loading categories.';
        this.loading = false;
        this.cdr.detectChanges();
        console.error(err);
      }
    });
  }

  onSearch(): void {
    const term = this.searchTerm.toLowerCase().trim();
    this.filteredCategories = this.categories.filter(cat =>
      cat.category_name.toLowerCase().includes(term)
    );
  }

  toggleCheck(cat: Category): void {
    cat.checked = !cat.checked;
  }

  onSave(): void {
    const uncheckedIds = this.categories
      .filter(cat => !cat.checked)
      .map(cat => cat.category_id);

    sessionStorage.setItem(
      `unchecked_categories_${this.opportunityId}`,
      JSON.stringify(uncheckedIds)
    );

    this.router.navigate(['/'], { queryParams: { view: 'imported', reopen: this.opportunityId  } });
  }
}