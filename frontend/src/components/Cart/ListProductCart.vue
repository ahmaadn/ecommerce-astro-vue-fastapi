<script setup lang="ts">
import { auth } from '@/lib/auth'
import type { CartDetailRespones } from '@/types'
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import IncrementButton from './IncrementButton.vue'

const cart_details = ref<CartDetailRespones[]>([])
const totalHarga = ref(0)

const pathImag = import.meta.env.PUBLIC_BACKEND_API

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

onMounted(getKeranjang)

const deleteKeranjang = async (value: Number) => {
    await axios
        .delete(`${import.meta.env.PUBLIC_BACKEND_API}/carts`, {
            params: { keranjang_id: value },
            headers: { ...auth.authorize().httpOptions.headers },
        })
        .then(async (res) => {
            await getKeranjang()
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}

const checkout = () => {
    window.location.href = '/checkout'
}
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Keranjang</h2>
            <div class="text-center" v-if="cart_details.length == 0">
                Kamu tidak mempunyai barang di Keranjang
            </div>

            <div class="h-full divide-y divide-base-300" v-else>
                <!-- LIST PRODUCTS -->
                <div
                    class="flex gap-4 py-8 text-sm text-base-content md:text-base"
                    v-for="(cart, index) in cart_details"
                    v-bind:key="index"
                >
                    <figure class="w-24 flex-none overflow-hidden rounded-lg md:w-36">
                        <img
                            class="transision-transform ratio-1 scale-100 duration-300 group-hover:scale-110"
                            :src="pathImag + '/' + cart.variant_barang.barang.file_gambar"
                            :alt="cart.variant_barang.barang.nama_barang"
                        />
                    </figure>
                    <div class="flex-1">
                        <div class="flex justify-between">
                            <div class="text-bold">
                                {{ cart.variant_barang.barang.nama_barang }}
                            </div>
                            <button
                                class="hover:text-error"
                                @click="deleteKeranjang(cart.keranjang_id)"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="18"
                                    height="18"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        fill="currentColor"
                                        d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"
                                    />
                                </svg>
                            </button>
                        </div>

                        <div class="flex items-center justify-between">
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Variant</span>
                                </label>
                                <input
                                    type="radio"
                                    name="size"
                                    class="btn btn-sm after:text-secondary-content disabled:bg-secondary"
                                    disabled
                                    :value="cart.variant_barang.ukuran"
                                    :aria-label="cart.variant_barang.ukuran"
                                />
                            </div>
                            <IncrementButton
                                client:load
                                :harga="cart.variant_barang.barang.harga"
                                :jumlah="cart.jumlah"
                                :stok="cart.variant_barang.stok"
                                :keranjang_id="cart.keranjang_id"
                                @click="getKeranjang"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div
            class="sticky bottom-0 w-full flex-none rounded-b-box border-t border-base-200 bg-base-100 p-8"
        >
            <div class="inline-flex w-full justify-between text-sm font-semibold md:text-base">
                <p>Sub total</p>
                <p class="text-end">
                    {{
                        Intl.NumberFormat('id', { style: 'currency', currency: 'IDR' }).format(
                            totalHarga
                        )
                    }}
                </p>
            </div>
            <p class="mb-4 text-sm md:text-base">Shipping and taxes calculated at checkout.</p>
            <button
                class="btn btn-primary w-full"
                :disabled="cart_details.length == 0"
                @click="checkout"
            >
                Checkout
            </button>
        </div>
    </div>
</template>
