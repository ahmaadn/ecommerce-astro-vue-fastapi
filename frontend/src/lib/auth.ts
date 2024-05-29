import axios, { type AxiosResponse } from 'axios'
import type { JwtPayLoad } from '@/types'
import { jwtDecode } from 'jwt-decode'
import Cookies from 'js-cookie'
import type { AstroGlobal } from 'astro'

const auth = {
    token: (Astro?: AstroGlobal) => {
        if (Astro) {
            return Astro.cookies.get('accessToken')?.value
        }
        return Cookies.get('accessToken')
    },
    authorize: (Astro?: AstroGlobal) => {
        const token = auth.token(Astro)
        if (!token) {
            throw new Error('token login tidak ada')
        }
        return {
            httpOptions: {
                headers: { Authorization: `Bearer ${token}` },
            },
        }
    },
    isLogin: (Astro?: AstroGlobal) => {
        try {
            return auth.token(Astro) ? true : false
        } catch {
            return false
        }
    },
    logOut: (Astro?: AstroGlobal) => {
        if (Astro) {
            Astro.cookies.delete('accessToken', { path: '/' })
            return
        }
        Cookies.remove('accessToken', { path: '/' })
    },
    logIn: async (values: { username: string; password: string }) => {
        return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
            axios
                .post(`${import.meta.env.PUBLIC_BACKEND_API}/auth/token`, values, {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                })
                .then((respones) => {
                    if (respones.status == 200) {
                        const data = respones.data
                        const { access_token } = data
                        Cookies.set('accessToken', access_token, { expires: 7, path: '/' })
                    }
                    resolve(respones)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    register: async (values: {
        name: string
        username: string
        email: string
        password: string
    }) => {
        return new Promise<AxiosResponse<any, any>>((resolve, reject) => {
            axios
                .post(`${import.meta.env.PUBLIC_BACKEND_API}/auth/register`, values, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then((respones) => {
                    resolve(respones)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    payLoad: (Astro?: AstroGlobal) => {
        const token = Astro ? Astro.cookies.get('accessToken')?.value : Cookies.get('accessToken')
        const decodeJwt = jwtDecode<JwtPayLoad>(token)
        return decodeJwt
    },
}

export { Cookies, auth }
