export interface JwtPayLoad {
    iat: string
    exp: string
    sub: string
    username: string
    permission: 'admin' | 'user'
}

export interface CategoryResult {
    kategori_id: number
    nama_kategori: string
}

export interface ProductVariantType {
    varian_barang_id: number
    ukuran: string
    stok: number
}

export interface ProductResult {
    barang_id: number
    nama_barang: string
    deskripsi: string
    harga: number
    kategori: CategoryResult
    file_gambar: string
    dibuat_at: Date
    diupdate_at: Date
    status: 'active' | 'draft'
}

export interface ProductDetailResult extends ProductResult {
    list_varian: ProductVariantType[]
}

export interface UserDetail {
    nama: string
    username: string
    email: string
    no_hp: string
    is_aktif: boolean
    role: 'admin' | 'user'
    dibuat_at: Date
    diupdate_at: Date
}

export interface SidebarItem {
    name: string
    url?: string
    icon?: string
    permission?: 'admin' | 'user'
}

export interface PageResultItems<T> {
    items: T[]
    total: number
    page: number
    size: number
    pages: number
}

export interface CartDetailRespones {
    keranjang_id: number
    varian_barang_id: number
    jumlah: number
    variant_barang: {
        varian_barang_id: number
        ukuran: string
        stok: number
        barang: ProductResult
    }
}
