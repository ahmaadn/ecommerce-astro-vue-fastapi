<script setup>
import { ref } from 'vue'
import axios from 'axios'
import * as FileDownload from 'js-file-download'
import { auth } from '@/lib/auth'

const disabled = ref(false)

const onClick = async () => {
    disabled.value = true
    axios({
        url: `${import.meta.env.PUBLIC_BACKEND_API}/payments/export`,
        method: 'GET',
        responseType: 'blob',
        headers: {
            ...auth.authorize().httpOptions.headers,
        },
    })
        .then((res) => {
            const url = window.URL.createObjectURL(new Blob([res]))
            const a = document.createElement('a')
            a.href = url
            const filename = `payment.xlsx`
            a.setAttribute('download', filename)
            document.body.appendChild(a)
            a.click()
            a.remove()
        })
        .finally(() => (disabled.value = false))
}
</script>

<template>
    <button class="btn btn-secondary btn-sm" id="btn-report" @click="onClick" :disabled="disabled">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
            <path
                fill="currentColor"
                d="M13 9V3.5L18.5 9M6 2c-1.11 0-2 .89-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"
            />
        </svg>
        Export
    </button>
</template>
