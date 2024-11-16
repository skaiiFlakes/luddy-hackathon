// types/kpi.ts
export interface KpiInfo {
  description: string;
  unit: string;
  abbr: string;
}

export interface KpiDictionary {
  [key: string]: KpiInfo;
}

// utils/kpiData.ts
export const kpis: KpiDictionary = {
  'Customer Acquisition Cost': {
    description:
      'The total cost of acquiring a new customer, including marketing and sales expenses.',
    unit: 'USD',
    abbr: 'CAC',
  },
  'Churn Rate': {
    description:
      'The percentage of customers who stop using your product/service over a given time period.',
    unit: '%',
    abbr: 'CR',
  },
  'Average Order Size': {
    description:
      'The average monetary value of each order placed by customers.',
    unit: 'USD',
    abbr: 'AOS',
  },
  'Monthly Recurring Revenue': {
    description: 'Predictable revenue generated each month from subscriptions.',
    unit: 'USD',
    abbr: 'MRR',
  },
  'Annual Recurring Revenue': {
    description: 'Predictable revenue generated annually from subscriptions.',
    unit: 'USD',
    abbr: 'ARR',
  },
  'Cash Runway': {
    description:
      'The amount of time a company can continue operating with its current cash reserves.',
    unit: 'mos.',
    abbr: 'CR',
  },
  'Burn Rate': {
    description:
      'The rate at which a company spends its cash reserves on operating expenses.',
    unit: 'USD',
    abbr: 'BR',
  },
  'K-factor': {
    description:
      'The growth rate of a product through viral customer acquisition.',
    unit: '',
    abbr: 'KF',
  },
  'Gross Sales': {
    description:
      'Total revenue generated before deductions for returns, discounts, and other expenses.',
    unit: 'USD',
    abbr: 'GS',
  },
  'Monthly Active Users': {
    description:
      'The number of unique users who interact with your product in a month.',
    unit: '#',
    abbr: 'MAU',
  },
  'Net Promoter Score': {
    description: 'Measures customer satisfaction and likelihood to recommend.',
    unit: '',
    abbr: 'NPS',
  },
  'LVT/CAC': {
    description: 'Measures the return on customer acquisition investment.',
    unit: '',
    abbr: 'LVT/CAC',
  },
};
