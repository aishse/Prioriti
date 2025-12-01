/**
 * Tailwind config for Prioriti
 * - scans templates and static source files for classes
 * - adds a couple of custom colors and font family
 */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/src/**/*.{html,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        dm: ["'DM Serif Display'", 'serif']
      }
    }
  },
 
  plugins: []
}
