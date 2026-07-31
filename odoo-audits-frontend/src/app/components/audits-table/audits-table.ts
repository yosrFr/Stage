import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Opportunities, Opportunity } from '../../services/opportunities';

@Component({
  selector: 'app-audits-table',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './audits-table.html',
  styleUrls: ['./audits-table.css']
})
export class AuditsTableComponent implements OnInit {
  opportunities: Opportunity[] = [];
  loading = true;
  error: string | null = null;

  viewMode: 'not-imported' | 'imported' = 'not-imported';

  constructor(
    private opportunitiesService: Opportunities,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.opportunitiesService.syncCleanup().subscribe({
      next: () => {
        this.loadCurrentView();
      },
      error: (err) => {
        console.error('Erreur sync cleanup:', err);
        this.loadCurrentView();
      }
    });
  }

  switchView(mode: 'not-imported' | 'imported'): void {
    if (this.viewMode === mode) return;
    this.viewMode = mode;
    this.loading = true;
    this.loadCurrentView();
  }

  loadCurrentView(): void {
    if (this.viewMode === 'not-imported') {
      this.loadOpportunities();
    } else {
      this.loadImportedOpportunities();
    }
  }

  loadOpportunities(): void {
    this.opportunitiesService.getOpportunities().subscribe({
      next: (data) => {
        this.opportunities = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des données.';
        this.loading = false;
        this.cdr.detectChanges();
        console.error(err);
      }
    });
  }

  loadImportedOpportunities(): void {
    this.opportunitiesService.getImportedOpportunities().subscribe({
      next: (data) => {
        this.opportunities = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des données.';
        this.loading = false;
        this.cdr.detectChanges();
        console.error(err);
      }
    });
  }

  onImport(opportunityId: number): void {
    this.opportunitiesService.importOpportunity(opportunityId).subscribe({
      next: (res: any) => {
        this.opportunities = this.opportunities.filter(
          opp => opp.opportunity_id !== opportunityId
        );
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        alert('Erreur import : ' + (err.error?.error || err.message));
        console.error(err);
      }
    });
  }
showEditModal = false;
editingOpportunityId: number | null = null;
selectedProtectionNeeds: string = '';

selectedNorm: string = '';

onEditClick(opp: Opportunity): void {
  this.editingOpportunityId = opp.opportunity_id;
  this.selectedProtectionNeeds = opp.audits.protection_needs || '';
  this.selectedNorm = opp.audits.norme;
  this.showEditModal = true;
}

closeEditModal(): void {
  this.showEditModal = false;
  this.editingOpportunityId = null;
  this.selectedProtectionNeeds = '';
}

saveProtectionNeeds(): void {
  if (!this.editingOpportunityId || !this.selectedProtectionNeeds) return;

  this.opportunitiesService.updateProtectionNeeds(this.editingOpportunityId, this.selectedProtectionNeeds).subscribe({
    next: () => {
      const opp = this.opportunities.find(o => o.opportunity_id === this.editingOpportunityId);
      if (opp) {
        opp.audits.protection_needs = this.selectedProtectionNeeds;
      }
      this.closeEditModal();
      this.cdr.detectChanges();
    },
    error: (err) => {
      alert('Erreur mise à jour : ' + (err.error?.error || err.message));
      console.error(err);
    }
  });
}
}