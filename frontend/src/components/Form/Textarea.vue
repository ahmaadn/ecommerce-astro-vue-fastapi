<script setup lang="ts">
import { useField, ErrorMessage } from 'vee-validate'
import { defineProps } from 'vue'

const props = defineProps({
    label: {
        type: String,
    },
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
        <label class="label" v-if="props.label">
            <span class="label-text font-semibold">{{ props.label }}</span>
        </label>
        <textarea
            class="textarea textarea-bordered h-24"
            v-model="value"
            :disabled="props.disabled"
        >
        </textarea>
        <div class="label">
            <span class="label-text-alt text-error">{{ errorMessage }} </span>
        </div>
    </div>
</template>
