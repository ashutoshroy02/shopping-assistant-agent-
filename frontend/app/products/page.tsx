"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { ProductCard } from "@/components/products/ProductCard"
import { Search, Filter } from "lucide-react"

interface Product {
  id: string
  title: string
  price: number
  original_price?: number
  rating?: number
  category: string
  brand: string
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<{ name: string; count: number }[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>("")
  const [searchQuery, setSearchQuery] = useState("")
  const [sortBy, setSortBy] = useState("rating")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchProducts()
    fetchCategories()
  }, [selectedCategory, sortBy])

  const fetchProducts = async () => {
    setIsLoading(true)
    try {
      const params: Record<string, string> = { sort_by: sortBy, limit: "50" }
      if (selectedCategory) params.category = selectedCategory
      if (searchQuery) params.search = searchQuery

      const data = await api.products.list(params)
      setProducts(data as Product[])
    } catch (error) {
      console.error("Failed to fetch products:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchCategories = async () => {
    try {
      const data = await api.products.categories()
      setCategories(data.categories as { name: string; count: number }[])
    } catch (error) {
      console.error("Failed to fetch categories:", error)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchProducts()
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Products</h1>

      <div className="flex flex-col md:flex-row gap-6">
        <aside className="w-full md:w-64 shrink-0">
          <div className="border rounded-lg p-4">
            <h2 className="font-medium mb-4 flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Categories
            </h2>
            <div className="space-y-2">
              <button
                onClick={() => setSelectedCategory("")}
                className={`block w-full text-left px-2 py-1 rounded text-sm ${
                  !selectedCategory ? "bg-primary text-primary-foreground" : "hover:bg-muted"
                }`}
              >
                All Categories
              </button>
              {categories.map((cat) => (
                <button
                  key={cat.name}
                  onClick={() => setSelectedCategory(cat.name)}
                  className={`block w-full text-left px-2 py-1 rounded text-sm ${
                    selectedCategory === cat.name
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-muted"
                  }`}
                >
                  {cat.name} ({cat.count})
                </button>
              ))}
            </div>
          </div>
        </aside>

        <div className="flex-1">
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <form onSubmit={handleSearch} className="flex-1 flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search products..."
                  className="w-full pl-10 pr-4 py-2 border rounded-lg"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
              >
                Search
              </button>
            </form>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border rounded-lg"
            >
              <option value="rating">Sort by Rating</option>
              <option value="price">Sort by Price</option>
              <option value="newest">Sort by Newest</option>
            </select>
          </div>

          {isLoading ? (
            <div className="text-center py-12 text-muted-foreground">Loading products...</div>
          ) : products.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">No products found</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {products.map((product) => (
                <ProductCard key={product.id} product={product as unknown as Record<string, string>} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
