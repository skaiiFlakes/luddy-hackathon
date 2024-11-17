import Form from './Form';
import Link from 'next/link';
import React, { useEffect, useState } from 'react';
import Gantt from './Gantt';
import GanttSkeleton from './GanttSkeleton';
import { Target, Clock, TrendingUp, LineChart } from 'lucide-react';
import TechStack from './TechStack';
import { format, addDays, parseISO, addBusinessDays } from 'date-fns';

// import { sampleGanttData } from '../sampleGanttData';

export default function Main() {
  interface ResponseData {
    recommendations: any[];
  }

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<ResponseData>({
    recommendations: [],
  });
  // const [response, setResponse] = useState<ResponseData>({
  //   recommendations: [
  //     {
  //       TaskID: 1,
  //       TaskName:
  //         'Implement AI-driven marketing strategies to optimize Gross Sales from 5,000,000 to 5,000,000',
  //       Description:
  //         'The positive sentiment in financial news, especially from companies like Insider Monkey and Motley Fool, indicates market receptivity to advanced technologies. Leveraging AI for marketing can improve customer targeting and increase sales. This objective aligns with the dynamic trends in the Information Technology industry towards innovative solutions.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Conduct a market analysis to identify AI implementation opportunities',
  //           StartDate: '2024-11-18',
  //           Duration: 15,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Collaborate with AI experts to develop personalized marketing algorithms',
  //           StartDate: '2024-12-03',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Launch AI-powered marketing campaigns targeting high-potential customer segments',
  //           StartDate: '2025-01-02',
  //           Duration: 45,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 2,
  //       TaskName:
  //         'Enhance customer engagement strategies to maintain Gross Sales at 5,000,000',
  //       Description:
  //         'The negative sentiment in general news indicates a potential risk of customer disengagement. Developing proactive engagement strategies can retain existing customers and drive repeat sales. This objective leverages the industry financial context to ensure sustained performance in the Information Technology sector.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Implement a customer feedback system to gather insights for engagement improvements',
  //           StartDate: '2024-11-18',
  //           Duration: 20,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Train customer service teams on personalized engagement tactics',
  //           StartDate: '2024-12-08',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Launch a loyalty program to incentivize repeat purchases',
  //           StartDate: '2025-01-07',
  //           Duration: 45,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 3,
  //       TaskName:
  //         'Expand market reach to increase Gross Sales from 5,000,000 to 5,000,000',
  //       Description:
  //         'The positive sentiment in financial news presents an opportunity to capitalize on market optimism. Expanding market reach can tap into new customer segments and drive additional sales. This objective aligns with the growth potential highlighted in the industry financial context for Information Technology.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Conduct a market segmentation analysis to identify untapped markets',
  //           StartDate: '2024-11-20',
  //           Duration: 25,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Develop partnerships with complementary businesses to access new customer pools',
  //           StartDate: '2024-12-15',
  //           Duration: 40,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Launch targeted marketing campaigns in newly identified market segments',
  //           StartDate: '2025-01-24',
  //           Duration: 35,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 4,
  //       TaskName:
  //         'Optimize pricing strategies to improve Gross Sales from 5,000,000 to 5,000,000',
  //       Description:
  //         'The negative sentiment in general news may indicate price sensitivity among potential customers. Optimizing pricing strategies can attract cost-conscious buyers and drive sales volume. This objective leverages the financial news sentiment to adapt pricing in the competitive landscape of the Information Technology industry.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Conduct a pricing analysis to assess competitive pricing structures',
  //           StartDate: '2024-11-22',
  //           Duration: 20,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Implement dynamic pricing models to adjust prices based on market demand',
  //           StartDate: '2024-12-12',
  //           Duration: 35,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Monitor competitor pricing strategies and adapt pricing accordingly',
  //           StartDate: '2025-01-16',
  //           Duration: 30,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 5,
  //       TaskName:
  //         'Strengthen distribution channels to sustain Gross Sales at 5,000,000',
  //       Description:
  //         'The positive sentiment in financial news towards specific tickers and publishers suggests receptiveness to technology-related products. Strengthening distribution channels can ensure product availability to meet market demand. This objective capitalizes on industry trends in the Information Technology sector to enhance product accessibility.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Evaluate current distribution network performance and identify bottlenecks',
  //           StartDate: '2024-11-25',
  //           Duration: 15,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Diversify distribution channels to reach a broader customer base',
  //           StartDate: '2024-12-10',
  //           Duration: 25,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Implement a logistics tracking system to improve delivery efficiency',
  //           StartDate: '2025-01-04',
  //           Duration: 35,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 6,
  //       TaskName:
  //         'Enhance product personalization to drive Gross Sales from 5,000,000 to 5,000,000',
  //       Description:
  //         "The positive sentiment in financial news towards personalized services emphasizes the importance of tailored customer experiences. Enhancing product personalization can boost customer loyalty and drive repeat purchases. This objective aligns with the industry's move towards customized solutions in the Information Technology sector.",
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Conduct a customer segmentation analysis to identify personalized product opportunities',
  //           StartDate: '2024-11-28',
  //           Duration: 20,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Implement AI algorithms for product recommendations based on customer preferences',
  //           StartDate: '2024-12-18',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Launch personalized marketing campaigns highlighting customized product offerings',
  //           StartDate: '2025-01-17',
  //           Duration: 40,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 7,
  //       TaskName:
  //         'Improve customer service processes to ensure Gross Sales at 5,000,000',
  //       Description:
  //         'The negative sentiment in general news highlights the importance of quality customer service. Improving customer service processes can enhance customer satisfaction and drive positive word-of-mouth referrals. This objective leverages the financial news sentiment to address customer experience in the competitive Information Technology industry.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Conduct a customer service audit to identify pain points and areas for improvement',
  //           StartDate: '2024-12-02',
  //           Duration: 25,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Implement a training program for customer service representatives on effective communication skills',
  //           StartDate: '2024-12-27',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Integrate AI chatbots to streamline customer query resolution processes',
  //           StartDate: '2025-01-26',
  //           Duration: 35,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 8,
  //       TaskName:
  //         'Utilize social media channels to increase brand visibility and drive Gross Sales from 5,000,000 to 5,000,000',
  //       Description:
  //         "The positive sentiment in financial news towards specific publishers like Insider Monkey and Motley Fool presents an opportunity for brand exposure. Leveraging social media channels can boost brand visibility and attract new customers. This objective aligns with the industry's social media engagement trends in the Information Technology sector.",
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Audit current social media presence and identify areas for enhancement',
  //           StartDate: '2024-12-05',
  //           Duration: 20,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Develop a social media content calendar with engaging posts and promotions',
  //           StartDate: '2024-12-25',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Collaborate with social media influencers to reach a wider audience',
  //           StartDate: '2025-01-24',
  //           Duration: 35,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 9,
  //       TaskName:
  //         'Implement customer feedback analysis tools to enhance product offerings and maintain Gross Sales at 5,000,000',
  //       Description:
  //         "The positive sentiment in financial news towards personalized products underscores the value of customer feedback. Implementing feedback analysis tools can provide actionable insights for product improvements and innovation. This objective aligns with the industry's focus on customer-centric solutions in the Information Technology sector.",
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Select and onboard a customer feedback analysis platform',
  //           StartDate: '2024-12-09',
  //           Duration: 25,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Analyze customer feedback data to identify key improvement areas',
  //           StartDate: '2025-01-03',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Implement product updates based on customer feedback insights',
  //           StartDate: '2025-02-02',
  //           Duration: 35,
  //         },
  //       ],
  //     },
  //     {
  //       TaskID: 10,
  //       TaskName:
  //         'Optimize website user experience to drive online sales and achieve Gross Sales of 5,000,000',
  //       Description:
  //         'The positive sentiment in financial news towards innovative solutions indicates the importance of a seamless online experience. Optimizing website user experience can attract and retain online customers, driving incremental sales. This objective leverages the industry trend of digital transformation in the Information Technology sector.',
  //       subtasks: [
  //         {
  //           TaskID: 'A',
  //           TaskName:
  //             'Conduct a website UX audit to identify usability gaps and bottlenecks',
  //           StartDate: '2024-12-12',
  //           Duration: 20,
  //         },
  //         {
  //           TaskID: 'B',
  //           TaskName:
  //             'Implement UX improvements based on audit findings to enhance site navigation',
  //           StartDate: '2025-01-01',
  //           Duration: 30,
  //         },
  //         {
  //           TaskID: 'C',
  //           TaskName:
  //             'Perform A/B testing for new UX features to optimize conversion rates',
  //           StartDate: '2025-01-31',
  //           Duration: 35,
  //         },
  //       ],
  //     },
  //   ],
  // });

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
            isLoading={isLoading}
            setError={setError}
            setIsLoading={setIsLoading}
            setResponse={setResponse}
          />
        </div>
      </div>

      {isLoading && response.recommendations.length === 0 && <GanttSkeleton />}

      {Array.isArray(response.recommendations) &&
        response.recommendations.length > 0 && (
          <div>
            <Gantt data={response.recommendations} />

            <div className='pt-12 pb-8 px-10 mx-auto fsac4'>
              {response.recommendations.map((recommendation, index) => (
                <React.Fragment key={index}>
                  <div
                    id={`task-${index + 1}`}
                    className='ktq4 hover:shadow-[0_10px_10px_1px_0.3] hover:shadow-pink-600 hover:brightness-150 hover:text-gray-300 transition duration-100'
                  >
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
