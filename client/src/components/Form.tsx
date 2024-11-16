import React, { useState, useEffect } from 'react';
import { Datepicker, Label, Select, TextInput } from 'flowbite-react';
// import { HiMail } from 'react-icons/hi';

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
  const [kpi, setKpi] = useState('');
  const [currentStatus, setCurrentStatus] = useState('');
  const [targetStatus, setTargetStatus] = useState('');
  const [deadline, setDeadline] = useState('');

  // KPI descriptions object
  const kpiDescriptions: { [key: string]: string } = {
    CAC: 'Customer Acquisition Cost - The total cost of acquiring a new customer, including marketing and sales expenses.',
    'Churn Rate':
      'The percentage of customers who stop using your product/service over a given time period.',
    'Average Order Size':
      'The average monetary value of each order placed by customers.',
    MRR: 'Monthly Recurring Revenue - Predictable revenue generated each month from subscriptions.',
    ARR: 'Annual Recurring Revenue - Predictable revenue generated annually from subscriptions.',
    'Cash Runway':
      'The amount of time a company can continue operating with its current cash reserves.',
    'Burn Rate':
      'The rate at which a company spends its cash reserves on operating expenses.',
    'K-factor':
      'The growth rate of a product through viral customer acquisition.',
    'Gross Sales':
      'Total revenue generated before deductions for returns, discounts, and other expenses.',
    MAU: 'Monthly Active Users - The number of unique users who interact with your product in a month.',
    NPS: 'Net Promoter Score - Measures customer satisfaction and likelihood to recommend.',
    'LVT/CAC':
      'Lifetime Value to Customer Acquisition Cost ratio - Measures the return on customer acquisition investment.',
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
          {Object.keys(kpiDescriptions).map((key) => (
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
            <p className='text-sm text-gray-400'>{kpiDescriptions[kpi]}</p>
          </div>
        </div>
      )}

      <FormGroup label='Current Status'>
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
                colors: { gray: 'bg-gray-800 border-gray-500 text-white' },
              },
            },
          }}
        />
      </FormGroup>

      <FormGroup label='Target Status'>
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
      </FormGroup>

      <FormGroup label='Deadline'>
        <Datepicker
          className='dark w-full'
          // onSelectedDateChanged={handleDeadlineChange}
          theme={{
            root: {
              base: 'relative',
            },
            popup: {
              root: {
                base: 'absolute top-10 z-50 block bg-gray-800 border-gray-500 text-white',
              },
            },
            views: {
              days: {
                items: {
                  base: 'grid w-64 grid-cols-7',
                  item: {
                    base: 'block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 hover:bg-gray-700 hover:text-white text-gray-300',
                    selected: 'bg-blue-600 text-white hover:bg-blue-600',
                  },
                },
              },
            },
          }}
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
