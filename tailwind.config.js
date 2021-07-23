const colors = require("tailwindcss/colors");
module.exports = {
  plugins: [
    // ...
    require('@tailwindcss/forms'),
  ],
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: {
          // blue: "#4a49c9",
          blue: {
            light: "#4a49c9",
            dark : "#66677a",
            accent: "#d7d9f2"
          },
          green: {
            light: "#c7ebdd",
            dark: "#506b60",
          },
          red: {
            accent: "#ffd6c4",
            dark: "#9a7d6f"
          },
          yellow: {
            accent: "#fff9e6",
            dark: "#87700c",
          }
        },
        
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
