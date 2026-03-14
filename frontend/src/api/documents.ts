import { apiClient } from "./client";
import type { ExtractionResponse } from "../types/api";

export async function extractDocuments(
  formData: FormData,
): Promise<ExtractionResponse> {
  const response = await apiClient.post<ExtractionResponse>(
    "/documents/extract",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}
