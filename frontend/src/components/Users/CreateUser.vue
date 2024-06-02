<script setup lang="ts">
import { auth } from '@/lib/auth'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ref } from 'vue'
import { z } from 'zod'
import Input from '../Form/Input.vue'

const formSchema = toTypedSchema(
    z.object({
        nama: z.string().min(3).max(100),
        username: z.string().min(5).max(100),
        email: z.string().min(5).max(100).email(),
        no_hp: z.number().optional(),
        password: z.string().min(8).max(100),
    })
)

const loading = ref(false)

const form = useForm({
    validationSchema: formSchema,
})

const onSubmit = form.handleSubmit((values) => {
    loading.value = true
    auth.register(values)
        .then((respones) => {
            if (respones.status >= 200 && respones.status <= 300) {
                window.location.href = '/dashboard/users'
            } else if (respones.status == 406) {
                console.log('Email sudah ada yang pake')
            }
        })
        .catch((error) => {
            console.log(error)
        })
})
</script>

<template>
    <form @submit="onSubmit" class="space-y-4">
        <Input name="nama" label="Nama Lengkap" />
        <Input name="username" label="Username" />
        <Input name="email" label="Email" type="email" />
        <Input name="np_hp" label="Nomer handphone" type="number" />
        <Input name="password" label="Password" type="password" />
        <button type="submit" class="btn btn-secondary w-full" :disabled="loading">Submit</button>
    </form>
</template>

<style scoped>
input[type='number']::-webkit-inner-spin-button,
input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>
