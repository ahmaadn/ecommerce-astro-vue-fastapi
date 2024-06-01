<script lang="ts" setup>
import Select from '@/components/Form/Select.vue'
import { getKategories } from '@/lib/products'
import { ref, onMounted } from 'vue'

const kategories = ref<
    {
        kategori_id: Number
        nama_kategori: String
    }[]
>([])

onMounted(async () => {
    await getKategories()
        .then((res) => {
            if (res.status == 200) {
                const data = res.data
                kategories.value = data
            }
        })
        .catch((e) => console.error(e))
})
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Kategori Barang</h2>
            <Select label="Kategori" name="kategori_id">
                <option
                    v-for="(kategori, index) in kategories"
                    v-bind:key="index"
                    :value="kategori.kategori_id"
                >
                    {{ kategori.nama_kategori }}
                </option>
            </Select>
        </div>
    </div>
</template>
