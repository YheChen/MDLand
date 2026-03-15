import type { Warning } from "../types/api";

interface WarningListProps {
  emptyMessage?: string;
  warnings: Warning[];
}

export default function WarningList({
  emptyMessage,
  warnings,
}: WarningListProps) {
  if (warnings.length === 0) {
    return (
      <div className="empty-state">
        {emptyMessage ??
          "No warnings yet. They will appear after verification if something needs front-desk attention."}
      </div>
    );
  }

  return (
    <ul className="warning-list">
      {warnings.map((warning) => (
        <li className={`warning-item warning-item--${warning.severity}`} key={warning.code}>
          <div>
            <strong>{warning.code}</strong>
            <p>{warning.message}</p>
          </div>
          <span className="warning-item__severity">{warning.severity}</span>
        </li>
      ))}
    </ul>
  );
}
