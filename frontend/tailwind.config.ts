const config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6F4E37',
        'primary-light': '#8B6F47',
        'primary-dark': '#4A3728',
        accent: '#D4A574',
        'accent-light': '#E8C5A5',
        dark: '#2C1810',
        light: '#FBF8F3',
        success: '#10B981',
      },
      fontFamily: {
        sans: ['Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

module.exports = config;
