<script setup lang="ts">
import { auth } from '@/lib/auth'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import type { Header, Item } from 'vue3-easy-data-table'

const headers: Header[] = [
    { text: 'username', value: 'username' },
    { text: 'email', value: 'email', width: 300 },
    { text: 'ho_hp', value: 'no_hp' },
    { text: 'role', value: 'role' },
    { text: 'Dibuat', value: 'dibuat_at' },
    { text: 'Update', value: 'diupdate_at' },
    { text: '', value: 'action', width: 20 },
]
const items = ref<Item[]>([])

const loadUser = async () => {
    const { headers: headerAuth } = auth.authorize().httpOptions
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/users`, {
            headers: {
                'Content-Type': 'application/json',
                ...headerAuth,
            },
        })
        .then((res) => {
            if (res.status == 200) {
                const data = res.data
                items.value = data.items
            }
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
    await loadUser()
})
</script>

<template>
    <EasyDataTable :headers="headers" :items="items" show-index>
        <template #loading>
            <img
                src="https://i.pinimg.com/originals/94/fd/2b/94fd2bf50097ade743220761f41693d5.gif"
                style="width: 100px; height: 80px"
            />
        </template>
        <template #item-dibuat_at="{ dibuat_at }">
            {{ new Date(dibuat_at + 'Z').toLocaleDateString('id-ID') }}
        </template>
        <template #item-diupdate_at="{ diupdate_at }">
            {{ new Date(diupdate_at + 'Z').toLocaleDateString('id-ID') }}
        </template>
        <template #item-role="{ role }">
            <div
                class="badge"
                :class="{ 'badge-accent': role == 'admin', 'badge-primary': role == 'active' }"
            >
                {{ role }}
            </div>
        </template>
        <template #item-action="{ username }">
            <a :href="`/dashboard/users/details?username=${username}`" class="btn btn-ghost btn-xs"
                >details</a
            >
        </template>
    </EasyDataTable>
</template>
