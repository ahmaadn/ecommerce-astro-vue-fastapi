import animate from 'tailwindcss-animate'
const defaultTheme = require('tailwindcss/defaultTheme')
const daisyuiColorObj = require('daisyui/src/theming/index')

/** @type {import('tailwindcss').Config} */
export default {
    darkMode: ['class'],
    safelist: ['dark'],
    prefix: '',
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        container: {
            center: true,
            padding: '2rem',
            screens: {
                '2xl': '1400px',
            },
        },
        extend: {
            // fontFamily: {
            //     sans: ['Inter', ...defaultTheme.fontFamily.sans],
            // },
            colors: {
                border: daisyuiColorObj['base-content'],
                input: daisyuiColorObj['base-content'],
                ring: daisyuiColorObj['base-content'],
                background: daisyuiColorObj['base-100'],
                foreground: daisyuiColorObj['base-content'],
                primary: {
                    DEFAULT: daisyuiColorObj['primary'],
                    foreground: daisyuiColorObj['primary-content'],
                },
                secondary: {
                    DEFAULT: daisyuiColorObj['secondary'],
                    foreground: daisyuiColorObj['secondary-content'],
                },
                destructive: {
                    DEFAULT: daisyuiColorObj['error'],
                    foreground: daisyuiColorObj['error-content'],
                },
                muted: {
                    DEFAULT: daisyuiColorObj['base-300'],
                    foreground: daisyuiColorObj['base-content'],
                },
                accent: {
                    DEFAULT: daisyuiColorObj['accent'],
                    foreground: daisyuiColorObj['accent-content'],
                },
                popover: {
                    DEFAULT: daisyuiColorObj['base-100'],
                    foreground: daisyuiColorObj['base-content'],
                },
                card: {
                    DEFAULT: daisyuiColorObj['base-100'],
                    foreground: daisyuiColorObj['base-content'],
                },
            },
            borderRadius: {
                lg: 'var(--radius)',
                md: 'calc(var(--radius) - 2px)',
                sm: 'calc(var(--radius) - 4px)',
            },
            keyframes: {
                'accordion-down': {
                    from: { height: 0 },
                    to: { height: 'var(--radix-accordion-content-height)' },
                },
                'accordion-up': {
                    from: { height: 'var(--radix-accordion-content-height)' },
                    to: { height: 0 },
                },
                'collapsible-down': {
                    from: { height: 0 },
                    to: { height: 'var(--radix-collapsible-content-height)' },
                },
                'collapsible-up': {
                    from: { height: 'var(--radix-collapsible-content-height)' },
                    to: { height: 0 },
                },
            },
            animation: {
                'accordion-down': 'accordion-down 0.2s ease-out',
                'accordion-up': 'accordion-up 0.2s ease-out',
                'collapsible-down': 'collapsible-down 0.2s ease-in-out',
                'collapsible-up': 'collapsible-up 0.2s ease-in-out',
            },
        },
    },
    plugins: [animate, require('daisyui')],
    daisyui: {
        themes: [
            {
                light: {
                    ...require('daisyui/src/theming/themes')['bumblebee'],
                    '--rounded-box': '0.5rem',
                    '--rounded-btn': '.5rem',
                    '--rounded-badge': '0.5rem',
                },
            },
        ],
    },
}
