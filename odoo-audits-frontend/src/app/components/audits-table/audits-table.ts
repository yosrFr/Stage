import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Opportunities, Opportunity } from '../../services/opportunities';

@Component({
  selector: 'app-audits-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audits-table.html',
  styleUrls: ['./audits-table.css']
})
export class AuditsTableComponent implements OnInit {
  opportunities: Opportunity[] = [];
  loading = true;
  error: string | null = null;

  constructor(
    private opportunitiesService: Opportunities,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
  this.opportunitiesService.syncCleanup().subscribe({
    next: () => {
      this.loadOpportunities();
    },
    error: (err) => {
      console.error('Erreur sync cleanup:', err);
      this.loadOpportunities(); // on charge quand même même si le nettoyage échoue
    }
  });
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
  onImport(opportunityId: number): void {
  this.opportunitiesService.importOpportunity(opportunityId).subscribe({
    next: (res: any) => {
      alert('Import réussi ! customer_id=' + res.customer_id + ', norm_id=' + res.norm_id);
      // Retire immédiatement la ligne de l'affichage, sans attendre un rechargement
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
}