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

const riskGlowColors: Record<RiskSpectrum, string> = {
  1: 'hover:shadow-[0_0_15px_rgba(59,130,246,0.5)]',
  2: 'hover:shadow-[0_0_15px_rgba(37,99,235,0.5)]',
  3: 'hover:shadow-[0_0_15px_rgba(147,51,234,0.5)]',
  4: 'hover:shadow-[0_0_15px_rgba(219,39,119,0.5)]',
  5: 'hover:shadow-[0_0_15px_rgba(220,38,38,0.5)]',
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
    <>
      <div
        data-tooltip-id={`risk-${risklevel}`}
        className={`w-3 h-3 rounded-full ${riskColors[risklevel]}`}
      />
      <Tooltip id={`risk-${risklevel}`}>
        <span className='text-sm'>{riskLabels[risklevel]}</span>
      </Tooltip>
    </>
  );
};

interface RecommendationsDisplayProps {
  recommendations: Recommendation[];
}

const RecommendationsDisplay: React.FC<RecommendationsDisplayProps> = ({
  recommendations,
}) => {
  return (
    <div className='space-y-6'>
      {recommendations.map((recommendation, index) => (
        <div key={recommendation.TaskID} className='lg:flex lg:gap-6'>
          <div
            className={`flex-1 p-6 rounded-lg border transition-shadow ${
              riskGlowColors[recommendation.RiskLevel]
            }`}
          >
            <div className='flex items-center gap-3 mb-4'>
              <RiskDot risklevel={recommendation.RiskLevel} />
              <h3 className='font-semibold text-lg'>
                {(index + 1).toString()}. {recommendation.TaskName} by{' '}
                {format(
                  addBusinessDays(
                    parseISO(recommendation.subtasks[2].StartDate),
                    recommendation.subtasks[2].Duration - 1
                  ),
                  'MMM d, yyyy'
                )}
              </h3>
            </div>
            <p className='text-gray-600'>{recommendation.Description}</p>
          </div>
          <div className='lg:w-96 mt-4 lg:mt-0 h-full'>
            <div
              className={`h-full p-6 rounded-lg border transition-shadow ${
                riskGlowColors[recommendation.RiskLevel]
              }`}
            >
              <h4 className='font-semibold mb-4'>Subtasks</h4>
              <div className='space-y-3'>
                {recommendation.subtasks.map((subtask, subindex) => (
                  <div
                    key={subtask.TaskID}
                    className='flex items-center gap-3 p-3 rounded-md bg-gray-50'
                  >
                    <RiskDot risklevel={subtask.RiskLevel} />
                    <span>{subtask.TaskName}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RecommendationsDisplay;
