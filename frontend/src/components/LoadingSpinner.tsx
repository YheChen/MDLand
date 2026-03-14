interface LoadingSpinnerProps {
  label: string;
}

export default function LoadingSpinner({ label }: LoadingSpinnerProps) {
  return (
    <div aria-live="polite" className="loading-spinner" role="status">
      <span aria-hidden="true" className="loading-spinner__ring" />
      <span>{label}</span>
    </div>
  );
}
