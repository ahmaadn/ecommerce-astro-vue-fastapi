<script setup lang="ts">
import axios from 'axios'
import { auth } from '@/lib/auth'
import { computed, toRef } from 'vue'

const props = defineProps<{
    harga: Number
    jumlah: Number
    stok: Number
    keranjang_id: Number
}>()

const emit = defineEmits(['click'])

const jumlah = toRef(props.jumlah)
const harga = toRef(props.harga)
const stok = toRef(props.stok)

const updateJumlah = async (value: Number) => {
    jumlah.value = jumlah.value + value

    axios.put(
        `${import.meta.env.PUBLIC_BACKEND_API}/carts`,
        {
            keranjang_id: props.keranjang_id,
            jumlah: jumlah.value,
        },
        {
            headers: {
                'Content-Type': 'application/json',
                ...auth.authorize().httpOptions.headers,
            },
        }
    )

    emit('click')
}

const totalHarga = computed(() => harga.value * jumlah.value)
</script>

<template>
    <div class="flex items-center justify-end gap-10">
        <div class="inline-flex items-center gap-2 border border-base-200 p-2">
            <button class="btn btn-circle btn-xs" :disabled="jumlah == 1" @click="updateJumlah(-1)">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19 13H5v-2h14z" />
                </svg>
            </button>
            <span>{{ jumlah }}</span>
            <button
                class="btn btn-circle btn-xs"
                :disabled="jumlah >= stok"
                @click="updateJumlah(1)"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6z" />
                </svg>
            </button>
        </div>
        <div class="font-xl">
            {{ Intl.NumberFormat('id', { style: 'currency', currency: 'IDR' }).format(totalHarga) }}
        </div>
    </div>
</template>
