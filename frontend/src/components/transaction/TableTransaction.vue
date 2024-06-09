<script setup lang="ts">
import { auth } from '@/lib/auth'
import { onMounted, ref, defineProps, watch } from 'vue'
import type { Header, Item, ServerOptions } from 'vue3-easy-data-table'
import { rupiah, tanggal } from '@/lib/utils'
import axios from 'axios'

const props = defineProps({
    permission: {
        type: String,
    },
})

const permission = ref(props.permission)
const serverItemsLength = ref(0)
const optionsServer = ref<ServerOptions>({
    page: 1,
    rowsPerPage: 50,
})

const headers: Header[] = [
    { text: 'ID Transaksi', value: 'pembayaran_id' },
    { text: 'ID Pemesanan', value: 'pesanan_id' },
    { text: 'ID User', value: 'user_id' },
    { text: 'Total Dibayar', value: 'total_dibayar' },
    { text: 'Status', value: 'status_bayar' },
    { text: 'dibuat', value: 'dibuat_at' },
    { text: 'dibayar', value: 'dibayar_at' },
]
const items = ref<Item[]>([])

const getHistoriPembayaran = async () => {
    const options = optionsServer.value
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/payments`, {
            params: {
                page: options.page,
                size: options.rowsPerPage,
            },
            ...auth.authorize().httpOptions,
        })
        .then((res) => {
            items.value = res.data.items
            serverItemsLength.value = res.data.total
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}

watch(
    optionsServer,
    async () => {
        await getHistoriPembayaran()
    },
    { deep: true }
)

onMounted(getHistoriPembayaran)
</script>

<template>
    <EasyDataTable
        v-model:server-options="optionsServer"
        :server-items-length="serverItemsLength"
        :headers="headers"
        :items="items"
        :rows-items="[25, 50, 100]"
    >
        <template #item-dibuat_at="{ dibuat_at }">
            {{ tanggal(new Date(dibuat_at + 'Z')) }}
        </template>
        <template #item-dibayar_at="{ dibayar_at }">
            {{ tanggal(new Date(dibayar_at + 'Z')) }}
        </template>
        <template #item-total_dibayar="{ total_dibayar }">
            {{ rupiah(total_dibayar) }}
        </template>
    </EasyDataTable>
</template>
