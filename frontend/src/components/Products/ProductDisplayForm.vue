<script setup lang="ts">
import type { ProductVariantType } from '@/types'

const props = defineProps<{
    varians: ProductVariantType[]
}>()
</script>
<template>
    <form class="space-y-4">
        <fieldset v-if="props.varians && props.varians.length >= 2">
            <div class="inline-flex gap-4">
                <input
                    v-for="(varian, index) in props.varians"
                    v-bind:key="index"
                    type="radio"
                    name="size-choice"
                    class="btn btn-sm w-8 min-w-8"
                    :id="varian.varian_barang_id.toString()"
                    :value="varian.varian_barang_id.toString()"
                    :aria-label="varian.ukuran"
                    :disabled="varian.stok == 0"
                    :checked="index == 0"
                />
            </div>
        </fieldset>
        <button
            type="submit"
            class="btn btn-secondary w-full text-base font-bold"
            :disabled="props.varians && props.varians.length == 2 && props.varians[0].stok == 0"
        >
            Masukan ke keranjang
        </button>
    </form>
</template>
