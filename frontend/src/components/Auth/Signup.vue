<script setup lang="ts">
import { auth } from '@/lib/auth'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { z } from 'zod'
import Input from '../Form/Input.vue'

const props = defineProps({ urlSuccress: String })

const formSchema = toTypedSchema(
    z.object({
        nama: z.string().min(3).max(100),
        username: z.string().min(5).max(100),
        email: z.string().min(5).max(100).email(),
        no_hp: z.string().optional(),
        password: z.string().min(8).max(100),
    })
)

const form = useForm({
    validationSchema: formSchema,
})

const onSubmit = form.handleSubmit((values) => {
    auth.register(values)
        .then((res) => {
            window.location.href = props.urlSuccress || '/'
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
})
</script>

<template>
    <form @submit="onSubmit">
        <Input name="nama" label="Nama Lengkap*" />
        <Input name="username" label="Username*" />
        <Input name="email" label="Email*" type="email" />
        <Input name="np_hp" label="Nomer handphone" />
        <Input name="password" label="Password*" type="password" />
        <button type="submit" class="btn btn-secondary w-full">Submit</button>
    </form>
</template>
