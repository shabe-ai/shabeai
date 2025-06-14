/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/styles/**/*.css',
    './src/app/globals.css',
  ],
  theme: {
    extend: {
      colors: {
        lemon: {
          DEFAULT: 'var(--clr-lemon)',
        },
        sun: {
          DEFAULT: 'var(--clr-sun)',
        },
        gold: {
          DEFAULT: 'var(--clr-gold)',
        },
        fog: {
          DEFAULT: 'var(--clr-fog)',
        },
        charcoal: {
          DEFAULT: 'var(--clr-charcoal)',
        },
      },
      fontFamily: {
        heading: ['var(--ff-heading)'],
        body:    ['var(--ff-body)'],
      },
      borderRadius: {
        card:   'var(--radius-card)',
        button: 'var(--radius-btn)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}; 