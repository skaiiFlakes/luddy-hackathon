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
  isLoading,
  setIsLoading,
  setError,
  setResponse,
}: {
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setResponse: (response: any) => void;
}) {
  const [industry, setIndustry] = useState('Information Technology');
  const [kpi, setKpi] = useState('Gross Sales');
  const [currentStatus, setCurrentStatus] = useState('');
  const [targetStatus, setTargetStatus] = useState('');
  const [deadline, setDeadline] = useState(new Date());

  const waitForElement = (
    selector: string,
    timeout = 5000
  ): Promise<HTMLElement | null> => {
    const startTime = Date.now();
    return new Promise((resolve) => {
      const checkElement = () => {
        const element = document.querySelector(selector);
        if (element) {
          resolve(element as HTMLElement);
          return;
        }
        if (Date.now() - startTime > timeout) {
          resolve(null);
          return;
        }
        setTimeout(checkElement, 100);
      };
      checkElement();
    });
  };

  const scrollToGantt = async () => {
    await new Promise((resolve) => setTimeout(resolve, 500));
    const element = await waitForElement('#gantt-skeleton');
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setResponse({ recommendations: [] });
    setIsLoading(true);
    setError(null);

    await scrollToGantt();

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
      setIsLoading(false);
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

  const minDate = new Date();
  const maxDate = new Date();
  maxDate.setFullYear(maxDate.getFullYear() + 5);

  return (
    <form onSubmit={handleSubmit} className='space-y-4 '>
      <FormGroup label='Industry'>
        <Select
          className='dark'
          id='industries'
          required
          value={industry}
          onChange={handleIndustryChange}
          style={{ backgroundColor: '#242424' }}
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
          style={{ backgroundColor: '#242424' }}
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
            type='number'
            step='any'
            value={currentStatus}
            onChange={handleCurrentStatusChange}
            required
            onKeyDown={(e) => {
              if (
                (e.key !== 'Backspace' &&
                  e.key !== 'Delete' &&
                  e.key !== 'ArrowLeft' &&
                  e.key !== 'ArrowRight' &&
                  !/^[0-9.]$/.test(e.key)) ||
                (e.key === '.' && currentStatus.includes('.'))
              )
                e.preventDefault();
            }}
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
            type='number'
            step='any'
            value={targetStatus}
            onChange={handleTargetStatusChange}
            required
            onKeyDown={(e) => {
              if (
                (e.key !== 'Backspace' &&
                  e.key !== 'Delete' &&
                  e.key !== 'ArrowLeft' &&
                  e.key !== 'ArrowRight' &&
                  !/^[0-9.]$/.test(e.key)) ||
                (e.key === '.' && targetStatus.includes('.'))
              )
                e.preventDefault();
            }}
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
          min={minDate.toISOString().split('T')[0]}
          max={maxDate.toISOString().split('T')[0]}
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
        {/* <div className='flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4'> */}
        <button
          type='submit'
          disabled={isLoading}
          className={`inline-flex items-center justify-center py-2 rounded-lg font-semibold tracking-tighter text-white ease-in-out transform bg-transparent bg-gradient-to-r from-blue-600 to-blue-800 px-10 text-md md:mt-0 focus:shadow-outline lg:ml-2.5 active:scale-95 focus:scale-100 transition duration-300 ${
            isLoading
              ? 'brightness-50'
              : 'hover:brightness-150 focus:brightness-100'
          }`}
          style={{ width: '100%' }}
        >
          <div className='flex justify-center items-center text-lg'>
            <span>Generate G4NTT</span>
          </div>
        </button>
        {/* <button
            disabled={isLoading}
            className={`inline-flex items-center justify-center py-2 rounded-lg font-semibold tracking-tighter text-white ease-in-out transform bg-transparent bg-gradient-to-r from-pink-600 to-purple-700 px-10 text-md md:mt-0 focus:shadow-outline lg:ml-2.5 active:scale-95 focus:scale-100 transition duration-300 ${
              isLoading
                ? 'brightness-50'
                : 'hover:brightness-150 focus:brightness-100'
            }`}
            style={{ width: '100%' }}
          >
            <div className='flex justify-center items-center text-lg'>
              <span>Run Risk Analysis</span>
            </div>
          </button>
        </div> */}
      </div>
    </form>
  );
}
