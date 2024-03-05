interface Audit {
  id: string;
  weight: number;
  group?: string;
}

interface Category {
  id: string;
  title: string;
  description?: string;
  score: number;
  manualDescription?: string;
  auditRefs: Audit[];
}

interface PerformanceCategory extends Category {
  auditRefs: Audit[];
}

interface AccessibilityCategory extends Category {
  auditRefs: Audit[];
}

interface BestPracticesCategory extends Category {
  auditRefs: Audit[];
}

interface SEOCategory extends Category {
  auditRefs: Audit[];
}

interface PWACategory extends Category {
  auditRefs: Audit[];
}

interface LighthouseData {
  performance: PerformanceCategory;
  accessibility: AccessibilityCategory;
  bestPractices: BestPracticesCategory;
  seo: SEOCategory;
  pwa: PWACategory;
}

export interface Insights {
  deviceData: { mobile: LighthouseData; desktop: LighthouseData };
}
