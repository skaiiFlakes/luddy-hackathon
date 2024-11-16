import React, { useState, useEffect } from 'react';
import { Label, Select, TextInput } from 'flowbite-react';

const FormGroup = ({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) => (
  <div className='max-w-full lg:flex lg:items-center lg:gap-4'>
    <div className='lg:w-1/3'>
      <Label
        className='text-xl text-gray-300 font-normal leading-relaxed fs521'
        value={label}
      />
    </div>
    <div className='lg:w-2/3'>{children}</div>
  </div>
);

export default function Form() {
  const [industry, setIndustry] = useState('');
  const [kpi, setKpi] = useState('Gross Sales');
  const [currentStatus, setCurrentStatus] = useState('');
  const [targetStatus, setTargetStatus] = useState('');
  const [deadline, setDeadline] = useState('');

  const kpis: {
    [key: string]: { description: string; unit: string; abbr: string };
  } = {
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
      description:
        'Predictable revenue generated each month from subscriptions.',
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
      description:
        'Measures customer satisfaction and likelihood to recommend.',
      unit: '',
      abbr: 'NPS',
    },
    'LVT/CAC': {
      description: 'Measures the return on customer acquisition investment.',
      unit: '',
      abbr: 'LVT/CAC',
    },
  };

  // Effect to log changes
  useEffect(() => {
    console.log('Industry changed:', industry);
  }, [industry]);

  useEffect(() => {
    console.log('KPI changed:', kpi);
  }, [kpi]);

  useEffect(() => {
    console.log('Current Status changed:', currentStatus);
  }, [currentStatus]);

  useEffect(() => {
    console.log('Target Status changed:', targetStatus);
  }, [targetStatus]);

  useEffect(() => {
    console.log('Deadline changed:', deadline);
  }, [deadline]);

  const handleIndustryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setIndustry(event.target.value);
  };

  const handleKpiChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setKpi(event.target.value);
  };

  const handleCurrentStatusChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setCurrentStatus(event.target.value);
  };

  const handleTargetStatusChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setTargetStatus(event.target.value);
  };

  const handleDeadlineChange = (date: Date) => {
    setDeadline(date.toISOString());
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    console.log('Form submitted with values:', {
      industry,
      kpi,
      currentStatus,
      targetStatus,
      deadline,
    });
  };

  return (
    <form onSubmit={handleSubmit} className='space-y-4'>
      <FormGroup label='Industry'>
        <Select
          className='dark'
          id='industries'
          required
          value={industry}
          onChange={handleIndustryChange}
        >
          {[
            'Automotive',
            'Banking',
            'Construction',
            'Education',
            'Energy',
            'Fashion',
            'Food and Beverage',
            'Healthcare',
            'Information Technology',
            'Manufacturing',
            'Media and Entertainment',
            'Real Estate',
            'Retail',
            'Telecommunications',
            'Transportation',
            'Travel and Tourism',
            'Utilities',
            'Wholesale',
            'Not Specified',
          ].map((industry) => (
            <option key={industry} value={industry}>
              {industry}
            </option>
          ))}
        </Select>
      </FormGroup>

      <FormGroup label='KPI'>
        <Select
          className='dark'
          id='kpis'
          required
          value={kpi}
          onChange={handleKpiChange}
        >
          {Object.keys(kpis).map((key) => (
            <option key={key} value={key}>
              {key}
            </option>
          ))}
        </Select>
      </FormGroup>

      {kpi && (
        <div className='max-w-full lg:flex lg:items-center lg:gap-4'>
          <div className='lg:w-1/3'></div>
          <div className='lg:w-2/3'>
            <p className='text-sm text-gray-400'>{kpis[kpi].description}</p>
          </div>
        </div>
      )}

      <FormGroup label='Current Status'>
        <div className='flex'>
          {kpis[kpi].unit !== '' && (
            <div className='text-sm text-gray-400 pt-3 pr-4'>
              {kpis[kpi].unit}
            </div>
          )}
          <TextInput
            className='dark w-full'
            id='currentstatus'
            type='text'
            value={currentStatus}
            onChange={handleCurrentStatusChange}
            required
            theme={{
              field: {
                input: {
                  colors: {
                    gray: 'bg-gray-800 border-gray-500 text-white',
                  },
                },
              },
            }}
          />
        </div>
      </FormGroup>

      <FormGroup label='Target Status'>
        <div className='flex'>
          {kpis[kpi].unit !== '' && (
            <div className='text-sm text-gray-400 pt-3 pr-4'>
              {kpis[kpi].unit}
            </div>
          )}
          <TextInput
            className='dark w-full'
            id='targetstatus'
            type='text'
            value={targetStatus}
            onChange={handleTargetStatusChange}
            required
            theme={{
              field: {
                input: {
                  colors: { gray: 'bg-gray-800 border-gray-500 text-white' },
                },
              },
            }}
          />
        </div>
      </FormGroup>

      <FormGroup label='Deadline'>
        <TextInput
          type='date'
          value={deadline}
          onChange={(e) => {
            setDeadline(e.target.value);
            console.log('Date changed:', e.target.value);
          }}
          className='dark w-full'
          theme={{
            field: {
              input: {
                colors: { gray: 'bg-gray-800 border-gray-500 text-white' },
              },
            },
          }}
          required
        />
      </FormGroup>

      <div className='lg:ml-[33.33%]'>
        <button
          type='submit'
          className='inline-flex items-center py-2 rounded-lg font-semibold tracking-tighter text-white transition duration-200 ease-in-out transform bg-transparent bg-gradient-to-r from-blue-500 to-blue-800 px-28 text-md md:mt-0 focus:shadow-outline ml-2.5 hover:scale-105 focus:scale-100'
        >
          <div className='flex text-lg'>
            <span className='justify-center'>Submit</span>
          </div>
        </button>
      </div>
    </form>
  );
}
