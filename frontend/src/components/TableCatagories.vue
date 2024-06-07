<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'
import type { Header, Item, ClickRowArgument } from 'vue3-easy-data-table'
import Input from './Form/Input.vue'
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { auth } from '@/lib/auth'

const headers: Header[] = [
    { text: 'ID', value: 'kategori_id' },
    { text: 'Nama', value: 'nama_kategori' },
]

const items = ref<Item[]>([])
const selectedkategory = ref<Number>(0)

const validationSchema = toTypedSchema(
    z.object({
        nama_kategori: z.string().min(1),
    })
)

const form = useForm({ validationSchema })

const loadKategories = async () => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/categories`)
        .then((res) => {
            if (res.status == 200) {
                const data = res.data
                items.value = data
            }
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}

onMounted(async () => {
    await loadKategories()
})

const showRow = (item: ClickRowArgument) => {
    selectedkategory.value = item.kategori_id
    form.setValues({ nama_kategori: item.nama_kategori })
}

const handleSubmit = form.handleSubmit(async (values) => {
    if (selectedkategory.value) {
        await onUpdate(values.nama_kategori)
    } else {
        await onCreate(values.nama_kategori)
    }
    await loadKategories()
})

const onCancel = () => {
    selectedkategory.value = 0
    form.resetForm()
}

const onCreate = async (values: String) => {
    const { headers: headersAuth } = auth.authorize().httpOptions
    await axios
        .post(
            `${import.meta.env.PUBLIC_BACKEND_API}/categories`,
            {},
            {
                params: { nama_kategori: values },
                headers: headersAuth,
            }
        )
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}

const onUpdate = async (values: String) => {
    const { headers: headersAuth } = auth.authorize().httpOptions
    await axios
        .put(
            `${import.meta.env.PUBLIC_BACKEND_API}/categories`,
            {},
            {
                params: { kategori_id: selectedkategory.value, nama_kategori: values },
                headers: headersAuth,
            }
        )
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}
</script>

<template>
    <EasyDataTable :headers="headers" :items="items" show-index @click-row="showRow">
    </EasyDataTable>
    <form @submit="handleSubmit">
        <div class="inline-flex w-full gap-2">
            <Input name="nama_kategori" label="Nama kategory" />
        </div>
        <div class="grid w-full grid-cols-2 gap-2" v-if="selectedkategory">
            <button type="button" id="close" class="btn btn-sm" @click="onCancel">Batalkan</button>
            <button type="submit" id="simpan" class="btn btn-info btn-sm">Perbaharui</button>
        </div>
        <button type="submit" class="btn btn-success btn-sm w-full" v-else>Add variant</button>
    </form>
</template>
