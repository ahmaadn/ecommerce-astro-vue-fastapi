<script setup>
import Input from '../Form/Input.vue'
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import axios from 'axios'
import { auth } from '@/lib/auth'

const validationSchema = toTypedSchema(
    z
        .object({
            password: z.string(),
            new_password: z.string().min(8),
            confirm_password: z.string().min(8),
        })
        .superRefine(({ confirm_password, new_password }, ctx) => {
            if (confirm_password !== new_password) {
                ctx.addIssue({
                    message: 'The passwords did not match',
                    path: ['confirm_password'],
                    fatal: true,
                })
            }
        })
)

const form = useForm({ validationSchema })
const handleSubmit = form.handleSubmit(async (values) => {
    const { httpOptions } = auth.authorize()
    await axios
        .post(`${import.meta.env.PUBLIC_BACKEND_API}/users/new-password`, values, {
            headers: {
                'Content-Type': 'application/json',
                ...httpOptions.headers,
            },
        })
        .then((res) => {
            alert(res.data.detail)
            form.resetForm()
        })
        .catch((e) => {
            console.error(e)
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
})
</script>

<template>
    <form @submit="handleSubmit">
        <Input name="password" type="password" label="Password lama" />
        <Input name="new_password" type="password" label="Password baru" />
        <Input name="confirm_password" type="password" label="Konfirmasi password" />
        <button class="btn btn-success btn-sm" type="submit">Simpan</button>
    </form>
</template>
