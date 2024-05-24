import axios from 'axios'
import type { ProductResult, ProductDetailResult } from '@/types'

export const getProducts = async (
    values: {
        skip: number
        limit: number
        q?: 'all' | 'active' | 'daft'
    },
    options?: object
) => {
    let baseUrl = `${import.meta.env.PUBLIC_BACKEND_API}/products`
    if (!options) {
        options = {}
    }

    if (values.q) {
        baseUrl = `${baseUrl}/all`
    }

    const respones = await axios.get(baseUrl, {
        params: values,
    })

    const data = await respones.data
    return data as ProductResult[]
}

export const getProductByID = async (id: number) => {
    try {
        const respones = await axios.get(`${import.meta.env.PUBLIC_BACKEND_API}/products/${id}`)
        const data = await respones.data
        if (respones.status) {
            return data as ProductDetailResult
        }
        return null
    } catch (e) {
        console.error(e)
        return null
    }
}
