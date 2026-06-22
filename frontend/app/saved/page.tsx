"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { useAuth } from "@/hooks/useAuth"
import { formatCurrency, formatDate } from "@/lib/utils"
import { Heart, Trash2 } from "lucide-react"

interface SavedProduct {
  id: string
  title: string
  price: number
  rating?: number
  brand: string
  category: string
  saved_at: string
}

export default function SavedPage() {
  const { token } = useAuth()
  const [products, setProducts] = useState<SavedProduct[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (token) {
      fetchSaved()
    }
  }, [token])

  const fetchSaved = async () => {
    if (!token) return
    setIsLoading(true)
    try {
      const data = await api.saved.list(token)
      setProducts(data.products as SavedProduct[])
    } catch (error) {
      console.error("Failed to fetch saved products:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRemove = async (productId: string) => {
    if (!token) return
    try {
      await api.saved.remove(productId, token)
      setProducts((prev) => prev.filter((p) => p.id !== productId))
    } catch (error) {
      console.error("Failed to remove product:", error)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Heart className="w-6 h-6" />
        Saved Products
      </h1>

      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground">Loading...</div>
      ) : products.length === 0 ? (
        <div className="text-center py-12">
          <Heart className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No saved products yet</p>
          <a href="/products" className="text-primary hover:underline mt-2 inline-block">
            Browse products
          </a>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {products.map((product) => (
            <div key={product.id} className="border rounded-lg p-4">
              <div className="aspect-square bg-muted rounded-md mb-3 flex items-center justify-center">
                <span className="text-4xl">📦</span>
              </div>
              <h3 className="font-medium line-clamp-2 mb-2">{product.title}</h3>
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold">{formatCurrency(product.price)}</span>
                {product.rating && (
                  <span className="text-sm text-muted-foreground">⭐ {product.rating}</span>
                )}
              </div>
              <p className="text-xs text-muted-foreground mb-3">
                Saved {formatDate(product.saved_at)}
              </p>
              <div className="flex gap-2">
                <a
                  href={`/products/${product.id}`}
                  className="flex-1 px-3 py-1 text-center text-sm border rounded hover:bg-muted"
                >
                  View
                </a>
                <button
                  onClick={() => handleRemove(product.id)}
                  className="px-3 py-1 text-sm text-destructive border border-destructive rounded hover:bg-destructive hover:text-destructive-foreground"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
