import { useEffect, useRef, useState } from "react";

import ErrorBanner from "../components/ErrorBanner";
import ExtractionReviewForm from "../components/ExtractionReviewForm";
import FileUploadSection from "../components/FileUploadSection";
import Layout from "../components/Layout";
import LoadingSpinner from "../components/LoadingSpinner";
import Raw271Viewer from "../components/Raw271Viewer";
import VerificationSummary from "../components/VerificationSummary";
import WarningList from "../components/WarningList";
import type {
  ExtractionResponse,
  ReviewFormValues,
  SelectedDocuments,
  VerificationRequest,
  VerificationResponse,
} from "../types/api";
import { EMPTY_REVIEW_FORM, INITIAL_SELECTED_DOCUMENTS } from "../utils/constants";
import { formatPatientName } from "../utils/format";

const EXTRACTION_DELAY_MS = 900;
const VERIFICATION_DELAY_MS = 1200;

function createEmptyReviewForm(): ReviewFormValues {
  return { ...EMPTY_REVIEW_FORM };
}

function buildReviewFormValues(
  extractionResponse: ExtractionResponse,
): ReviewFormValues {
  return {
    ...extractionResponse.patient,
    ...extractionResponse.insurance,
  };
}

function buildVerificationRequest(
  values: ReviewFormValues,
): VerificationRequest {
  return {
    patient: {
      firstName: values.firstName,
      middleName: values.middleName,
      lastName: values.lastName,
      dateOfBirth: values.dateOfBirth,
      address: values.address,
      city: values.city,
      state: values.state,
      postalCode: values.postalCode,
    },
    insurance: {
      payerName: values.payerName,
      payerId: values.payerId,
      memberId: values.memberId,
      groupNumber: values.groupNumber,
      rxBin: values.rxBin,
      rxPcn: values.rxPcn,
      rxGroup: values.rxGroup,
    },
  };
}

function buildMockExtractionResponse(
  selectedDocuments: SelectedDocuments,
): ExtractionResponse {
  return {
    patient: {
      firstName: "Avery",
      middleName: "Jordan",
      lastName: "Carter",
      dateOfBirth: "1988-11-04",
      address: "123 Harbor Street",
      city: "Baltimore",
      state: "MD",
      postalCode: "21201",
    },
    insurance: {
      payerName: "Blue Cross Blue Shield of Maryland",
      payerId: "BCBSMD01",
      memberId: "XJH123456789",
      groupNumber: "GRP-45029",
      rxBin: "610279",
      rxPcn: "03200000",
      rxGroup: "MDRX01",
    },
    confidence: 0.93,
    documentNotes: [
      `Driver's license staged: ${selectedDocuments.driversLicense?.name ?? "missing"}`,
      `Insurance front staged: ${selectedDocuments.insuranceFront?.name ?? "missing"}`,
      `Insurance back staged: ${selectedDocuments.insuranceBack?.name ?? "missing"}`,
    ],
  };
}

