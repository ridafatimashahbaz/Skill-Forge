export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#161A24",
        paper: "#F6F5F1",
        forge: {
          DEFAULT: "#2F6F5E",
          light: "#E4F0EC",
          dark: "#1E4A3E",
        },
        ember: "#C7622A",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
      },
    },
  },
  plugins: [],
}
