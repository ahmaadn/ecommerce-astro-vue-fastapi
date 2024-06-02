<script lang="ts" setup>
import type { ProductDetailResult } from '@/types'
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { onMounted } from 'vue'
import KategoryForm from './DetailProduct/KategoryForm.vue'
import StatusForm from './DetailProduct/StatusForm.vue'
import DetailProductForm from './DetailProduct/DetailProductForm.vue'
import TableVarianForm from './DetailProduct/TableVarianForm.vue'
import ImageUpload from './DetailProduct/ImageUpload.vue'
import axios from 'axios'
import { auth } from '@/lib/auth'

const props = defineProps<{
    product: ProductDetailResult
}>()

const product = props.product

const validationSchema = toTypedSchema(
    z.object({
        nama_barang: z.string().max(100).min(1),
        deskripsi: z.string().max(300).min(1),
        harga: z.number().positive().gt(1000),
        kategori_id: z.number().positive(),
        status: z.enum(['active', 'draft']),
    })
)

const form = useForm({ validationSchema })
const onSumbit = form.handleSubmit(async (values) => {
    const { headers: headerAuth } = auth.authorize().httpOptions
    await axios
        .put(`${import.meta.env.PUBLIC_BACKEND_API}/products`, values, {
            params: {
                barang_id: product.barang_id,
            },
            headers: {
                'Content-Type': 'application/json',
                ...headerAuth,
            },
        })
        .then((res) => {
            const detail = res.data.detail
            alert(detail)
            window.location.href = `/dashboard/products/details?product=${product.barang_id}`
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
})

const onDelete = async () => {
    const { headers } = auth.authorize().httpOptions
    await axios
        .delete(`${import.meta.env.PUBLIC_BACKEND_API}/products?barang_id=${product.barang_id}`, {
            headers,
        })
        .then((res) => {
            const detail = res.data.detail
            alert(detail)
            window.location.href = '/dashboard/products'
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
    form.setValues({ kategori_id: product.kategori.kategori_id, ...product })
})
</script>

<template>
    <div class="space-y-8">
        <form @submit="onSumbit">
            <div class="flex items-center justify-between pb-4">
                <div class="inline-flex items-center gap-2 font-semibold">
                    <a href="/dashboard/products" class="btn btn-square">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            width="24"
                            height="24"
                        >
                            <path
                                fill="currentColor"
                                d="M15.41 16.58L10.83 12l4.58-4.59L14 6l-6 6l6 6z"
                            />
                        </svg>
                    </a>
                    <div class="text-2xl">{{ product.nama_barang }}</div>
                    <div
                        class="badge"
                        :class="{
                            'badge-accent': product.status == 'draft',
                            'badge-success': product.status == 'active',
                        }"
                    >
                        {{ product.status }}
                    </div>
                </div>
                <div class="inline-flex gap-4">
                    <button type="submit" class="btn btn-success btn-sm">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                        >
                            <path
                                fill="currentColor"
                                d="M15 9H5V5h10m-3 14a3 3 0 0 1-3-3a3 3 0 0 1 3-3a3 3 0 0 1 3 3a3 3 0 0 1-3 3m5-16H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7z"
                            />
                        </svg>
                        Simpan
                    </button>
                    <button type="button" class="btn btn-error btn-sm" @click="onDelete">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                        >
                            <path
                                fill="currentColor"
                                d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"
                            />
                        </svg>
                        Hapus
                    </button>
                </div>
            </div>

            <div class="flex w-full flex-col gap-8 md:flex-row">
                <div class="flex w-full flex-col gap-8 md:w-3/4">
                    <DetailProductForm></DetailProductForm>
                </div>
                <div class="flex w-full flex-col gap-8 md:w-1/4">
                    <kategoryForm></kategoryForm>
                    <StatusForm></StatusForm>
                </div>
            </div>
        </form>
        <TableVarianForm
            :barang_id="product.barang_id"
            :list_variant="product.list_varian"
        ></TableVarianForm>
        <ImageUpload :src="product.file_gambar" :barang_id="product.barang_id"> </ImageUpload>
    </div>
</template>
