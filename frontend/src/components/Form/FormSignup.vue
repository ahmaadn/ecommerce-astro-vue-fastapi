<script setup lang="ts">
import {
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import { auth } from '@/lib/auth'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import { ref } from 'vue'
import { z } from 'zod'
import { Input } from '@/components/ui/input'

const formSchema = toTypedSchema(
    z.object({
        name: z.string().min(3).max(100),
        username: z.string().min(5).max(100),
        email: z.string().min(5).max(100).email(),
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
                setTimeout(() => {
                    window.location.href = '/signin'
                }, 600)
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
        <FormField v-slot="{ componentField }" name="name">
            <FormItem class="flex flex-col gap-2">
                <FormLabel>name</FormLabel>
                <FormControl>
                    <Input type="text" v-bind="componentField" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="username">
            <FormItem class="flex flex-col gap-2">
                <FormLabel>username</FormLabel>
                <FormControl>
                    <Input type="text" v-bind="componentField" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="email">
            <FormItem class="flex flex-col gap-2">
                <FormLabel>email</FormLabel>
                <FormControl>
                    <Input type="text" v-bind="componentField" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="password">
            <FormItem class="flex flex-col gap-2">
                <FormLabel>password</FormLabel>
                <FormControl>
                    <Input type="password" v-bind="componentField" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
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
