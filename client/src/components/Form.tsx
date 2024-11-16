import React, { useState, useEffect } from 'react';
import { Datepicker, Label, Select, TextInput } from 'flowbite-react';
import { HiMail } from 'react-icons/hi';

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
    <div className='dark'>
      <form onSubmit={handleSubmit} className='space-y-4'>
        <div className='max-w-md'>
          <div className='mb-2 block'>
            <Label htmlFor='industries' value='Industry:' />
          </div>
          <Select
            id='industries'
            required
            value={industry}
            onChange={handleIndustryChange}
            theme={{
              field: {
                input: {
                  colors: { gray: 'bg-gray-800 border-gray-500 text-white' },
                },
              },
            }}
          >
            <option value='Technology'>Technology</option>
            <option value='Finance'>Finance</option>
            <option value='Healthcare'>Healthcare</option>
            <option value='Retail'>Retail</option>
            <option value='Education'>Education</option>
            <option value='Manufacturing'>Manufacturing</option>
            <option value='Hospitality'>Hospitality</option>
            <option value='Transportation'>Transportation</option>
            <option value='Media'>Media</option>
            <option value='Telecommunications'>Telecommunications</option>
          </Select>
        </div>

        <div className='max-w-md'>
          <div className='mb-2 block'>
            <Label htmlFor='kpis' value='KPI:' />
          </div>
          <Select
            id='kpis'
            required
            value={kpi}
            onChange={handleKpiChange}
            theme={{
              field: {
                input: {
                  colors: { gray: 'bg-gray-800 border-gray-500 text-white' },
                },
              },
            }}
          >
            <option value='CAC'>CAC</option>
            <option value='Churn Rate'>Churn Rate</option>
            <option value='Average Order Size'>Average Order Size</option>
            <option value='MRR'>MRR</option>
            <option value='ARR'>ARR</option>
            <option value='Cash Runway'>Cash Runway</option>
            <option value='Burn Rate'>Burn Rate</option>
            <option value='K-factor'>K-factor</option>
            <option value='Gross Sales'>Gross Sales</option>
            <option value='MAU'>MAU</option>
            <option value='NPS'>NPS</option>
            <option value='LVT/CAC'>LVT/CAC</option>
          </Select>
          {kpi && (
            <p className='mt-2 text-sm text-gray-400'>{kpiDescriptions[kpi]}</p>
          )}
        </div>

        <div className='max-w-md'>
          <div className='mb-2 block'>
            <Label htmlFor='currentstatus' value='Current Status:' />
          </div>
          <TextInput
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
        </div>

        <div className='max-w-md'>
          <div className='mb-2 block'>
            <Label htmlFor='targetstatus' value='Target Status:' />
          </div>
          <TextInput
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

        <div>
          <div className='mb-2 block'>
            <Label htmlFor='deadline' value='Deadline:' />
          </div>
          <div className='relative max-w-sm'>
            <Datepicker
              onSelectedDateChanged={handleDeadlineChange}
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
          </div>
        </div>

        <button
          type='submit'
          className='inline-flex items-center py-3 font-semibold tracking-tighter text-white transition duration-500 ease-in-out transform bg-transparent bg-gradient-to-r from-blue-500 to-blue-800 px-14 text-md md:mt-0 focus:shadow-outline'
        >
          <div className='flex text-lg'>
            <span className='justify-center'>Submit</span>
          </div>
        </button>
      </form>
    </div>
  );
}
