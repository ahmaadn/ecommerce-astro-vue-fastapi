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
import { users } from '@/lib/users'
import Summary from './Summary.vue'

const hasAddress = ref(false)
const ongkir = ref(0)
const provinsi = ref<{ provinsi_id: Number; name_provinsi: String; ongkir: Number }[]>([])
const kabupaten = ref<{ kabupaten_id: Number; nama_kabupaten: String }[]>([])
const kecamatan = ref<{ kecamatan_id: Number; nama_kecamatan: String }[]>([])

const validationSchema = toTypedSchema(
    z.object({
        nama: z.string().min(3).max(100),
        email: z.string().max(100).email(),
        no_hp: z.string().max(20),
        provinsi_id: z.number(),
        kabupaten_id: z.number(),
        kecamatan_id: z.number(),
        zip_code: z.string(),
        baris_alamat: z.string(),
    })
)

const form = useForm({ validationSchema })

const handleSubmit = form.handleSubmit(async (values) => {
    // update user
    await axios
        .put(
            `${import.meta.env.PUBLIC_BACKEND_API}/users/me`,
            {
                nama: values.nama,
                email: values.email,
                no_hp: values.no_hp,
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    ...auth.authorize().httpOptions.headers,
                },
            }
        )
        .catch((e) => {
            console.error(e)
        })

    // add alamat
    await axios(`${import.meta.env.PUBLIC_BACKEND_API}/addresses`, {
        method: hasAddress.value ? 'PUT' : 'POST',
        data: {
            provinsi_id: values.provinsi_id,
            kabupaten_id: values.kabupaten_id,
            kecamatan_id: values.kecamatan_id,
            zip_code: values.zip_code,
            baris_alamat: values.baris_alamat,
        },
        headers: { 'Content-Type': 'application/json', ...auth.authorize().httpOptions.headers },
    }).catch((e) => {
        console.error(e)
    })

    // buat pesanan
    await axios
        .post(
            `${import.meta.env.PUBLIC_BACKEND_API}/orders/checkout`,
            {},
            {
                ...auth.authorize().httpOptions,
            }
        )
        .then((res) => {
            alert(res.data.detail)
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
                window.location.href = '/dashboard/orders'
            } else {
                console.error(e)
            }
        })
})

const onChangeProvinsi = async (e: any) => {
    form.resetField('kabupaten_id')
    form.resetField('kecamatan_id')
    kabupaten.value = []
    kecamatan.value = []

    ongkir.value =
        provinsi.value.find((value) => value.provinsi_id == form.values.provinsi_id).ongkir || 0

    await getKabupaten(form.values.provinsi_id || 11)
}

const onChangeKabupaten = async (e: Event) => {
    form.resetField('kecamatan_id')
    kecamatan.value = []

    await getKecamatan(form.values.kabupaten_id || 11)
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
            hasAddress.value = true
            // ongkir
            ongkir.value = provinsi.value.find(
                (value) => value.provinsi_id == form.values.provinsi_id
            ).ongkir
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

const getUserDetail = async () => {
    const userData = await users.getDetail()
    form.setValues({
        nama: userData.nama,
        email: userData.email,
        no_hp: userData.no_hp,
    })
}

onMounted(async () => {
    await getProvinsi()
    await getUserAddress()
    await getUserDetail()
})
</script>

<template>
    <div class="grid grid-cols-[1fr_40%] gap-4 py-8">
        <div class="card h-fit bg-base-100">
            <form class="card-body" @submit="handleSubmit">
                <div class="card-title">Tagihan</div>
                <Input name="nama" label="Nama lengkap*" />
                <Input name="email" label="email*" />
                <Input name="no_hp" label="No handphone*" />
                <div class="card-title">Alamat</div>

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
                <Select name="kecamatan_id" label="Kecamatan*">
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
                <button class="btn btn-success btn-sm w-full">Bayar Pesanaan</button>
            </form>
        </div>
        <Summary v-model:ongkir="ongkir"></Summary>
    </div>
</template>
