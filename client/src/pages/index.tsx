import Head from 'next/head';
import Header from '../components/Header';
import Main from '../components/Main';
import Footer from '../components/Footer';

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
