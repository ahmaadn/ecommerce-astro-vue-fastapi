<script setup lang="ts">
import Input from '@/components/Form/Input.vue'
import Textarea from '@/components/Form/Textarea.vue'
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Detail Barang</h2>
            <Input name="nama_barang" label="Nama barang" />
            <Input name="harga" label="Harga barang" type="number" />
            <Textarea name="deskripsi" label="Deskripsi barang"></Textarea>
        </div>
    </div>
</template>
