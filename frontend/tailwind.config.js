// tailwind.config.js
export default {
    theme: {
      extend: {
        colors: {
          primary: '#0D9488',
          'primary-hover': '#0F766E'
        }
      },
    },
    plugins: [require('@tailwindcss/line-clamp')],
  }