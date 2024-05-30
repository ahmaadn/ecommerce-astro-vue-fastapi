<script lang="ts" setup>
import { auth } from '@/lib/auth'
import { toTypedSchema } from '@vee-validate/zod'
import axios from 'axios'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import { ref, onMounted } from 'vue'
import * as z from 'zod'

const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
const MAX_FILE_SIZE = 5000000
const kategories = ref<
    {
        kategori_id: Number
        nama_kategori: String
    }[]
>([])
const loading = ref(false)

onMounted(async () => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/categories`)
        .then((res) => {
            if (res.status == 200) {
                const data = res.data
                kategories.value = data
            }
        })
        .catch((e) => {
            console.error(e)
        })
})

const validationSchema = toTypedSchema(
    z.object({
        nama_barang: z.string().max(100),
        deskripsi: z.string(),
        harga: z.number().positive(),
        kategori_id: z.number().positive(),
        status: z.enum(['active', 'draft']),
        gambar: z
            .any()
            .refine((file) => file?.size <= MAX_FILE_SIZE, `Max image size is 5MB.`)
            .refine(
                (file) => ACCEPTED_IMAGE_TYPES.includes(file?.type),
                'Only .jpg, .jpeg, .png and .webp formats are supported.'
            ),
    })
)

const form = useForm({ validationSchema })

const onSubmit = form.handleSubmit((values) => {
    loading.value = true
    const { headers: headersAuth } = auth.authorize().httpOptions
    const formData = new FormData()
    formData.append('gambar', values.gambar)
    axios
        .post(`${import.meta.env.PUBLIC_BACKEND_API}/products`, formData, {
            params: {
                nama: values.nama_barang,
                status: values.status,
                deskripsi: values.deskripsi,
                kategory_id: values.kategori_id,
                harga: values.harga,
            },
            headers: {
                'Content-Type': 'multipart/form-data',
                ...headersAuth,
            },
        })
        .then((response) => {
            if (response.status >= 200 && response.status <= 300) {
                window.location.href = '/dashboard/products'
            }
        })
        .catch((e) => {
            console.error(e)
        })
        .finally(() => {
            loading.value = true
        })
})
</script>

<template>
    <form @submit="onSubmit" class="w-full">
        <div class="form-control w-full">
            <label class="label">
                <span class="label-text">Nama</span>
            </label>
            <Field
                name="nama_barang"
                type="text"
                placeholder="Masukkan nama"
                class="input input-bordered w-full"
            ></Field>
            <div class="label">
                <ErrorMessage name="nama_barang" class="text-sm text-error"></ErrorMessage>
            </div>
        </div>

        <div class="form-control">
            <label class="label">
                <span class="label-text">Deskripsi</span>
            </label>
            <Field
                name="deskripsi"
                as="textarea"
                class="textarea textarea-bordered h-24"
                placeholder="Bio"
            ></Field>
            <div class="label">
                <ErrorMessage name="deskripsi" class="text-sm text-error"></ErrorMessage>
            </div>
        </div>
        <div class="form-control w-full">
            <label class="label">
                <span class="label-text">Harga</span>
            </label>
            <Field
                name="harga"
                type="number"
                placeholder="Masukkan harga"
                class="input input-bordered w-full"
            ></Field>
            <div class="label">
                <ErrorMessage name="harga" class="text-sm text-error"></ErrorMessage>
            </div>
        </div>
        <div class="form-control w-full">
            <label class="label">
                <span class="label-text">Kategori</span>
            </label>
            <Field name="kategori_id" class="select select-bordered" as="select">
                <option
                    v-for="(kategori, index) in kategories"
                    v-bind:key="index"
                    :value="kategori.kategori_id"
                >
                    {{ kategori.nama_kategori }}
                </option>
            </Field>
        </div>
        <div class="form-control w-full">
            <label class="label">
                <span class="label-text">Status</span>
            </label>
            <Field name="status" class="select select-bordered" as="select">
                <option value="active">Active</option>
                <option value="draft">Draft</option>
            </Field>
        </div>
        <div class="form-control w-full max-w-xs">
            <label class="label">
                <span class="label-text">Upload gambar</span>
            </label>
            <Field
                name="gambar"
                type="file"
                class="file-input file-input-bordered file-input-sm w-full"
                id="gambar"
            />
            <div class="label">
                <ErrorMessage name="gambar" class="text-sm text-error"></ErrorMessage>
            </div>
        </div>
        <button type="submit" class="btn btn-success" :disabled="loading">Buat Barang</button>
    </form>
</template>
