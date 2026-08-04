import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray} from '@angular/forms';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface FamilyNorm {
  family_norm_id: number;
  name: string;
}

@Component({
  selector: 'app-fields',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './fields.html',
  styleUrls: ['./fields.css']
})
export class FieldsComponent implements OnInit {
  form: FormGroup;
  private baseUrl = 'http://127.0.0.1:8000';

  familyNorms: FamilyNorm[] = [];
  selectedFamilyNormId: number | null = null;

  imagePreviews: { [key: string]: string | null } = {
    background: null,
    cover_page_logo: null,
    header_logo: null,
    last_page_background: null
  };

  imageFieldsChanged: { [key: string]: boolean } = {
    background: false,
    cover_page_logo: false,
    header_logo: false,
    last_page_background: false
  };

  loadingConfig = false;
  saving = false;
  saveMessage = '';

  constructor(private fb: FormBuilder, private http: HttpClient, private cdr: ChangeDetectorRef) {
    this.form = this.fb.group({
      web_page_link: [''],
      disable_page: this.fb.group({
        evaluation_results_summary: [true],
        risk_level_dist: [true],
        maturity_level_assessment: [true],
        list_non_conformity: [true]
      }),
      list_abbreviation: this.fb.array([]),
      maturity_levels: this.fb.array([]),
      risk_levels: this.fb.array([]),
      initiation: [''],
      introduction: [''],
      organisation: [''],
      overall_summary_chart_title: [''],
      maturity_assessment_section_title: [''],
      maturity_assessment_chart_title: [''],
      report_title: this.createTextStyleGroup(),
      header1: this.createTextStyleGroup(),
      header2: this.createTextStyleGroup(),
      header3: this.createTextStyleGroup(),
      text: this.createTextStyleGroup(),
      table_header_bg_color: ['#000028'],
      audit_report_colors: this.fb.group({
        color_1: ['#000028'],
        color_2: ['#32fae6']
      }),
      gradient: [true]
    });
  }

  ngOnInit(): void {
    this.loadFamilyNorms();
  }

  loadFamilyNorms(): void {
    this.http.get<FamilyNorm[]>(`${this.baseUrl}/report-config/family-norms`).subscribe({
      next: (data) => {
        this.familyNorms = data;
        if (data.length > 0) {
          this.selectedFamilyNormId = data[0].family_norm_id;
          this.loadConfig();
        }
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Erreur chargement family norms:', err)
    });
  }
  private resetForm(): void {
  this.form.reset({
    web_page_link: '',
    disable_page: {
      evaluation_results_summary: true,
      risk_level_dist: true,
      maturity_level_assessment: true,
      list_non_conformity: true
    },
    initiation: '',
    introduction: '',
    organisation: '',
    overall_summary_chart_title: '',
    maturity_assessment_section_title: '',
    maturity_assessment_chart_title: '',
    report_title: { font_family: 'Montserrat Bold', font_color: '#000028', font_size: 14 },
    header1: { font_family: 'Montserrat Bold', font_color: '#000028', font_size: 14 },
    header2: { font_family: 'Montserrat Bold', font_color: '#000028', font_size: 14 },
    header3: { font_family: 'Montserrat Bold', font_color: '#000028', font_size: 14 },
    text: { font_family: 'Montserrat Bold', font_color: '#000028', font_size: 14 },
    table_header_bg_color: '#000028',
    audit_report_colors: { color_1: '#000028', color_2: '#32fae6' },
    gradient: true
  });

  this.abbreviations.clear();
  this.addAbbreviationRow();
  this.maturityLevels.clear();
  this.addMaturityLevelRow();
  this.riskLevels.clear();
  this.addRiskLevelRow();

  const imgFields = ['background', 'cover_page_logo', 'header_logo', 'last_page_background'];
  imgFields.forEach(field => {
    this.imagePreviews[field] = null;
    this.imageFieldsChanged[field] = false;
  });
}

  onFamilyNormChange(): void {
    this.loadConfig();
  }

  createTextStyleGroup(): FormGroup {
    return this.fb.group({
      font_family: ['Montserrat Bold'],
      font_color: ['#000028'],
      font_size: [14]
    });
  }

  createAbbreviationRow(abbreviation = '', description = ''): FormGroup {
    return this.fb.group({ abbreviation: [abbreviation], description: [description] });
  }

  createLevelRow(name = '', color = '#000000', description = ''): FormGroup {
    return this.fb.group({ name: [name], color: [color], description: [description] });
  }

  get abbreviations(): FormArray {
    return this.form.get('list_abbreviation') as FormArray;
  }

  get maturityLevels(): FormArray {
    return this.form.get('maturity_levels') as FormArray;
  }

  get riskLevels(): FormArray {
    return this.form.get('risk_levels') as FormArray;
  }

  addAbbreviationRow(): void {
    this.abbreviations.push(this.createAbbreviationRow());
  }

  removeAbbreviationRow(index: number): void {
    this.abbreviations.removeAt(index);
  }

  addMaturityLevelRow(): void {
    this.maturityLevels.push(this.createLevelRow());
  }

  removeMaturityLevelRow(index: number): void {
    this.maturityLevels.removeAt(index);
  }

  addRiskLevelRow(): void {
    this.riskLevels.push(this.createLevelRow());
  }

  removeRiskLevelRow(index: number): void {
    this.riskLevels.removeAt(index);
  }

  onImageSelected(event: Event, fieldName: string): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      this.imagePreviews[fieldName] = reader.result as string;
      this.imageFieldsChanged[fieldName] = true;
    };

