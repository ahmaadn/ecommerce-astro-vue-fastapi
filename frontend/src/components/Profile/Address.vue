<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Input from '../Form/Input.vue'
import Select from '../Form/Select.vue'
import Textarea from '../Form/Textarea.vue'
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import axios from 'axios'
import { auth } from '@/lib/auth'

const hasAddress = ref(false)

const provinsi = ref<{ provinsi_id: Number; name_provinsi: String }[]>([])
const kabupaten = ref<{ kabupaten_id: Number; nama_kabupaten: String }[]>([])
const kecamatan = ref<{ kecamatan_id: Number; nama_kecamatan: String }[]>([])

const validationSchema = toTypedSchema(
    z.object({
        provinsi_id: z.number(),
        kabupaten_id: z.number(),
        kecamatan_id: z.number(),
        zip_code: z.string(),
        baris_alamat: z.string(),
    })
)

const form = useForm({ validationSchema })

const handleSubmit = form.handleSubmit(async (values) => {
    // alert(values)
    const { headers: headersAuth } = auth.authorize().httpOptions
    const methode = hasAddress.value ? 'PUT' : 'POST'
    await axios(`${import.meta.env.PUBLIC_BACKEND_API}/addresses`, {
        method: methode,
        data: values,
        headers: { 'Content-Type': 'application/json', ...headersAuth },
    })
        .then((res) => {
            const data = res.data
            alert(JSON.stringify(data))
        })
        .catch((e) => {
            console.error(e)
        })
})

const onChangeProvinsi = async (e: Event) => {
    form.resetField('kabupaten_id')
    form.resetField('kecamatan_id')
    kabupaten.value = []
    kecamatan.value = []

    await getKabupaten(form.values.provinsi_id || 11)
}

const onChangeKabupaten = async (e: Event) => {
    form.resetField('kecamatan_id')
    kecamatan.value = []

    await getKecamatan(form.values.kabupaten_id)
}

const getProvinsi = async () => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/addresses/provinsi`)
        .then((res) => {
            const data = res.data
            provinsi.value = data
        })
        .catch((e) => {
            console.error(e)
        })
}

const getKabupaten = async (provinsi_id: Number) => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/addresses/kabupaten`, {
            params: { provinsi_id },
        })
        .then((res) => {
            const data = res.data
            kabupaten.value = data
        })
        .catch((e) => {
            console.error(e)
        })
}

const getKecamatan = async (kabupaten_id: Number) => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/addresses/kecamatan`, {
            params: { kabupaten_id },
        })
        .then((res) => {
            const data = res.data
            kecamatan.value = data
        })
        .catch((e) => {
            console.error(e)
        })
}

const getUserAddress = async () => {
    const { headers } = auth.authorize().httpOptions
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/addresses`, { headers })
        .then(async (res) => {
            const data = res.data
            await getKabupaten(data.provinsi.provinsi_id)
            await getKecamatan(data.kabupaten.kabupaten_id)
            form.setValues({
                provinsi_id: data.provinsi.provinsi_id,
                kabupaten_id: data.kabupaten.kabupaten_id,
                kecamatan_id: data.kecamatan.kecamatan_id,
                zip_code: data.zip_code,
                baris_alamat: data.baris_alamat,
            })
        })
        .catch((e) => {
            hasAddress.value = false
            if (e.response) {
                if (e.response.status != 404) {
                    alert(e.response.data.detail)
                }
            } else {
                console.error(e)
            }
        })
}

onMounted(async () => {
    await getProvinsi()
    await getUserAddress()
})
</script>

<template>
    <form @submit="handleSubmit">
        <Select name="provinsi_id" @change="onChangeProvinsi" label="provinsi*">
            <option
                v-for="(value, index) in provinsi"
                :value="value.provinsi_id"
                v-bind:key="index"
            >
                {{ value.name_provinsi }}
            </option>
        </Select>
        <Select name="kabupaten_id" label="Kabupaten*" @change="onChangeKabupaten">
            <option
                v-for="(value, index) in kabupaten"
                :value="value.kabupaten_id"
                v-bind:key="index"
            >
                {{ value.nama_kabupaten }}
            </option>
        </Select>
        <Select name="kecamatan_id" label="Kelurahan*">
            <option
                v-for="(value, index) in kecamatan"
                :value="value.kecamatan_id"
                v-bind:key="index"
            >
                {{ value.nama_kecamatan }}
            </option>
        </Select>
        <Input name="zip_code" label="Kode Post*" />
        <Textarea name="baris_alamat" label="Baris Alamat*"></Textarea>
        <button class="btn btn-success btn-sm w-full">Simpan Alamat</button>
    </form>
</template>
