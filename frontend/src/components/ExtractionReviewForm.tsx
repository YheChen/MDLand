import type { ReviewFormValues } from "../types/api";
import { INSURANCE_FIELDS, PATIENT_FIELDS } from "../utils/constants";

interface ExtractionReviewFormProps {
  values: ReviewFormValues;
  disabled: boolean;
  isVerifying: boolean;
  onChange: (field: keyof ReviewFormValues, value: string) => void;
  onVerify: () => void;
}

export default function ExtractionReviewForm({
  values,
  disabled,
  isVerifying,
  onChange,
  onVerify,
}: ExtractionReviewFormProps) {
  return (
    <div className="panel__body">
      <fieldset className="form-shell" disabled={disabled || isVerifying}>
        <div className="form-section">
          <div className="form-section__header">
            <h3>Patient Details</h3>
            <p>Review OCR output and correct anything before verification.</p>
          </div>

          <div className="form-grid">
            {PATIENT_FIELDS.map((field) => (
              <label className="field" key={field.key}>
                <span className="field__label">{field.label}</span>
                <input
                  autoComplete={field.autoComplete}
                  onChange={(event) => onChange(field.key, event.target.value)}
                  placeholder={field.placeholder}
                  type={field.key === "dateOfBirth" ? "date" : "text"}
                  value={values[field.key]}
                />
              </label>
            ))}
          </div>
        </div>

        <div className="form-section">
          <div className="form-section__header">
            <h3>Insurance Details</h3>
            <p>Use local state for now so we can shape the API contract later.</p>
          </div>

          <div className="form-grid">
            {INSURANCE_FIELDS.map((field) => (
              <label className="field" key={field.key}>
                <span className="field__label">{field.label}</span>
                <input
                  autoComplete={field.autoComplete}
                  onChange={(event) => onChange(field.key, event.target.value)}
                  placeholder={field.placeholder}
                  type="text"
                  value={values[field.key]}
                />
              </label>
            ))}
          </div>
        </div>
      </fieldset>

      <div className="panel__actions">
        <button
          className="button button--primary"
          disabled={disabled || isVerifying}
          onClick={onVerify}
          type="button"
        >
          {isVerifying ? "Verifying..." : "Verify Eligibility"}
        </button>
      </div>
    </div>
  );
}
