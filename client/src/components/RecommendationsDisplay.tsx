import React from 'react';
import { format, addBusinessDays, parseISO } from 'date-fns';
import { Tooltip } from 'react-tooltip';

interface Subtask {
  TaskID: string;
  TaskName: string;
  StartDate: string;
  Duration: number;
  RiskLevel: 1 | 2 | 3 | 4 | 5;
}

interface Recommendation {
  TaskID: number;
  TaskName: string;
  Description: string;
  RiskLevel: 1 | 2 | 3 | 4 | 5;
  subtasks: Subtask[];
}

type RiskSpectrum = 1 | 2 | 3 | 4 | 5;

interface RiskDotProps {
  risklevel: RiskSpectrum;
}

const riskColors: Record<RiskSpectrum, string> = {
  1: 'bg-blue-500',
  2: 'bg-blue-600',
  3: 'bg-purple-600',
  4: 'bg-pink-600',
  5: 'bg-red-600',
};

const riskLabels: Record<RiskSpectrum, string> = {
  1: 'Very Low Risk',
  2: 'Low Risk',
  3: 'Medium Risk',
  4: 'High Risk',
  5: 'Very High Risk',
};

const RiskDot: React.FC<RiskDotProps> = ({ risklevel }) => {
  return (
    <div className='flex items-center space-x-2'>
      <div className={`w-3 h-3 rounded-full ${riskColors[risklevel]}`} />
      <span
        className={`text-sm ${riskColors[risklevel].replace('bg-', 'text-')}`}
      >
        {riskLabels[risklevel]}
      </span>
    </div>
  );
};

interface RecommendationsDisplayProps {
  recommendations: Recommendation[];
}

const RecommendationsDisplay: React.FC<RecommendationsDisplayProps> = ({
  recommendations,
}) => {
  return (
    <div className='pt-12 pb-8 px-10 mx-auto space-y-6'>
      {recommendations.map((recommendation, index) => (
        <div key={recommendation.TaskID} className='lg:flex lg:gap-6'>
          <React.Fragment key={index}>
            <div className='ktq4 hover:brightness-150 hover:text-gray-300 transition duration-100 flex-1'>
              <div className='flex items-center space-x-4 mb-2'>
                <RiskDot risklevel={recommendation.RiskLevel} />
              </div>
              <h3 className='font-semibold text-lg text-white'>
                {(index + 1).toString()}. {recommendation.TaskName} by{' '}
                {format(
                  addBusinessDays(
                    parseISO(recommendation.subtasks[2].StartDate),
                    recommendation.subtasks[2].Duration - 1
                  ),
                  'MMM d, yyyy'
                )}
              </h3>
              <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
                {recommendation.Description}
              </p>
            </div>
            <div className='lg:w-96 mt-4 lg:mt-0 h-100 flex flex-col space-y-2'>
              {recommendation.subtasks.map((subtask, subindex) => (
                <div
                  key={subindex}
                  className=' bg-gray-900 text-gray-500 h-full rounded-lg p-4 hover:brightness-150 hover:text-gray-300 transition duration-100'
                >
                  <div className='flex justify-between items-center w-full h-full'>
                    <span>{subtask.TaskName}</span>
                    <>
                      <div
                        data-tooltip-id={`risk-${subtask.TaskName}`}
                        className={`w-3 h-3 rounded-full ${
                          riskColors[subtask.RiskLevel as RiskSpectrum]
                        }`}
                      />
                      <Tooltip id={`risk-${subtask.TaskName}`}>
                        <span className='text-sm'>
                          {riskLabels[subtask.RiskLevel]}
                        </span>
                      </Tooltip>
                    </>
                  </div>
                </div>
              ))}
            </div>
          </React.Fragment>
        </div>
      ))}
    </div>
  );
};

export default RecommendationsDisplay;
