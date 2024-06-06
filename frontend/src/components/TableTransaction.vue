<script setup lang="ts">
import { auth } from '@/lib/auth'
import { onMounted, ref, defineProps } from 'vue'
import type { Header, Item, ClickRowArgument } from 'vue3-easy-data-table'
import { rupiah } from '@/lib/utils'
import axios from 'axios'
const props = defineProps({
    permission: {
        type: String,
    },
})
const permission = ref(props.permission)
const headers: Header[] = [
    { text: 'ID Transaksi', value: 'pembayaran_id' },
    { text: 'ID Pemesanan', value: 'pesanan_id' },
    { text: 'ID User', value: 'pesanan.user_id' },
    { text: 'Total Dibayar', value: 'total_dibayar' },
    { text: 'Status', value: 'status_bayar' },
    { text: 'dibuat', value: 'dibuat_at' },
    { text: 'dibayar', value: 'dibuat_at' },
]
const items = ref<Item[]>([])

const getHistoriPembayaran = async () => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/payments`, { ...auth.authorize().httpOptions })
        .then((res) => {
            items.value = res.data.items
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
    await getHistoriPembayaran()
})
</script>

<template>
    <EasyDataTable :headers="headers" :items="items">
        <template #item-total_dibayar="{ total_dibayar }">
            {{ rupiah(total_dibayar) }}
        </template>
    </EasyDataTable>
</template>
