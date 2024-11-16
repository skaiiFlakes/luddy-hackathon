import React, { useState, useEffect } from 'react';
import { Label, Select, TextInput } from 'flowbite-react';
import { kpis } from '../utils/kpiData';

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

export default function Form({
  setIsLoading,
  setError,
  setResponse,
}: {
  setIsLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setResponse: (response: any) => void;
}) {
  const [industry, setIndustry] = useState('Information Technology');
  const [kpi, setKpi] = useState('Gross Sales');
  const [currentStatus, setCurrentStatus] = useState('');
  const [targetStatus, setTargetStatus] = useState('');
  const [deadline, setDeadline] = useState(new Date());

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    const formData = {
      industry,
      kpi,
      currentStatus,
      targetStatus,
      deadline: deadline.toISOString(),
    };

    try {
      const response = await fetch(
        process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/submit',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to submit form');
      }

      const data = await response.json();
      setResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
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

  const handleDeadlineChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDeadline(event.target.valueAsDate!);
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
              {key} {'('}
              {kpis[key].abbr}
              {')'}
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

      <FormGroup label={`Current ${kpis[kpi].abbr}`}>
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

      <FormGroup label={`Target ${kpis[kpi].abbr}`}>
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
          onChange={handleDeadlineChange}
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
          className='inline-flex items-center py-2 rounded-lg font-semibold tracking-tighter text-white transition duration-200 ease-in-out transform bg-transparent bg-gradient-to-r from-blue-500 to-blue-800 px-28 text-md md:mt-0 focus:shadow-outline lg:ml-2.5 hover:scale-105 focus:scale-100'
        >
          <div className='flex text-lg'>
            <span className='justify-center'>Submit</span>
          </div>
        </button>
      </div>
    </form>
  );
}
