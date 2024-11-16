import Form from './Form';
import Link from 'next/link';
import React, { useEffect, useState } from 'react';
import Gantt from './Gantt';
import GanttSkeleton from './GanttSkeleton';
import { Target, Clock, TrendingUp, LineChart } from 'lucide-react';
import TechStack from './TechStack';

// import { sampleGanttData } from '../sampleGanttData';

export default function Main() {
  interface ResponseData {
    outputs: {
      recommendations: any[];
    };
  }

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<ResponseData>({
    outputs: { recommendations: [] },
  });

  return (
    <section className='text-gray-600 body-font'>
      <div className='max-w-5xl pt-56 pb-16 mx-auto'>
        <h1 className='text-80 text-center font-4 lh-6 ld-04 font-bold text-white mb-6'>
          Turn Your KPIs into Actionable Plans
        </h1>
        <h2 className='text-2xl font-4 font-semibold lh-6 ld-04 pb-11 text-gray-700 text-center'>
          Input your KPI, industry, and deadline. Let us analyze the data
          <br /> and deliver a tailored Gantt chart of tasks to drive your
          success.
        </h2>
      </div>
      <div className='container pt-12 pb-36 max-w-4xl mx-auto justify-center items-center'>
        <div className='ktq4'>
          <Form
            setError={setError}
            setIsLoading={setIsLoading}
            setResponse={setResponse}
          />
        </div>
      </div>

      {Object.keys(response).length !== 0 &&
        response.outputs.recommendations.length > 0 && (
          <Gantt data={response.outputs.recommendations} />
        )}
      {isLoading && Object.keys(response).length !== 0 && <GanttSkeleton />}

      {Object.keys(response).length !== 0 &&
        response.outputs.recommendations.length > 0 && (
          <div className='pt-12 pb-8 px-10 mx-auto fsac4'>
            {response.outputs.recommendations.map((recommendation, index) => (
              <React.Fragment key={index}>
                <div
                  id={`task-${index * 4 + 1}`}
                  className='ktq4 hover:brightness-150 hover:text-gray-300 transition duration-100'
                >
                  <h3 className='font-semibold text-lg text-white'>
                    {(index + 1).toString()}. {recommendation.TaskName}
                  </h3>
                  <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
                    {recommendation.Description}
                  </p>
                </div>
                <div className='flex flex-col space-y-2'>
                  {recommendation.subtasks.map(
                    (subtask: any, subindex: any) => (
                      <div
                        key={subindex}
                        className='bg-gray-900 text-gray-500 rounded-lg p-4 hover:brightness-150 hover:text-gray-300 transition duration-100'
                      >
                        {subtask.TaskName}
                      </div>
                    )
                  )}
                </div>
              </React.Fragment>
            ))}
          </div>
        )}
      <TechStack />

      <h2 className='pt-40 mb-1 text-2xl font-semibold tracking-tighter text-center text-gray-200 lg:text-7xl md:text-6xl'>
        Planning made simple.
      </h2>
      <br></br>
      <p className='mx-auto text-xl text-center text-gray-300 font-normal leading-relaxed fs521 lg:w-2/3'>
        Our intelligent platform helps you break down complex KPI targets into
        manageable, <br />
        time-bound action items with clear tasks and measurable outcomes.
      </p>
      <div className='pt-12 pb-24 max-w-4xl mx-auto fsac4 md:px-1 px-3'>
        <div className='ktq4'>
          <Target className='w-10 h-10 text-blue-500 text-gradient-to-r from-blue-300 to-blue-800' />
          <h3 className='pt-3 font-semibold text-lg text-white'>
            Smart Goal Setting
          </h3>
          <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
            Transform high-level KPIs into specific, measurable objectives with
            our AI-powered goal breakdown system. Get clear metrics and
            milestones for every stage of your journey.
          </p>
        </div>
        <div className='ktq4'>
          <Clock className='w-10 h-10 text-blue-500 text-gradient-to-r from-blue-300 to-blue-800' />
          <h3 className='pt-3 font-semibold text-lg text-white'>
            Timeline Optimization
          </h3>
          <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
            Our intelligent scheduling algorithm creates realistic timelines
            based on your industry benchmarks and resource constraints. Stay on
            track with automated progress tracking and adjustments.
          </p>
        </div>
        <div className='ktq4'>
          <TrendingUp className='w-10 h-10 text-blue-500 text-gradient-to-r from-blue-300 to-blue-800' />
          <h3 className='pt-3 font-semibold text-lg text-white'>
            Finance-Driven Insights
          </h3>
          <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
            Enhance your KPI planning with stock insights. Our platform analyzes
            market conditions, cost structures, and revenue patterns to provide
            contextual recommendations that align with your financial goals.
          </p>
        </div>
        <div className='ktq4'>
          <LineChart className='w-10 h-10 text-blue-500 text-gradient-to-r from-blue-300 to-blue-800' />
          <h3 className='pt-3 font-semibold text-lg text-white'>
            Market Sentiment Analytics
          </h3>
          <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
            Stay ahead with real-time market sentiment analysis. Our AI
            processes customer feedback, social media trends, and industry
            signals to help you adjust your KPI strategies based on market
            dynamics.
          </p>
        </div>
      </div>
      {/*
      <div className='pt-32 pb-32 max-w-6xl mx-auto fsac4 md:px-1 px-3'>
        <div className='ktq4'>
          <img src='/api/placeholder/400/300' alt='Sales KPI Template'></img>
          <h3 className='pt-3 font-semibold text-lg text-white'>
            Sales Performance KPI Template
          </h3>
          <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
            Accelerate your sales team's performance with our comprehensive KPI
            template. Includes proven strategies for pipeline management,
            conversion rate optimization, and revenue growth. Perfect for B2B
            and B2C sales teams looking to exceed their targets.
          </p>
        </div>
        <div className='ktq4'>
          <img
            src='/api/placeholder/400/300'
            alt='Customer Success Template'
          ></img>
          <h3 className='pt-3 font-semibold text-lg text-white'>
            Customer Success Metrics Template
          </h3>
          <p className='pt-2 value-text text-md text-gray-200 fkrr1'>
            Drive customer satisfaction and retention with our customer success
            KPI template. Features detailed action plans for improving NPS,
            reducing churn, and increasing customer lifetime value. Built on
            best practices from leading SaaS companies.
          </p>
        </div>
      </div> */}
      <section className='relative pb-24'>
        <div className='max-w-6xl mx-auto px-4 sm:px-6 text-center'>
          <div className='py-24 md:py-36'>
            <h1 className='mb-5 text-6xl font-bold text-white'>
              Subscribe to our newsletter
            </h1>
            <h1 className='mb-9 text-2xl font-semibold text-gray-200'>
              Get expert KPI insights and planning tips delivered to your inbox.
            </h1>
            <input
              type='email'
              placeholder='g4ntt@iu.edu'
              name='email'
              className='border border-gray-600 w-1/4 pr-2 pl-2 py-3 mt-2 rounded-md text-gray-800 font-semibold hover:border-gray-700 bg-black'
            />
            <Link
              className='inline-flex items-center px-14 py-3 mt-2 ml-2 font-medium text-black transition duration-500 ease-in-out transform bg-transparent border rounded-lg bg-white'
              href='/subscribe'
            >
              <span className='justify-center'>Subscribe</span>
            </Link>
          </div>
        </div>
      </section>
    </section>
  );
}
