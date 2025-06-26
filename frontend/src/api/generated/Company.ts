export interface CompanyCreate {
  name: string;
  website?: string | null;
  linkedinUrl?: string | null;
}

export interface CompanyOut {
  name: string;
  website?: string | null;
  linkedinUrl?: string | null;
  id: string;
}

export interface Company {
  id: string;
  name: string;
  website?: string | null;
  linkedinUrl?: string | null;
  createdAt: string;
} 