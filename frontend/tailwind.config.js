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
        lemon:   'var(--clr-lemon)',
        sun:     'var(--clr-sun)',
        gold:    'var(--clr-gold)',
        fog:     'var(--clr-fog)',
        charcoal:'var(--clr-charcoal)',
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
  plugins: [],
}; 