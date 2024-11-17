import React, { useState, useEffect } from 'react';
import { Spinner } from 'flowbite-react';

function GanttSkeleton() {
  const loadingMessages = [
    'Sending data to server...',
    'Parsing stock financials...',
    'Running market analysis...',
    'Classifying data...',
    'Generating strategies...',
    'Optimizing recommendations...',
    'Building timeline...',
  ];

  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMessageIndex(
        (prevIndex) => (prevIndex + 1) % loadingMessages.length
      );
    }, 5000); // Change message every 2 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      id='gantt-skeleton'
      className='w-full h-[500px] ktq4 rounded-lg p-8 mt-5'
    >
      <div className='h-full flex flex-col items-center justify-center gap-4'>
        <Spinner
          aria-label='Loading spinner'
          size='xl'
          className='w-12 h-12 fill-blue-500 text-gray-900 '
        />
        <div className='text-xl font-4 text-gray-200 min-h-[28px] text-center'>
          {loadingMessages[currentMessageIndex]}
        </div>
      </div>
    </div>
  );
}

export default GanttSkeleton;
