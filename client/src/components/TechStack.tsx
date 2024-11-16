import React from 'react';
import {
  SiNextdotjs,
  SiReact,
  SiPython,
  SiFlask,
  SiGithub,
  SiTypescript,
  SiNodedotjs,
  SiTailwindcss,
  SiVercel,
  SiRender,
} from 'react-icons/si';

export default function TechStack() {
  const technologies = [
    { icon: <SiReact className='w-8 h-8' />, name: 'React' },
    { icon: <SiTailwindcss className='w-8 h-8' />, name: 'Tailwind' },
    { icon: <SiNextdotjs className='w-8 h-8' />, name: 'Next.js' },
    { icon: <SiPython className='w-8 h-8' />, name: 'Python' },
    { icon: <SiFlask className='w-8 h-8' />, name: 'Flask' },
    { icon: <SiTypescript className='w-8 h-8' />, name: 'TypeScript' },
    { icon: <SiNodedotjs className='w-8 h-8' />, name: 'Node.js' },
    { icon: <SiGithub className='w-8 h-8' />, name: 'Github' },
    { icon: <SiVercel className='w-8 h-8' />, name: 'Vercel' },
    { icon: <SiRender className='w-8 h-8' />, name: 'Render' },
  ];

  // Create three sets of icons for seamless infinite scroll
  const scrollingIcons = [...technologies, ...technologies, ...technologies];

  return (
    <div className='relative w-full overflow-hidden py-12'>
      <div className='absolute inset-0 pointer-events-none bg-gradient-to-r from-black via-transparent to-black z-10' />

      <div className='animate-scroll flex'>
        {scrollingIcons.map((item, index) => (
          <div
            key={index}
            className='flex-none inline-flex flex-col items-center justify-center mx-8'
          >
            <div className='w-16 h-16 rounded-xl bg-gray-800 flex items-center justify-center text-white hover:text-blue-400 transition-colors duration-200'>
              {item.icon}
            </div>
            <span className='mt-2 text-sm text-gray-400'>{item.name}</span>
          </div>
        ))}
      </div>

      <style jsx>{`
        .animate-scroll {
          animation: scroll 40s linear infinite;
          width: fit-content;
        }

        @keyframes scroll {
          0% {
            transform: translateX(0);
          }
          100% {
            transform: translateX(calc(-33.33% - 2px));
          }
        }

        .animate-scroll:hover {
          animation-play-state: paused;
        }
      `}</style>
    </div>
  );
}
