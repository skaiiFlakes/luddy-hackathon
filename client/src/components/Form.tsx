import React, { useState } from 'react';

export default function Form() {
  const [industry, setIndustry] = useState('');
  const [kpi, setKpi] = useState('');
  const [currentStatus, setCurrentStatus] = useState('');
  const [targetStatus, setTargetStatus] = useState('');
  const [deadline, setDeadline] = useState('');

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
    setDeadline(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Handle form submission logic here
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Industry:
          <select value={industry} onChange={handleIndustryChange}>
            <option value=''>Select an industry</option>
            <option value='Industry 1'>Industry 1</option>
            <option value='Industry 2'>Industry 2</option>
            {/* Add more options as needed */}
          </select>
        </label>
        <br />
        <label>
          KPI:
          <select value={kpi} onChange={handleKpiChange}>
            <option value=''>Select a KPI</option>
            <option value='CAC'>CAC</option>
            <option value='Churn Rate'>Churn Rate</option>
            <option value='Average Order Size'>Average Order Size</option>
            {/* Add more options as needed */}
          </select>
        </label>
        <br />
        <label>
          Current Status:
          <input
            type='text'
            value={currentStatus}
            onChange={handleCurrentStatusChange}
          />
        </label>
        <br />
        <label>
          Target Status:
          <input
            type='text'
            value={targetStatus}
            onChange={handleTargetStatusChange}
          />
        </label>
        <br />
        <label>
          Deadline/Target Date:
          <input type='text' value={deadline} onChange={handleDeadlineChange} />
        </label>
        <br />
        <button type='submit'>Submit</button>
      </form>
    </div>
  );
}
