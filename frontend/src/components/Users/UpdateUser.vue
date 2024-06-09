<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { onMounted } from 'vue'
import { z } from 'zod'
import type { UserDetail } from '@/types'
import DetailForm from './Form/DetailForm.vue'
import RoleForm from './Form/RoleForm.vue'
import StatusForm from './Form/StatusForm.vue'
import { auth } from '@/lib/auth'
import axios from 'axios'

const props = defineProps<{ user: UserDetail }>()

const validationSchema = toTypedSchema(
    z.object({
        nama: z.string().min(3).max(100),
        username: z.string().min(5).max(100),
        email: z.string().max(100).email(),
        no_hp: z.string().nullable(),
        role: z.string(),
        is_aktif: z.boolean(),
    })
)

const form = useForm({ validationSchema })

const onSumbit = form.handleSubmit(async (values) => {
    const { headers: headersAuth } = auth.authorize().httpOptions
    await axios
        .put(`${import.meta.env.PUBLIC_BACKEND_API}/users`, values, {
            params: {
                username: props.user.username,
            },
            headers: {
                'Content-Type': 'application/json',
                ...headersAuth,
            },
        })
        .then((res) => {
            if (res.status >= 200 && res.status <= 300) {
                alert(res.data.detail)
                if (values.username != props.user.username) {
                    auth.logOut()
                    window.location.href = `/signin`
                } else {
                    window.location.href = `/dashboard/users/details?username=${props.user.username}`
                }
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

onMounted(() => {
    form.setValues({ ...props.user })
})
</script>

<template>
    <form @submit="onSumbit">
        <div class="flex items-center justify-between pb-4">
            <div class="inline-flex items-center gap-2 font-semibold">
                <a href="/dashboard/users" class="btn btn-square">
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
                <div class="text-2xl">{{ user.nama }}</div>
                <div
                    class="badge"
                    :class="{
                        'badge-success': user.role == 'admin',
                        'badge-accent': user.role == 'user',
                    }"
                >
                    {{ user.role }}
                </div>
            </div>
            <button class="btn btn-success btn-sm" type="submit">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                    <path
                        fill="currentColor"
                        d="M15 9H5V5h10m-3 14a3 3 0 0 1-3-3a3 3 0 0 1 3-3a3 3 0 0 1 3 3a3 3 0 0 1-3 3m5-16H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7z"
                    />
                </svg>
                Simpan
            </button>
        </div>
        <div class="flex w-full flex-col gap-8 md:flex-row">
            <div class="flex w-full flex-col gap-8 md:w-3/4">
                <DetailForm></DetailForm>
            </div>
            <div class="flex w-full flex-col gap-8 md:w-1/4">
                <RoleForm></RoleForm>
                <StatusForm></StatusForm>
            </div>
        </div>
    </form>
</template>