    reader.readAsDataURL(file);
  }

  loadConfig(): void {
    if (this.selectedFamilyNormId === null) return;

    this.loadingConfig = true;

    this.http.get<any>(`${this.baseUrl}/report-config/${this.selectedFamilyNormId}`).subscribe({
      next: (data) => {
        if (!data.exists) {
          this.resetForm();
          this.loadingConfig = false;
          this.cdr.detectChanges();
          return;
  }
        this.form.patchValue({
          web_page_link: data.web_page_link || '',
          disable_page: {
            evaluation_results_summary: data.evaluation_results_summary,
            risk_level_dist: data.risk_level_dist,
            maturity_level_assessment: data.maturity_level_assessment,
            list_non_conformity: data.list_non_conformity
          },
          initiation: data.initiation || '',
          introduction: data.introduction || '',
          organisation: data.organisation || '',
          overall_summary_chart_title: data.overall_summary_chart_title || '',
          maturity_assessment_section_title: data.maturity_assessment_section_title || '',
          maturity_assessment_chart_title: data.maturity_assessment_chart_title || '',
          report_title: data.report_title,
          header1: data.header1,
          header2: data.header2,
          header3: data.header3,
          text: data.text,
          table_header_bg_color: data.table_header_bg_color || '#000028',
          audit_report_colors: data.audit_report_colors,
          gradient: data.gradient
        });

        this.abbreviations.clear();
        (data.list_abbreviation || []).forEach((row: any) => {
          this.abbreviations.push(this.createAbbreviationRow(row.abbreviation, row.description));
        });
        if (this.abbreviations.length === 0) this.addAbbreviationRow();

        this.maturityLevels.clear();
        (data.maturity_levels || []).forEach((row: any) => {
          this.maturityLevels.push(this.createLevelRow(row.name, row.color, row.description));
        });
        if (this.maturityLevels.length === 0) this.addMaturityLevelRow();

        this.riskLevels.clear();
        (data.risk_levels || []).forEach((row: any) => {
          this.riskLevels.push(this.createLevelRow(row.name, row.color, row.description));
        });
        if (this.riskLevels.length === 0) this.addRiskLevelRow();

        const imgFields = ['background', 'cover_page_logo', 'header_logo', 'last_page_background'];
        imgFields.forEach(field => {
          this.imagePreviews[field] = data[field] ? `data:image/png;base64,${data[field]}` : null;
          this.imageFieldsChanged[field] = false;
        });

        this.loadingConfig = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loadingConfig = false;
        this.cdr.detectChanges();
        console.error('Erreur chargement config:', err);
      }
    });
  }

  onSave(): void {
    if (this.selectedFamilyNormId === null) return;

    this.saving = true;
    this.saveMessage = '';
    this.cdr.detectChanges();

    const v = this.form.value;

    const payload = {
      web_page_link: v.web_page_link,
      evaluation_results_summary: v.disable_page.evaluation_results_summary,
      risk_level_dist: v.disable_page.risk_level_dist,
      maturity_level_assessment: v.disable_page.maturity_level_assessment,
      list_non_conformity: v.disable_page.list_non_conformity,
      initiation: v.initiation,
      introduction: v.introduction,
      organisation: v.organisation,
      overall_summary_chart_title: v.overall_summary_chart_title,
      maturity_assessment_section_title: v.maturity_assessment_section_title,
      maturity_assessment_chart_title: v.maturity_assessment_chart_title,
      report_title_font_family: v.report_title.font_family,
      report_title_font_color: v.report_title.font_color,
      report_title_font_size: v.report_title.font_size,
      header1_font_family: v.header1.font_family,
      header1_font_color: v.header1.font_color,
      header1_font_size: v.header1.font_size,
      header2_font_family: v.header2.font_family,
      header2_font_color: v.header2.font_color,
      header2_font_size: v.header2.font_size,
      header3_font_family: v.header3.font_family,
      header3_font_color: v.header3.font_color,
      header3_font_size: v.header3.font_size,
      text_font_family: v.text.font_family,
      text_font_color: v.text.font_color,
      text_font_size: v.text.font_size,
      table_header_bg_color: v.table_header_bg_color,
      audit_report_color_1: v.audit_report_colors.color_1,
      audit_report_color_2: v.audit_report_colors.color_2,
      gradient: v.gradient,
      list_abbreviation: v.list_abbreviation,
      maturity_levels: v.maturity_levels,
      risk_levels: v.risk_levels
    };

    this.http.patch(`${this.baseUrl}/report-config/${this.selectedFamilyNormId}`, payload).subscribe({
      next: () => this.uploadChangedImages(),
      error: (err) => {
        this.saving = false;
        this.saveMessage = 'Error saving configuration.';
        this.cdr.detectChanges();
        console.error(err);
      }
    });
  }

  private uploadChangedImages(): void {
    const imgFields = ['background', 'cover_page_logo', 'header_logo', 'last_page_background'];
    const toUpload = imgFields.filter(f => this.imageFieldsChanged[f] && this.imagePreviews[f]);

    if (toUpload.length === 0) {
      this.finishSave();
      return;
    }

    let remaining = toUpload.length;

    toUpload.forEach(field => {
      this.http.post(`${this.baseUrl}/report-config/${this.selectedFamilyNormId}/image/${field}`, {
        image_base64: this.imagePreviews[field]
      }).subscribe({
        next: () => {
          this.imageFieldsChanged[field] = false;
          remaining--;
          if (remaining === 0) this.finishSave();
        },
        error: (err) => {
          console.error(`Erreur upload image ${field}:`, err);
          remaining--;
          if (remaining === 0) this.finishSave();
        }
      });
    });
  }

  private finishSave(): void {
    this.saving = false;
    this.saveMessage = 'Configuration saved successfully.';
    this.cdr.detectChanges();
    setTimeout(() => {
      this.saveMessage = '';
      this.cdr.detectChanges();
    }, 3000);
  }

  onCancel(): void {
    this.loadConfig();
  }
}