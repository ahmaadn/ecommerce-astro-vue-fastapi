export interface jwtPayLoad {
    iat: string
    exp: string
    sub: string
    username: string
    permission: string
}

export interface CategoryResult {
    kategori_id: number
    nama_kategori: string
}

export interface ProductSizeResult {
    varian_barang_id: number
    ukuram: string
    stok: number
}

export interface ProductResult {
    barang_id: number
    // create_at: string
    // update_at: string
    nama_barang: string
    // status: 'active' | 'draf'
    deskripsi: string
    harga: number
    kategori: CategoryResult
    file_gambar: string
}

export interface ProductDetailResult extends ProductResult {
    list_varian: ProductSizeResult[]
}
