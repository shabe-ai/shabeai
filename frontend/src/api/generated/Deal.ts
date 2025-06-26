export interface DealCreate {
  title: string;
  value: number;
  stage?: string;
  companyId: string;
}

export interface DealOut {
  title: string;
  value: number;
  stage?: string;
  companyId: string;
  id: string;
}

export interface Deal {
  id: string;
  title: string;
  value: number;
  stage: string;
  companyId: string;
  createdAt: string;
} 