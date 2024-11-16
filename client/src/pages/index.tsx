// import Head from 'next/head';
// import Header from '../components/Header';
// import Main from '../components/Main';
// import Footer from '../components/Footer';

// export default function Home() {
//   return (
//     <div className='text-black bg-black'>
//       <Head>
//         <title>nine4</title>
//         <link rel='icon' href='/favicon.png' />
//       </Head>
//       <Header />
//       <Main />
//       <Footer />
//     </div>
//   );
// } hello

import React, { useEffect, useState } from 'react';

export default function Index() {
  const [message, setMessage] = useState('loading');
  const [people, setPeople] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8080/api/home')
      .then((res) => res.json())
      .then((data) => {
        setMessage(data.message);
        setPeople(data.people);
      });
  }, []);

  return (
    <div>
      <div>{message}</div>
      {people.map((person, index) => (
        <div key={index}>{person}</div>
      ))}
    </div>
  );
}
