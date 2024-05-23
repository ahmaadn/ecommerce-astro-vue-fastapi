<script setup lang="ts">
const props = defineProps<{
    sizes?: { size: string; stock: number }[]
}>()
</script>
<template>
    <form class="space-y-4">
        <fieldset v-if="props.sizes && props.sizes.length >= 2">
            <div class="inline-flex gap-4">
                <input
                    v-for="(size, index) in props.sizes"
                    v-bind:key="index"
                    type="radio"
                    name="size-choice"
                    class="btn btn-sm w-8 min-w-8"
                    :id="size.size"
                    :value="size.size"
                    :aria-label="size.size"
                    :disabled="size.stock == 0"
                    :checked="index == 0"
                />
            </div>
        </fieldset>
        <button
            type="submit"
            class="btn btn-secondary w-full"
            :disabled="props.sizes && props.sizes.length == 2 && props.sizes[0].stock == 0"
        >
            ADD TO BAG
        </button>
    </form>
</template>
