import type { VerificationSummary as VerificationSummaryData } from "../types/api";
import { formatIsoDateTime, formatLabel } from "../utils/format";

interface VerificationSummaryProps {
  checkedAt: string | null;
  summary: VerificationSummaryData | null;
}

export default function VerificationSummary({
  checkedAt,
  summary,
}: VerificationSummaryProps) {
  if (!summary) {
    return (
      <div className="empty-state">
        Verification results will appear here once the mock eligibility flow is
        complete.
      </div>
    );
  }

  return (
    <div className="summary-stack">
      <div className="summary-grid">
        <article className="stat-card">
          <span className="stat-card__label">Verification Status</span>
          <strong
            className={`status-pill status-pill--${summary.verificationStatus}`}
          >
            {formatLabel(summary.verificationStatus)}
          </strong>
        </article>

        <article className="stat-card">
          <span className="stat-card__label">Coverage Status</span>
          <strong
            className={`status-pill status-pill--coverage-${summary.coverageStatus}`}
          >
            {formatLabel(summary.coverageStatus)}
          </strong>
        </article>

        <article className="stat-card">
          <span className="stat-card__label">Payer Name</span>
          <strong>{summary.payerName}</strong>
        </article>

        <article className="stat-card">
          <span className="stat-card__label">Member ID</span>
          <strong>{summary.memberId}</strong>
        </article>
      </div>

      <div className="summary-grid summary-grid--secondary">
        <article className="summary-card">
          <h3>Copays</h3>
          <div className="copay-grid">
            {Object.entries(summary.copays).map(([key, value]) => (
              <div className="copay-item" key={key}>
                <span>{formatLabel(key)}</span>
                <strong>{value}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="summary-card">
          <h3>Pharmacy Info</h3>
          <dl className="detail-list">
            <div>
              <dt>BIN</dt>
              <dd>{summary.pharmacyInfo.bin}</dd>
            </div>
            <div>
              <dt>PCN</dt>
              <dd>{summary.pharmacyInfo.pcn}</dd>
            </div>
            <div>
              <dt>Group</dt>
              <dd>{summary.pharmacyInfo.group}</dd>
            </div>
            <div>
              <dt>Processor</dt>
              <dd>{summary.pharmacyInfo.processor}</dd>
            </div>
          </dl>
        </article>
      </div>

      <article className="summary-card">
        <div className="summary-card__header">
          <h3>Discrepancies</h3>
          <span>{checkedAt ? `Checked ${formatIsoDateTime(checkedAt)}` : ""}</span>
        </div>

        {summary.discrepancies.length === 0 ? (
          <div className="empty-state">
            No discrepancies were found in the mock response.
          </div>
        ) : (
          <ul className="discrepancy-list">
            {summary.discrepancies.map((discrepancy) => (
              <li className="discrepancy-item" key={discrepancy.field}>
                <div className="discrepancy-item__header">
                  <strong>{formatLabel(discrepancy.field)}</strong>
                  <span>{discrepancy.note}</span>
                </div>
                <div className="discrepancy-item__values">
                  <p>
                    <span>Extracted</span>
                    <strong>{discrepancy.extractedValue}</strong>
                  </p>
                  <p>
                    <span>Verified</span>
                    <strong>{discrepancy.verifiedValue}</strong>
                  </p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </article>
    </div>
  );
}
