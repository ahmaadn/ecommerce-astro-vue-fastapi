<script setup lang="ts">
import { useField } from 'vee-validate'
import { defineProps } from 'vue'

const props = defineProps({
    label: String,
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
        <select class="select select-bordered" v-model="value" :disabled="props.disabled">
            <slot />
        </select>
        <div v-if="errorMessage" class="label">
            <span class="label-text-alt text-error">
                {{ errorMessage }}
            </span>
        </div>
    </div>
</template>
