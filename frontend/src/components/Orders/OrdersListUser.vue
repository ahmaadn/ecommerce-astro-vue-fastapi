<script setup lang="ts">
import { auth } from '@/lib/auth'
import { rupiah, tanggal } from '@/lib/utils'
import axios from 'axios'
import { onMounted, ref, defineProps, watch } from 'vue'
import type { Header, Item, ClickRowArgument, ServerOptions } from 'vue3-easy-data-table'
import type { PesananRespones } from '@/types'

const props = defineProps({
    permission: {
        type: String,
    },
})

const permission = ref(props.permission)
const serverItemsLength = ref(0)
const optionsServer = ref<ServerOptions>({
    page: 1,
    rowsPerPage: 25,
})

const selectedPesanan = ref<PesananRespones>()
const headers: Header[] = [
    { text: 'ID Pesanan', value: 'pesanan_id' },
    { text: 'Total harga', value: 'total_harga', width: 300 },
    { text: 'ongkir', value: 'ongkir' },
    { text: 'Status', value: 'status' },
    { text: 'dibuat', value: 'dibuat_at' },
]
const items = ref<Item[]>([])

const getPesanan = async () => {
    const options = optionsServer.value
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/orders`, {
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
}

const showRow = (item: ClickRowArgument) => {
    selectedPesanan.value = items.value.find((value) => value.pesanan_id == item.pesanan_id)
}

const onClickBtn = async (value: String) => {
    await axios
        .put(
            `${import.meta.env.PUBLIC_BACKEND_API}/orders/order/${value}`,
            {},
            {
                params: {
                    pesanan_id: selectedPesanan.value?.pesanan_id,
                },
                ...auth.authorize().httpOptions,
            }
        )
        .then(async (res) => {
            alert(res.data.detail)
            await getPesanan()
            selectedPesanan.value = undefined
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}

watch(optionsServer, getPesanan)
onMounted(getPesanan)
</script>

<template>
    <EasyDataTable
        v-model:server-options="optionsServer"
        :server-items-length="serverItemsLength"
        :headers="headers"
        :items="items"
        :rows-items="[25, 50, 100]"
        @click-row="showRow"
    >
        <template #item-dibuat_at="{ dibuat_at }">
            {{ tanggal(new Date(dibuat_at + 'Z')) }}
        </template>
        <template #item-total_harga="{ total_harga }">
            {{ rupiah(total_harga) }}
        </template>
        <template #item-ongkir="{ ongkir }">
            {{ rupiah(ongkir) }}
        </template>
    </EasyDataTable>

    <div v-if="selectedPesanan">
        <div class="card-title pb-2">Ringkasan pesanan</div>
        <div
            class="grid grid-cols-3 text-sm"
            v-for="(pesanan, index) in selectedPesanan.details_pesanan"
            v-bind:key="index"
        >
            <p>
                {{ pesanan.varian_barang.barang.nama_barang }} ({{ pesanan.varian_barang.ukuran }})
            </p>
            <span class="text-center">{{ pesanan.jumlah_pesanan }}x</span>
            <span class="text-end">{{ rupiah(pesanan.harga_pesanan) }}</span>
        </div>
        <div class="inline-flex w-full text-sm">
            <p>Ongkir</p>
            <span class="text-end">{{ rupiah(selectedPesanan.ongkir) }}</span>
        </div>
        <div class="divider"></div>
        <div class="inline-flex w-full font-semibold">
            <p>Total</p>
            <span class="text-end">{{ rupiah(selectedPesanan.total_harga) }}</span>
        </div>
        <div>
            Status
            <span class="text-underline">{{ selectedPesanan.status }}</span>
        </div>

        <!-- shipped -->
        <button
            v-if="permission == 'admin' && selectedPesanan.status == 'paid'"
            class="btn btn-secondary btn-sm my-4 w-full"
            @click="onClickBtn('shipped')"
        >
            Kirim Pesanan
        </button>

        <!-- completed  -->
        <button
            v-if="permission == 'user' && selectedPesanan.status == 'shipped'"
            class="btn btn-secondary btn-sm my-4 w-full"
            @click="onClickBtn('completed')"
        >
            Terima Pesanan
        </button>
    </div>
</template>
