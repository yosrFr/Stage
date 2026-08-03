import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isPlatformServer } from '@angular/common';
import { Observable } from 'rxjs';

export interface Opportunity {
  opportunity_id: number;
  audits: {
    id: number;
    norme: string;
    product_id: number;
    product_tag: string;
    product_tag_id: number;
    type: string;
    date_of_order: string;
    title: string;
    protection_needs?: string;
  };
  customer_information: {
    id: number;
    company_name: string;
    street: string;
    zip: string;
    location: string;
    country: string;
    language: string;
    email: string;
    phone: string;
  };
  contact_information: {
    id: number;
    main_contact: string;
    email: string;
    phone: string;
  };
  internal_account_manager: {
    name: string;
    email: string;
    notes: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class Opportunities {
  private baseUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // Côté serveur (SSR, dans le conteneur) -> utiliser le nom du service Docker
    // Côté navigateur (client) -> utiliser localhost, accessible via le port mappé
    this.baseUrl = isPlatformServer(this.platformId)
      ? 'http://backend:8000'
      : 'http://127.0.0.1:8000';
  }

  getOpportunities(): Observable<Opportunity[]> {
    return this.http.get<Opportunity[]>(`${this.baseUrl}/opportunities`);
  }

  importOpportunity(opportunityId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/opportunities/import/${opportunityId}`, {});
  }

  syncCleanup(): Observable<any> {
    return this.http.post(`${this.baseUrl}/opportunities/sync-cleanup`, {});
  }

  deleteAudit(opportunityId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/audit/${opportunityId}`);
  }

  getImportedOpportunities(): Observable<Opportunity[]> {
    return this.http.get<Opportunity[]>(`${this.baseUrl}/opportunities/imported-opportunities`);
  }

  updateProtectionNeeds(opportunityId: number, protectionNeeds: string, categoryIds: number[]): Observable<any> {
  return this.http.patch(`${this.baseUrl}/opportunities/audit/${opportunityId}/protection-needs`, {
    protection_needs: protectionNeeds,
    category_ids: categoryIds
  });
}
}