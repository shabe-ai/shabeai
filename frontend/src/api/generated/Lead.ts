export interface LeadCreate {
  email: string;
  firstName: string;
  lastName: string;
  phone?: string | null;
  companyId?: string | null;
}

export interface LeadOut {
  email: string;
  firstName: string;
  lastName: string;
  phone?: string | null;
  companyId?: string | null;
  id: string;
}

export interface Lead {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string | null;
  linkedinUrl?: string | null;
  companyId?: string | null;
  createdAt: string;
} 