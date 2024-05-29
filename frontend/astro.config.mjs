import { defineConfig } from 'astro/config'

import vue from '@astrojs/vue'
import tailwind from '@astrojs/tailwind'
import icon from 'astro-icon'

// https://astro.build/config
export default defineConfig({
    output: 'server',
    integrations: [
        vue({ appEntrypoint: '/src/pages/_app' }),
        tailwind({
            applyBaseStyles: false,
        }),
        icon({
            include: {
                mdi: ['*'],
            },
        }),
    ],
})
