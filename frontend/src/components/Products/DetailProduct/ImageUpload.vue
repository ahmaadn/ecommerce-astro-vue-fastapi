<script setup>
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import { ref } from 'vue'
import axios from 'axios'
import { auth } from '@/lib/auth'

const props = defineProps({
    src: String,
    barang_id: Number,
})

const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
const MAX_FILE_SIZE = 5000000
const defaultImage = `${import.meta.env.PUBLIC_BACKEND_API}/${props.src}`
const pathImage = ref(defaultImage)

const validationSchema = toTypedSchema(
    z.object({
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

const handleSubmit = form.handleSubmit(async (values) => {
    const { headers: headersAuth } = auth.authorize().httpOptions
    const formData = new FormData()
    formData.append('gambar', values.gambar)
    await axios
        .post(`${import.meta.env.PUBLIC_BACKEND_API}/products/update-image`, formData, {
            params: {
                barang_id: props.barang_id,
            },
            headers: {
                'Content-Type': 'multipart/form-data',
                ...headersAuth,
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

const onFileChange = (e) => {
    const file = e.target.files[0]
    pathImage.value = URL.createObjectURL(file)
}
</script>

<template>
    <div class="w-full md:w-3/4">
        <div class="card bg-base-100 shadow-xl md:mr-6">
            <div class="card-body">
                <h2 class="card-title">Gambar Barang</h2>
                <form @submit="handleSubmit">
                    <div>
                        <div id="preview" class="w-56">
                            <img v-if="pathImage" :src="pathImage" />
                        </div>
                    </div>
                    <div class="form-control w-full max-w-xs">
                        <label class="label font-semibold">
                            <span class="label-text">Pilih Gambar</span>
                        </label>
                        <Field
                            name="gambar"
                            type="file"
                            class="file-input file-input-bordered w-full max-w-xs"
                            @change="onFileChange"
                        />
                        <div class="label">
                            <span class="label-text-alt text-error">
                                <ErrorMessage name="gambar"></ErrorMessage>
                            </span>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success btn-sm">Update Gambar</button>
                </form>
            </div>
        </div>
    </div>
</template>
