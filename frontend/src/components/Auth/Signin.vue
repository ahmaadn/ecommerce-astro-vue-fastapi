<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { useForm } from 'vee-validate'
import { auth } from '@/lib/auth'
import Input from '../Form/Input.vue'

const formSchema = toTypedSchema(
    z.object({
        username: z.string().min(2).max(50),
        password: z.string().min(5).max(100),
    })
)

const form = useForm({
    validationSchema: formSchema,
})

const onSubmit = form.handleSubmit((values) => {
    auth.logIn(values)
        .then((resposes) => {
            if (resposes.status == 200) {
                window.location.href = '/'
            }
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
        <Input name="username" label="Username atau email" />
        <Input name="password" type="password" label="Password" />
        <button type="submit" class="btn btn-secondary w-full">Submit</button>
    </form>
</template>
