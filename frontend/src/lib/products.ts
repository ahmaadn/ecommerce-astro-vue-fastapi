import axios, { type AxiosResponse } from 'axios'
import type { ProductResult, ProductDetailResult, PageResultItems } from '@/types'
import { auth } from './auth'
import type { AstroGlobal } from 'astro'

export const getProducts = async (values: { skip: number; limit: number }) => {
    let baseUrl = `${import.meta.env.PUBLIC_BACKEND_API}/products`

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

export const getAllProducts = async (
    values: {
        q?: 'all' | 'active' | 'daft'
        sort_by?: 'barang_id' | 'nama_barang' | 'harga'
        sort_type?: 'asc' | 'desc'
        page?: number
        size?: number
    },
    Astro?: AstroGlobal
) => {
    const { httpOptions } = auth.authorize(Astro)
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        axios
            .get(`${import.meta.env.PUBLIC_BACKEND_API}/products/all`, {
                params: values,
                timeout: 5000,
                ...httpOptions,
            })
            .then((response) => resolve(response))
            .catch((error) => reject(error))
    })
}

export const getKategories = async () => {
    return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
        axios
            .get(`${import.meta.env.PUBLIC_BACKEND_API}/categories`)
            .then((response) => resolve(response))
            .catch((error) => reject(error))
    })
}