function buildMockVerificationResponse(
  payload: VerificationRequest,
): VerificationResponse {
  const displayName = formatPatientName(payload.patient) || "Member";
  const raw271 = [
    "ISA*00*          *00*          *ZZ*MDLAND         *ZZ*ELIGIBILITY    *260314*1200*^*00501*000000905*0*T*:",
    "GS*HB*MDLAND*ELIGIBILITY*20260314*1200*1*X*005010X279A1",
    "ST*271*0001*005010X279A1",
    "BHT*0022*11*10001234*20260314*1200",
    "HL*1**20*1",
    `NM1*PR*2*${payload.insurance.payerName.toUpperCase()}*****PI*${payload.insurance.payerId}`,
    "HL*2*1*21*1",
    "NM1*1P*2*MDLAND CLINIC*****XX*1234567893",
    "HL*3*2*22*0",
    `TRN*2*MDLAND-DEMO-${payload.insurance.memberId}`,
    `NM1*IL*1*${payload.patient.lastName}*${payload.patient.firstName}****MI*${payload.insurance.memberId}`,
    `DMG*D8*${payload.patient.dateOfBirth.split("-").join("")}`,
    "EB*1**30**PLAN ACTIVE",
    "EB*B**98***PRIMARY CARE $25 COPAY",
    "EB*B**98***SPECIALIST $40 COPAY",
    "EB*B**88***PHARMACY PROCESSOR: MEDRX ADVANCE",
    "SE*16*0001",
    "GE*1*1",
    "IEA*1*000000905",
  ].join("\n");

  return {
    summary: {
      verificationStatus: "verified",
      coverageStatus: "active",
      payerName: payload.insurance.payerName,
      memberId: payload.insurance.memberId,
      copays: {
        primaryCare: "$25",
        specialist: "$40",
        urgentCare: "$60",
        pharmacy: "Tiered copay plan",
      },
      pharmacyInfo: {
        bin: payload.insurance.rxBin,
        pcn: payload.insurance.rxPcn,
        group: payload.insurance.rxGroup,
        processor: "MedRx Advance",
      },
      discrepancies: [
        {
          field: "address",
          extractedValue: payload.patient.address,
          verifiedValue: `${payload.patient.address}, Apt 2`,
          note: "Eligibility source returned a more specific service address.",
        },
      ],
    },
    warnings: [
      {
        code: "COPAY-DUE",
        message: `${displayName} has an office visit copay due at check-in.`,
        severity: "warning",
      },
      {
        code: "PCP-REFERRAL",
        message: "Specialist visits may require PCP referral confirmation.",
        severity: "info",
      },
    ],
    raw271,
    checkedAt: new Date().toISOString(),
  };
}

