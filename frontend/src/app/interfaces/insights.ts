export interface AuditResult {
  domain: string;
  checkTime: string;
  overallScore: number;
  grade: string;
  screenshots: string[];
  results: {
    mobile: any;
    desktop: any;
  };
  audits: {
    mobile: any;
    desktop: any;
  };
}
