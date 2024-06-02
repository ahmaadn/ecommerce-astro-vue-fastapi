<script setup lang="ts">
import Input from '@/components/Form/Input.vue'
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Detail User</h2>
            <Input name="nama" label="Nama Lengkap" />
            <Input name="username" label="Username" />
            <Input name="email" label="Email" type="email" />
            <Input name="no_hp" label="Nomer handphone" />
        </div>
    </div>
</template>
