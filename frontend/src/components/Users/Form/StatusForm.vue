<script setup lang="ts">
import Select from '@/components/Form/Select.vue'
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Status User</h2>
            <Select name="is_aktif" label="Status">
                <option :value="false">Tidak Aktif</option>
                <option :value="true">Active</option>
            </Select>
        </div>
    </div>
</template>
