import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

export function rupiah(value: number) {
    return Intl.NumberFormat('id', { currency: 'IDR', style: 'currency' }).format(value)
}
