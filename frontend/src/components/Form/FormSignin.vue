<script setup lang="ts">
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { useForm } from 'vee-validate'
import { auth } from '@/lib/auth'
import { ref } from 'vue'
import { Input } from '@/components/ui/input'

const formSchema = toTypedSchema(
    z.object({
        username: z.string().min(2).max(50),
        password: z.string().min(5).max(100),
    })
)

const form = useForm({
    validationSchema: formSchema,
})

const loading = ref(false)

const onSubmit = form.handleSubmit((values) => {
    loading.value = true
    auth.logIn(values)
        .then((resposes) => {
            console.log(auth.payLoad())
            if (resposes.status == 200) {
                window.location.href = '/'
            }
        })
        .catch((error) => {
            console.error(error)
        })
        .finally(() => {
            loading.value = false
        })
})
</script>

<template>
    <form @submit="onSubmit" class="space-y-4">
        <FormField v-slot="{ componentField }" name="username">
            <FormItem class="flex flex-col gap-2">
                <FormLabel>Username or email</FormLabel>
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
                    <Input type="text" v-bind="componentField" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <button type="submit" class="btn btn-secondary w-full" :disabled="loading">Submit</button>
    </form>
</template>
