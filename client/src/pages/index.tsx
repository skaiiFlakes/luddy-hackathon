import Head from 'next/head';
import Header from '../components/Header';
import Main from '../components/Main';
import Footer from '../components/Footer';
import { registerLicense } from '@syncfusion/ej2-base';

console.log('SUNFPGHSDFFHSH', process.env.NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY);
registerLicense(process.env.NEXT_PUBLIC_SYNCFUSION_LICENSE_KEY || '');

export default function Index() {
  return (
    <div className='text-black bg-black'>
      <Head>
        <title>G4NTT</title>
        <link rel='icon' href='/favicon.png' />
      </Head>
      <Header />
      <Main />
      <Footer />
    </div>
  );
}
