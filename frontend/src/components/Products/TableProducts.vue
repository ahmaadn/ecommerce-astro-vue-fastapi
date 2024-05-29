<script lang="ts" setup>
import { ref, watch, onMounted } from 'vue'
import { getAllProducts } from '@/lib/products'
import type { Header, Item, ServerOptions } from 'vue3-easy-data-table'

const pathImg = import.meta.env.PUBLIC_BACKEND_API
const optionsServer = ref<ServerOptions>({
    page: 1,
    rowsPerPage: 10,
})
const loading = ref(true)
const serverItemsLength = ref(0)

const headers: Header[] = [
    { text: 'ID', value: 'barang_id', sortable: true },
    { text: 'Nama', value: 'nama_barang', sortable: true, width: 300 },
    { text: 'Harga', value: 'harga', sortable: true },
    { text: 'Status', value: 'status' },
    { text: 'Dibuat', value: 'dibuat_at' },
    { text: 'Update', value: 'diupdate_at' },
    { text: '', value: 'action', width: 20 },
]
const items = ref<Item[]>([])

const loadProducts = async () => {
    loading.value = true
    const options = optionsServer.value
    await getAllProducts({
        page: options.page,
        size: options.rowsPerPage,
    })
        .then((response) => {
            if (response.status == 200) {
                const data = response.data
                items.value = data.items
                serverItemsLength.value = data.total
                loading.value = false
            }
        })
        .catch((e) => {
            console.error(e)
        })
}

onMounted(async () => {
    await loadProducts()
})

watch(serverItemsLength, async (value) => {
    await loadProducts()
})
</script>
<template>
    <EasyDataTable
        v-model:server-options="optionsServer"
        table-class-name="content-table"
        :server-items-length="serverItemsLength"
        :headers="headers"
        :items="items"
        :loading="loading"
        :rows-items="[10, 15, 25, 50]"
    >
        <template #loading>
            <img
                src="https://i.pinimg.com/originals/94/fd/2b/94fd2bf50097ade743220761f41693d5.gif"
                style="width: 100px; height: 80px"
            />
        </template>
        <template #item-nama_barang="{ nama_barang, file_gambar }">
            <div class="player-wrapper">
                <div class="flex items-center gap-3">
                    <div class="avatar">
                        <div class="mask mask-squircle h-12 w-12">
                            <img
                                :src="`${pathImg}/${file_gambar}`"
                                alt="Avatar Tailwind CSS Component"
                            />
                        </div>
                    </div>
                    <div class="font-semibold">{{ nama_barang }}</div>
                </div>
            </div>
        </template>
        <template #item-action="{ barang_id }">
            <a :href="`/dashboard/products/${barang_id}`" class="btn btn-ghost btn-xs">details</a>
        </template>
    </EasyDataTable>
</template>
