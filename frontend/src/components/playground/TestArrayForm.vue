<script setup>
import { Form, FieldArray, Field } from 'vee-validate'

const initialValues = {
    links: ['https://github.com/logaretm'],
}
function onSubmit(values) {
    alert(JSON.stringify(values, null, 2))
}
</script>
<template>
    <Form @submit="onSubmit" :initial-values="initialValues">
        <FieldArray name="links" v-slot="{ fields, push, remove }">
            <div v-for="(entry, idx) in fields" :key="entry.key">
                <Field :name="`links[${idx}]`" type="url" />
                <button type="button" @click="remove(idx)">Remove</button>
            </div>
            <button type="button" @click="push('')">Add</button>
        </FieldArray>
        <button>Submit</button>
    </Form>
</template>