export default function HomePage() {
  const [selectedDocuments, setSelectedDocuments] = useState<SelectedDocuments>(
    INITIAL_SELECTED_DOCUMENTS,
  );
  const [formValues, setFormValues] = useState<ReviewFormValues>(
    createEmptyReviewForm,
  );
  const [extractionResponse, setExtractionResponse] =
    useState<ExtractionResponse | null>(null);
  const [verificationResponse, setVerificationResponse] =
    useState<VerificationResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);

  const extractTimerRef = useRef<number | null>(null);
  const verifyTimerRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (extractTimerRef.current !== null) {
        window.clearTimeout(extractTimerRef.current);
      }

      if (verifyTimerRef.current !== null) {
        window.clearTimeout(verifyTimerRef.current);
      }
    };
  }, []);

  function resetDownstreamState() {
    if (extractTimerRef.current !== null) {
      window.clearTimeout(extractTimerRef.current);
      extractTimerRef.current = null;
    }

    if (verifyTimerRef.current !== null) {
      window.clearTimeout(verifyTimerRef.current);
      verifyTimerRef.current = null;
    }

    setIsExtracting(false);
    setIsVerifying(false);
    setExtractionResponse(null);
    setVerificationResponse(null);
    setFormValues(createEmptyReviewForm());
  }

  function handleFileChange(
    documentKind: keyof SelectedDocuments,
    file: File | null,
  ) {
    setSelectedDocuments((current) => ({
      ...current,
      [documentKind]: file,
    }));
    setErrorMessage(null);
    resetDownstreamState();
  }

  function handleFormChange(field: keyof ReviewFormValues, value: string) {
    setFormValues((current) => ({
      ...current,
      [field]: value,
    }));
    setErrorMessage(null);
    setVerificationResponse(null);
  }

  function handleExtract() {
    const hasAllDocuments = Object.values(selectedDocuments).every(Boolean);

    if (!hasAllDocuments) {
      setErrorMessage("Please select all three document images before extracting.");
      return;
    }

    if (extractTimerRef.current !== null) {
      window.clearTimeout(extractTimerRef.current);
    }

    if (verifyTimerRef.current !== null) {
      window.clearTimeout(verifyTimerRef.current);
      verifyTimerRef.current = null;
    }

    setErrorMessage(null);
    setIsExtracting(true);
    setIsVerifying(false);
    setVerificationResponse(null);

    extractTimerRef.current = window.setTimeout(() => {
      const mockExtraction = buildMockExtractionResponse(selectedDocuments);
      setExtractionResponse(mockExtraction);
      setFormValues(buildReviewFormValues(mockExtraction));
      setIsExtracting(false);
      extractTimerRef.current = null;
    }, EXTRACTION_DELAY_MS);
  }

  function handleVerify() {
    if (!extractionResponse) {
      setErrorMessage("Run extraction before verifying eligibility.");
      return;
    }

    if (verifyTimerRef.current !== null) {
      window.clearTimeout(verifyTimerRef.current);
    }

    setErrorMessage(null);
    setIsVerifying(true);
    setVerificationResponse(null);

    const verificationPayload = buildVerificationRequest(formValues);

    verifyTimerRef.current = window.setTimeout(() => {
      setVerificationResponse(buildMockVerificationResponse(verificationPayload));
      setIsVerifying(false);
      verifyTimerRef.current = null;
    }, VERIFICATION_DELAY_MS);
  }

  const canExtract = Object.values(selectedDocuments).every(Boolean);

  return (
    <Layout
      subtitle="A frontend-first walkthrough for document intake, extraction review, and mock eligibility verification."
      title="Patient Eligibility Prototype"
    >
      <div className="page-grid">
        {errorMessage ? <ErrorBanner message={errorMessage} /> : null}

        <section className="panel">
          <div className="panel__header">
            <span className="panel__step">01</span>
            <div>
              <h2>Upload Documents</h2>
              <p>
                Stage the driver&apos;s license and both insurance card sides to
                kick off mock extraction.
              </p>
            </div>
          </div>

          <FileUploadSection
            canExtract={canExtract}
            isExtracting={isExtracting}
            onExtract={handleExtract}
            onFileChange={handleFileChange}
            selectedDocuments={selectedDocuments}
          />

          {isExtracting ? (
            <LoadingSpinner label="Simulating document extraction..." />
          ) : null}

          {extractionResponse ? (
            <p className="panel__note">
              Mock extraction confidence:{" "}
              {Math.round(extractionResponse.confidence * 100)}%{" "}
              <span className="panel__note-divider">/</span>{" "}
              {extractionResponse.documentNotes.join(" / ")}
            </p>
          ) : (
            <p className="panel__note">
              Upload all three files, then click Extract to populate the review
              form with mock data.
            </p>
          )}
        </section>

        <section className="panel">
          <div className="panel__header">
            <span className="panel__step">02</span>
            <div>
              <h2>Review Extracted Data</h2>
              <p>
                Correct patient demographics and insurance fields before sending
                a verification request.
              </p>
            </div>
          </div>

          <ExtractionReviewForm
            disabled={!extractionResponse}
            isVerifying={isVerifying}
            onChange={handleFormChange}
            onVerify={handleVerify}
            values={formValues}
          />

          {isVerifying ? (
            <LoadingSpinner label="Simulating eligibility verification and 271 parsing..." />
          ) : null}
        </section>

        <section className="panel">
          <div className="panel__header">
            <span className="panel__step">03</span>
            <div>
              <h2>Front-Desk Summary</h2>
              <p>
                Surface coverage, copays, pharmacy routing, warnings, and raw
                271 output for the intake team.
              </p>
            </div>
          </div>

          <VerificationSummary
            checkedAt={verificationResponse?.checkedAt ?? null}
            summary={verificationResponse?.summary ?? null}
          />

          <div className="summary-subgrid">
            <article className="summary-card">
              <h3>Warnings</h3>
              <WarningList warnings={verificationResponse?.warnings ?? []} />
            </article>

            <article className="summary-card">
              <h3>Raw 271</h3>
              <Raw271Viewer raw271={verificationResponse?.raw271 ?? null} />
            </article>
          </div>
        </section>
      </div>
    </Layout>
  );
}
