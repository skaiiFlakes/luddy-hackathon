import Head from 'next/head';
import Header from '../components/Header';
import Main from '../components/Main';
import Footer from '../components/Footer';
import { registerLicense } from '@syncfusion/ej2-base';

registerLicense(process.env.NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY || '');

export default function Index() {
  return (
    <div className='text-black bg-black'>
      <Head>
        <title>G4NTT</title>
        <link rel='icon' href='/favicon.png' />
      </Head>
      <Header />
      <div className='relative w-full h-[500px] bg-gradient-to-r from-blue-300 via-blue-500 to-blue-800'>
        <div className='fade-out'></div>
        <div className='relative z-10'>
          <Main />
          <Footer />
        </div>
        <style jsx>{`
          .fade-out {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
              to bottom,
              rgba(0, 0, 0, 0.2) 0%,
              rgba(0, 0, 0, 1) 20%,
              rgba(0, 0, 0, 1) 100%
            );
          }
        `}</style>
      </div>
    </div>
  );
}
