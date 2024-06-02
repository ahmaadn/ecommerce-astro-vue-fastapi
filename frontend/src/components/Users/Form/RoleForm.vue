<script setup lang="ts">
import Select from '@/components/Form/Select.vue'
</script>

<template>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Role User</h2>
            <Select name="role" label="Role">
                <option value="admin">admin</option>
                <option value="user">user</option>
            </Select>
        </div>
    </div>
</template>
