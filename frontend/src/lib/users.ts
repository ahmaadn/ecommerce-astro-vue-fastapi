import type { AstroGlobal } from 'astro'
import { auth } from './auth'
import type { AxiosResponse } from 'axios'
import axios from 'axios'
import type { UserDetail } from '@/types'

export const users = {
    getDetail: async (Astro: AstroGlobal) => {
        try {
            const { httpOptions } = auth.authorize(Astro)
            const respones = await axios.get(`${import.meta.env.PUBLIC_BACKEND_API}/users/me`, {
                ...httpOptions,
            })
            const data = respones.data
            if (respones.status == 200) {
                return data as UserDetail
            }
            return data
        } catch (e) {
            console.error(e)
        }
    },
}
