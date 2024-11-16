import type { Config } from 'tailwindcss';
import flowbite from 'flowbite-react/tailwind';

export default {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/flowbite/**/*.js',
    flowbite.content(),
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          100: '#FBFBFB',
          200: '#c2c7ca',
          300: '#b8bcbf',
          400: '#999999',
          500: '#7F7F7F',
          600: '#666666',
          700: '#4C4C4C',
          800: '#121212',
          900: '#191919',
        },
      },
    },
  },

  plugins: [flowbite.plugin()],
} satisfies Config;
