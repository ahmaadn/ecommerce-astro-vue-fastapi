<script setup lang="ts">
import { auth } from '@/lib/auth'
import type { ProductVariantType } from '@/types'
import axios from 'axios'
import { onMounted, ref } from 'vue'

const props = defineProps<{
    barang_id: Number
    variants: ProductVariantType[]
}>()

const barang_id = props.barang_id
const variants = props.variants
const variant_id_choice = ref(0)
const disabled = ref(variants.length == 0)

const onClick = (e: any) => {
    const variant = variants.find(
        (value) => value.varian_barang_id == e.target.value
    ) as ProductVariantType
    if (variant.stok == 0) {
        disabled.value = true
    } else {
        disabled.value = false
    }
}

const handleSubmit = async () => {
    if (!auth.isLogin()) {
        alert('Kamu Harus Login terlebih dahulu untuk memasukkan barang ke keranjang')
        window.location.href = '/signin'
        return
    }
    if (variant_id_choice.value == 0 && variants.length >= 1) {
        alert('Pilih setidaknya 1 barang')
        return
    }
    await axios
        .post(
            `${import.meta.env.PUBLIC_BACKEND_API}/carts`,
            {
                barang_id: barang_id,
                varian_barang_id: variant_id_choice.value,
                jumlah: 1,
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    ...auth.authorize().httpOptions.headers,
                },
            }
        )
        .then((res) => {
            alert('Berhasil menambahkan ke keranjang')
        })
        .catch((e) => {
            if (e.response) {
                alert(e.response.data.detail)
            } else {
                console.error(e)
            }
        })
}

onMounted(() => {
    if (variants.length == 1) {
        const variant = variants[0]
        variant_id_choice.value = variant.varian_barang_id
    }
})
</script>
<template>
    <form class="space-y-4">
        <fieldset v-if="variants && variants.length >= 2">
            <div class="inline-flex gap-4">
                <input
                    v-for="(varian, index) in variants"
                    v-bind:key="index"
                    type="radio"
                    name="size"
                    class="btn btn-sm w-8 min-w-8"
                    :value="varian.varian_barang_id.toString()"
                    :aria-label="varian.ukuran"
                    v-model="variant_id_choice"
                    @click="onClick"
                />
            </div>
        </fieldset>
        <button
            type="submit"
            class="btn btn-secondary w-full"
            :disabled="disabled"
            @click="handleSubmit"
        >
            Masukan ke keranjang
        </button>
    </form>
</template>
