import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
  private apiUrl = 'http://127.0.0.1:8000/opportunities';

  constructor(private http: HttpClient) {}

  getOpportunities(): Observable<Opportunity[]> {
    return this.http.get<Opportunity[]>(this.apiUrl);
  }
  importOpportunity(opportunityId: number): Observable<any> {
  return this.http.post(`http://127.0.0.1:8000/import/${opportunityId}`, {});
}
syncCleanup(): Observable<any> {
  return this.http.post('http://127.0.0.1:8000/opportunities/sync-cleanup', {});
}
deleteAudit(opportunityId: number): Observable<any> {
  return this.http.delete(`http://127.0.0.1:8000/audit/${opportunityId}`);
}
getImportedOpportunities(): Observable<Opportunity[]> {
  return this.http.get<Opportunity[]>('http://127.0.0.1:8000/imported-opportunities');
}
updateProtectionNeeds(opportunityId: number, protectionNeeds: string): Observable<any> {
  return this.http.patch(`http://127.0.0.1:8000/audit/${opportunityId}/protection-needs`, {
    protection_needs: protectionNeeds
  });
}
}