/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
const color = require('tailwindcss/colors')
module.exports = {
  content: ['./templates/**/*.html', './node_modules/flowbite/**/*.js'],
  theme: {
    colors: {
      'bq': { 100: '#000000' },
      primary:'#cca876',
      gray: {
        "100": "#132335",
        "200": "#132334",
        "300": "#0f1c2a",
        "400": "#0d0c12",
        "500": "rgba(255, 255, 255, 0.5)",
      }, gray1: {
        "100": "#828282",
        "200": "#241520",
        "300": "#160813",
        "400": "rgba(0, 0, 0, 0.24)",
      },
      'bg':'#0d0c12',
      'bg2':'#132335',
      'headerber':'#0f1c2a',
      burlywood: {
        "100": "#cca876","300": "#F1C990DE",
        "200": "rgba(204, 168, 118, 0.2)",
      },maincolor: "#ba7894",
      slategray: "#222E3B",
      'slategray2': "#253341",
      palevioletred: {
        "100": "#a15e7a",
        "200": "rgba(161, 94, 122, 0.09)",
      },
      gainsboro: "#e3e3e3",
      white: "#fff",
      darkslategray: "#25374A98",
      peru: "#997542",
      darkgray: "#999",
      
      secondary: "#ecbfd3",
      aliceblue: {
        "100": "rgba(235, 243, 245, 0.5)",
        "200": "rgba(235, 243, 245, 0.22)",
      },

    
    },
    extend: {

colors:{
  primary:'#cca876',

},
      spacing: {},

      screens: {
        mq1875: {
          raw: "screen and (max-width: 1875px)",
        },
        mq1425: {
          raw: "screen and (max-width: 1425px)",
        },
        mq1400: {
          raw: "screen and (max-width: 1400px)",
        },
        lg: {
          max: "1200px",
        },
        mq925: {
          raw: "screen and (max-width: 925px)",
        },
        mq825: {
          raw: "screen and (max-width: 825px)",
        },
        mq765: {
          raw: "screen and (max-width: 765px)",
        },
        mq450: {
          raw: "screen and (max-width: 450px)",
        },
        mq449: {
          raw: "screen and (max-width: 449px)",
        }, mq380: {
          raw: "screen and (max-width: 380px)",
        },
      },
      fontFamily: {
        montserrat: "Montserrat",
        poppins: "Poppins",
        inter: "Inter",
          'body': [
        'Inter', 
        'ui-sans-serif', 
        'system-ui', 
        '-apple-system', 
        'system-ui', 
        'Segoe UI', 
        'Roboto', 
        'Helvetica Neue', 
        'Arial', 
        'Noto Sans', 
        'sans-serif', 
        'Apple Color Emoji', 
        'Segoe UI Emoji', 
        'Segoe UI Symbol', 
        'Noto Color Emoji'
      ],
          'sans': [
        'Inter', 
        'ui-sans-serif', 
        'system-ui', 
        '-apple-system', 
        'system-ui', 
        'Segoe UI', 
        'Roboto', 
        'Helvetica Neue', 
        'Arial', 
        'Noto Sans', 
        'sans-serif', 
        'Apple Color Emoji', 
        'Segoe UI Emoji', 
        'Segoe UI Symbol', 
        'Noto Color Emoji'
      ]
      },
      borderRadius: {
        "31xl": "50px",
        "8xs": "5px",
        "3xs": "10px",
        xl: "20px",
      }, fontSize: {
        base: "16px",
        "7xl": "26px",
        "2xl": "21px",
        xl: "20px",
        sm: "14px",
        smi: "13px",
        "16xl": "35px",
        "9xl": "28px",
        lg: "18px",
        mini: "15px",
        "3xl": "22px",
        "31xl": "50px",
        "11xl": "30px",
        "21xl": "40px",
        inherit: "inherit",
      },
    },
  },

  plugins: [
    require('flowbite/plugin')
    , require('preline/plugin'),
  ]
}

