<script setup lang="ts">
import { useField, ErrorMessage } from 'vee-validate'
import { defineProps } from 'vue'

const props = defineProps({
    label: String,
    type: String,
    name: {
        type: String,
        required: true,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
})

const { value, errorMessage } = useField(() => props.name, undefined)
</script>

<template>
    <div class="form-control w-full">
        <label class="label" v-if="label">
            <span class="label-text font-semibold">{{ label }}</span>
        </label>
        <input
            :type="type || 'text'"
            :disabled="disabled"
            class="input input-bordered w-full"
            v-model="value"
        />
        <div class="label">
            <span class="label-text-alt text-error">{{ errorMessage }} </span>
        </div>
    </div>
</template>
