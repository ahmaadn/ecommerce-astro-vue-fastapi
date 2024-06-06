<script setup lang="ts">
import type { CartDetailRespones } from '@/types'
import { auth } from '@/lib/auth'
import axios from 'axios'
import { onMounted, ref, watch } from 'vue'

const ongkir = defineModel<Number>('ongkir')
const cart_details = ref<CartDetailRespones[]>([])
const totalHarga = ref(0)

const getKeranjang = async () => {
    await axios
        .get(`${import.meta.env.PUBLIC_BACKEND_API}/carts`, auth.authorize().httpOptions)
        .then((res) => {
            cart_details.value = res.data
            totalHarga.value = cart_details.value
                .map((value) => value.jumlah * value.variant_barang.barang.harga)
                .reduce((prev, next) => prev + next)
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
    await getKeranjang()
})
</script>

<template>
    <div class="card h-fit max-w-sm bg-base-100">
        <div class="card-body">
            <div class="card-title pb-2">Ringkasan pesanan</div>
            <div class="grid grid-cols-3 text-sm" v-for="(cart, index) in cart_details">
                <p>
                    {{ cart.variant_barang.barang.nama_barang }} ({{ cart.variant_barang.ukuran }})
                </p>
                <span class="text-center">{{ cart.jumlah }}x</span>
                <span class="text-end">{{
                    Intl.NumberFormat('id', { style: 'currency', currency: 'IDR' }).format(
                        cart.variant_barang.barang.harga * cart.jumlah
                    )
                }}</span>
            </div>
            <div class="inline-flex">
                <p>Ongkir</p>
                <span class="text-end">{{
                    Intl.NumberFormat('id', { style: 'currency', currency: 'IDR' }).format(ongkir)
                }}</span>
            </div>
            <div class="divider"></div>
            <div class="inline-flex font-semibold">
                <p>Total</p>
                <span class="text-end">{{
                    Intl.NumberFormat('id', { style: 'currency', currency: 'IDR' }).format(
                        totalHarga + ongkir
                    )
                }}</span>
            </div>
        </div>
    </div>
</template>
