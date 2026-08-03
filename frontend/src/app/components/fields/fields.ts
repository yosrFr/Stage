import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-fields',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './fields.html',
  styleUrls: ['./fields.css']
})
export class FieldsComponent {
  form: FormGroup;

  imagePreviews: { [key: string]: string | null } = {
    background: null,
    cover_page_logo: null,
    header_logo: null,
    last_page_background: null
  };

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      background: [null],
      cover_page_logo: [null],
      header_logo: [null],
      web_page_link: [''],
      last_page_background: [null],
      disable_page: this.fb.group({
        evaluation_results_summary: [true],
        risk_level_dist: [true],
        maturity_level_assessment: [true],
        list_non_conformity: [true]
      }),
      list_abbreviation: this.fb.array([this.createAbbreviationRow()]),
      maturity_levels: this.fb.array([this.createMaturityLevelRow()]),
      risk_levels: this.fb.array([this.createRiskLevelRow()]),
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

  get abbreviations(): FormArray {
    return this.form.get('list_abbreviation') as FormArray;
  }

  get maturityLevels(): FormArray {
    return this.form.get('maturity_levels') as FormArray;
  }

  createAbbreviationRow(): FormGroup {
    return this.fb.group({
      abbreviation: [''],
      description: ['']
    });
  }

  createMaturityLevelRow(): FormGroup {
    return this.fb.group({
      name: [''],
      color: ['#000000'],
      description: ['']
    });
  }
  createRiskLevelRow(): FormGroup {
  return this.fb.group({
    name: [''],
    color: ['#000000'],
    description: ['']
  });
}

createTextStyleGroup(): FormGroup {
  return this.fb.group({
    font_family: ['Montserrat Bold'],
    font_color: ['#000028'],
    font_size: [14]
  });
}

get riskLevels(): FormArray {
  return this.form.get('risk_levels') as FormArray;
}

addRiskLevelRow(): void {
  this.riskLevels.push(this.createRiskLevelRow());
}

removeRiskLevelRow(index: number): void {
  this.riskLevels.removeAt(index);
}

  addAbbreviationRow(): void {
    this.abbreviations.push(this.createAbbreviationRow());
  }

  removeAbbreviationRow(index: number): void {
    this.abbreviations.removeAt(index);
  }

  addMaturityLevelRow(): void {
    this.maturityLevels.push(this.createMaturityLevelRow());
  }

  removeMaturityLevelRow(index: number): void {
    this.maturityLevels.removeAt(index);
  }

  onImageSelected(event: Event, fieldName: string): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      const result = reader.result as string;
      this.imagePreviews[fieldName] = result;
      this.form.get(fieldName)?.setValue(result);
    };

    reader.readAsDataURL(file);
  }
}