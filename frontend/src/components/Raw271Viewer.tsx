interface Raw271ViewerProps {
  raw271: string | null;
}

export default function Raw271Viewer({ raw271 }: Raw271ViewerProps) {
  if (!raw271) {
    return (
      <div className="empty-state">
        Raw 271 output will appear here after verification completes.
      </div>
    );
  }

  return (
    <details className="raw-viewer">
      <summary>View Raw 271 Response</summary>
      <pre>{raw271}</pre>
    </details>
  );
}
