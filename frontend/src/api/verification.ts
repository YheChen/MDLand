import { apiClient } from "./client";
import type { VerificationRequest, VerificationResponse } from "../types/api";

export async function verifyEligibility(
  payload: VerificationRequest,
): Promise<VerificationResponse> {
  const response = await apiClient.post<VerificationResponse>(
    "/verification/verify",
    payload,
  );

  return response.data;
}
