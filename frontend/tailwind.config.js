/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        finn: {
          dark: "#0B0F17",
          card: "#121826",
          cardHover: "#182235",
          border: "#1F293D",
          accent: "#2563EB",
          accentLight: "#3B82F6",
          emerald: "#10B981",
          rose: "#F43F5E",
          amber: "#F59E0B",
          subtext: "#94A3B8"
        }
      }
    },
  },
  plugins: [],
}
