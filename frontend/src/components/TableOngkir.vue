<script setup lang="ts">
import type { ClickRowArgument, Header, Item } from 'vue3-easy-data-table'
import Input from '@/components/Form/Input.vue'
import { onMounted, ref } from 'vue'
import axios from 'axios'
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { auth } from '@/lib/auth'

const headers: Header[] = [
    { text: 'ID', value: 'provinsi_id' },
    { text: 'Nama', value: 'name_provinsi' },
    { text: 'Ongkir', value: 'ongkir' },
]
const selected = ref(0)
const items = ref<Item[]>([])

const validationSchema = toTypedSchema(
    z.object({
        name_provinsi: z.string(),
        ongkir: z.number().positive(),
    })
)
const form = useForm({ validationSchema })

const handleSubmit = form.handleSubmit(async (values) => {
    if (selected.value == 0) {
        return
    }

    const { httpOptions } = auth.authorize()

    axios
        .put(
            `${import.meta.env.PUBLIC_BACKEND_API}/addresses/ongkir`,
            {},
            {
                params: {
                    provinsi_id: selected.value,
                    ongkir: values.ongkir,
                },
                headers: { ...httpOptions.headers },
            }
        )
        .then(async (res) => {
            alert(res.data.detail)
            await getOngkirByProvinsi()
        })
        .catch((e) => {
            console.error(e)
        })
})

const getOngkirByProvinsi = async () => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/addresses/provinsi`)
        .then((res) => {
            items.value = res.data
        })
        .catch((e) => {
            console.error(e)
        })
}

const showRow = (item: ClickRowArgument) => {
    selected.value = item.provinsi_id

    form.setValues({ ...item })
}

onMounted(getOngkirByProvinsi)
</script>

<template>
    <EasyDataTable :headers="headers" :items="items" show-index @click-row="showRow">
    </EasyDataTable>
    <form @submit="handleSubmit">
        <div class="inline-flex w-full gap-2">
            <Input name="name_provinsi" label="Nama provinsi" disabled />
            <Input name="ongkir" label="Ongkir" type="number" />
        </div>
        <button type="submit" class="btn btn-success btn-sm w-full">Perbahari</button>
    </form>
</template>
