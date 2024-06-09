<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import type { Header, Item, ServerOptions } from 'vue3-easy-data-table'
import { tanggal } from '@/lib/utils'
import { users } from '@/lib/users'

const optionsServer = ref<ServerOptions>({
    page: 1,
    rowsPerPage: 25,
})
const serverItemsLength = ref(0)

const headers: Header[] = [
    { text: 'username', value: 'username' },
    { text: 'email', value: 'email', width: 300 },
    { text: 'role', value: 'role' },
    { text: 'Status', value: 'is_aktif' },
    { text: 'Dibuat', value: 'dibuat_at' },
    { text: 'Update', value: 'diupdate_at' },
    { text: '', value: 'action', width: 20 },
]
const items = ref<Item[]>([])

const loadUser = async () => {
    const options = optionsServer.value
    const data = await users.getAllUsers({ page: options.page, size: options.rowsPerPage })
    items.value = data.items
    serverItemsLength.value = data.total
}

watch(optionsServer, loadUser)
onMounted(loadUser)
</script>

<template>
    <EasyDataTable
        v-model:server-options="optionsServer"
        :server-items-length="serverItemsLength"
        :headers="headers"
        :items="items"
        :rows-items="[25, 50, 100]"
        show-index
    >
        <template #loading>
            <img
                src="https://i.pinimg.com/originals/94/fd/2b/94fd2bf50097ade743220761f41693d5.gif"
                style="width: 100px; height: 80px"
            />
        </template>
        <template #item-dibuat_at="{ dibuat_at }">
            {{ tanggal(new Date(dibuat_at + 'Z')) }}
        </template>
        <template #item-diupdate_at="{ diupdate_at }">
            {{ tanggal(new Date(diupdate_at + 'Z')) }}
        </template>
        <template #item-role="{ role }">
            <div
                class="badge"
                :class="{ 'badge-primary': role == 'admin', 'badge-secondary': role == 'user' }"
            >
                {{ role }}
            </div>
        </template>
        <template #item-is_aktif="{ is_aktif }">
            <div class="flex items-center gap-2">
                <span
                    class="badge badge-xs"
                    :class="{ 'badge-info': is_aktif, 'badge-error': !is_aktif }"
                ></span>
                {{ is_aktif ? 'Active' : 'Not active' }}
            </div>
        </template>
        <template #item-action="{ username }">
            <a :href="`/dashboard/users/details?username=${username}`" class="btn btn-ghost btn-xs"
                >details</a
            >
        </template>
    </EasyDataTable>
</template>
