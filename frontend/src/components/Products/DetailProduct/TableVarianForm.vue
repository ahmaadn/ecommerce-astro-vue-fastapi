<script setup lang="ts">
import type { ClickRowArgument, Header, Item } from 'vue3-easy-data-table'
import type { ProductVariantType } from '@/types'
import Input from '@/components/Form/Input.vue'
import { ref } from 'vue'
import axios from 'axios'
import * as z from 'zod'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { auth } from '@/lib/auth'

const props = defineProps<{ barang_id: Number; list_variant: ProductVariantType[] }>()

const barang_id = props.barang_id
const headers: Header[] = [
    { text: 'ID', value: 'varian_barang_id' },
    { text: 'Ukuran', value: 'ukuran' },
    { text: 'Stok', value: 'stok' },
]

const items = ref<Item[]>(props.list_variant)
const selectedVariant = ref<Number>(0)
const baseurl = `${import.meta.env.PUBLIC_BACKEND_API}/products/${barang_id}/variants`

const showRow = (item: ClickRowArgument) => {
    selectedVariant.value = item.varian_barang_id
    form.setValues({ ukuran: item.ukuran, stok: item.stok })
}

const validationSchema = toTypedSchema(
    z.object({
        ukuran: z.string().min(1),
        stok: z.number().nonnegative(),
    })
)

const form = useForm({ validationSchema })

const handleSubmit = form.handleSubmit(async (values) => {
    if (selectedVariant.value) {
        await onUpdate({ varian_barang_id: selectedVariant.value, ...values })
    } else {
        await onAddVariant(values)
    }
})

const onCancel = () => {
    selectedVariant.value = 0
    form.resetForm()
}

const onDelete = async () => {
    const { httpOptions } = auth.authorize()
    await axios
        .delete(`${baseurl}?varian_id=${selectedVariant.value}`, {
            ...httpOptions,
        })
        .then((res) => {
            selectedVariant.value = 0
            alert('Berhasil di hapus')
        })
        .catch((e) => {
            console.error(e)
        })
    await refreshVariant()
}

const onUpdate = async (values: ProductVariantType) => {
    const { httpOptions } = auth.authorize()
    await axios
        .put(baseurl, values, {
            headers: {
                'Content-Type': 'application/json',
                ...httpOptions.headers,
            },
        })
        .then((res) => {
            alert([JSON.stringify(res.data)])
        })
        .catch((e) => {
            console.error(e)
        })
    await refreshVariant()
}

const onAddVariant = async (values) => {
    const { httpOptions } = auth.authorize()
    await axios
        .post(baseurl, values, {
            headers: {
                'Content-Type': 'application/json',
                ...httpOptions.headers,
            },
        })
        .then((res) => {
            alert([JSON.stringify(res.data)])
        })
        .catch((e) => {
            console.error(e)
        })
    await refreshVariant()
}
const refreshVariant = async () => {
    console.log(baseurl)
    axios.get(baseurl).then((res) => {
        if (res.status == 200) {
            items.value = res.data
        }
    })
}
</script>

<template>
    <div class="w-full md:w-3/4">
        <div class="card bg-base-100 shadow-xl md:mr-6">
            <div class="card-body">
                <h2 class="card-title">Stok Barang</h2>
                <div>Tekan baris untuk edit atau hapus</div>
                <EasyDataTable :headers="headers" :items="items" show-index @click-row="showRow">
                </EasyDataTable>
                <div id="row-clicked"></div>
                <form @submit="handleSubmit">
                    <div class="inline-flex w-full gap-2">
                        <Input name="ukuran" label="ukuran" />
                        <Input name="stok" label="stok" type="number" />
                    </div>
                    <div class="grid w-full grid-cols-3 gap-2" v-if="selectedVariant">
                        <button type="button" id="close" class="btn btn-sm" @click="onCancel">
                            Batalkan
                        </button>
                        <button type="submit" id="simpan" class="btn btn-info btn-sm">
                            Perbaharui
                        </button>
                        <button
                            type="button"
                            id="hapus"
                            class="btn btn-error btn-sm"
                            @click="onDelete"
                        >
                            Hapus
                        </button>
                    </div>
                    <button type="submit" class="btn btn-success btn-sm w-full" v-else>
                        Add variant
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>
