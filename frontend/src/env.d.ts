/// <reference types="astro/client" />
interface ImportMetaEnv {
    readonly PUBLIC_BACKEND_API: string
    // more env variables...
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
