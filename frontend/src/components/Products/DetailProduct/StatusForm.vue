<script setup>
import Select from '@/components/Form/Select.vue'
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Status Barang</h2>
            <Select label="Status" name="status">
                <option value="active">Active</option>
                <option value="draft">Draft</option>
            </Select>
        </div>
    </div>
</template>
