import type {
  Insurance,
  Patient,
  ReviewFormValues,
  SelectedDocuments,
} from "../types/api";

export interface DocumentFieldConfig {
  key: keyof SelectedDocuments;
  label: string;
  helper: string;
  accept: string;
}

export interface PatientFieldConfig {
  key: keyof Patient;
  label: string;
  autoComplete: string;
}

export interface InsuranceFieldConfig {
  key: keyof Insurance;
  label: string;
  autoComplete: string;
}

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

export const DOCUMENT_FIELDS: DocumentFieldConfig[] = [
  {
    key: "driversLicense",
    label: "Driver's License",
    helper: "Front image used to capture patient identity and address.",
    accept: "image/*",
  },
  {
    key: "insuranceId",
    label: "Insurance ID",
    helper: "Capture payer, member, group, and any visible Rx processing details.",
    accept: "image/*",
  },
];

export const PATIENT_FIELDS: PatientFieldConfig[] = [
  {
    key: "firstName",
    label: "First Name",
    autoComplete: "given-name",
  },
  {
    key: "middleName",
    label: "Middle Name",
    autoComplete: "additional-name",
  },
  {
    key: "lastName",
    label: "Last Name",
    autoComplete: "family-name",
  },
  {
    key: "dateOfBirth",
    label: "DOB",
    autoComplete: "bday",
  },
  {
    key: "address",
    label: "Address",
    autoComplete: "street-address",
  },
  {
    key: "city",
    label: "City",
    autoComplete: "address-level2",
  },
  {
    key: "state",
    label: "State",
    autoComplete: "address-level1",
  },
  {
    key: "postalCode",
    label: "Postal Code",
    autoComplete: "postal-code",
  },
];

export const INSURANCE_FIELDS: InsuranceFieldConfig[] = [
  {
    key: "payerName",
    label: "Payer Name",
    autoComplete: "organization",
  },
  {
    key: "payerId",
    label: "Payer ID",
    autoComplete: "off",
  },
  {
    key: "memberId",
    label: "Member ID",
    autoComplete: "off",
  },
  {
    key: "groupNumber",
    label: "Group Number",
    autoComplete: "off",
  },
  {
    key: "rxBin",
    label: "Rx BIN",
    autoComplete: "off",
  },
  {
    key: "rxPcn",
    label: "Rx PCN",
    autoComplete: "off",
  },
  {
    key: "rxGroup",
    label: "Rx Group",
    autoComplete: "off",
  },
];

export const EMPTY_PATIENT: Patient = {
  firstName: "",
  middleName: "",
  lastName: "",
  dateOfBirth: "",
  address: "",
  city: "",
  state: "",
  postalCode: "",
};

export const EMPTY_INSURANCE: Insurance = {
  payerName: "",
  payerId: "",
  memberId: "",
  groupNumber: "",
  rxBin: "",
  rxPcn: "",
  rxGroup: "",
};

export const EMPTY_REVIEW_FORM: ReviewFormValues = {
  ...EMPTY_PATIENT,
  ...EMPTY_INSURANCE,
};

export const INITIAL_SELECTED_DOCUMENTS: SelectedDocuments = {
  driversLicense: null,
  insuranceId: null,
};
