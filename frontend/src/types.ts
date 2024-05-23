export interface jwtPayLoad {
    iat: string
    exp: string
    sub: string
    username: string
    permission: string
}

export interface CategoryResult {
    id: number
    name: string
}

export interface ProductSizeResult {
    size: string
    stock: number
}

export interface ProductResult {
    id: number
    create_at: string
    update_at: string
    name: string
    status: 'active' | 'draf' | 'archive'
    description: string
    price: number
    category: CategoryResult
    image: string
}

export interface ProductDetailResult extends ProductResult {
    sizes: ProductSizeResult[]
}
