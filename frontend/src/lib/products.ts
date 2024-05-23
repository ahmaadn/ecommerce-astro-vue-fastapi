import axios from 'axios'
import { type ProductResult } from '@/types'

export const getProducts = async (
    values: {
        skip: number
        limit: number
        query?: 'all' | 'active' | 'daft'
    },
    options?: object
) => {
    if (!options) {
        options = {}
    }

    if (!values.query) {
        values.query = 'active'
    }

    const respones = await axios.get(`${import.meta.env.PUBLIC_BACKEND_API}/products`, {
        params: values,
    })

    const data = await respones.data
    return data as ProductResult[]
}
