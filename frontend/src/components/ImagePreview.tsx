import { useEffect, useState } from "react";

import { formatFileSize } from "../utils/format";

interface ImagePreviewProps {
  label: string;
  file: File | null;
}

export default function ImagePreview({ label, file }: ImagePreviewProps) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!file || !file.type.startsWith("image/")) {
      setPreviewUrl(null);
      return undefined;
    }

    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  return (
    <figure className="preview-card">
      <figcaption className="preview-card__label">{label}</figcaption>

      <div className="preview-card__frame">
        {previewUrl ? (
          <img
            className="preview-card__image"
            src={previewUrl}
            alt={`${label} preview`}
          />
        ) : (
          <div className="preview-card__placeholder">
            <span>No preview yet</span>
            <small>Select an image to stage this document.</small>
          </div>
        )}
      </div>

      <p className="preview-card__meta">
        {file ? `${file.name} · ${formatFileSize(file.size)}` : "Awaiting file"}
      </p>
    </figure>
  );
}
