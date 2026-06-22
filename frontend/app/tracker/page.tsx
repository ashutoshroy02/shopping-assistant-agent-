"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { useAuth } from "@/hooks/useAuth"
import { formatCurrency, formatDate } from "@/lib/utils"
import { TrendingDown, TrendingUp, Minus, Trash2 } from "lucide-react"

interface TrackedProduct {
  id: string
  product_id: string
  target_price: number
  current_price: number
  status: string
  created_at: string
}

export default function TrackerPage() {
  const { token } = useAuth()
  const [tracked, setTracked] = useState<TrackedProduct[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (token) {
      fetchTracked()
    }
  }, [token])

  const fetchTracked = async () => {
    if (!token) return
    setIsLoading(true)
    try {
      const data = await api.tracker.list(token)
      setTracked(data as TrackedProduct[])
    } catch (error) {
      console.error("Failed to fetch tracked products:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRemove = async (productId: string) => {
    if (!token) return
    try {
      await api.tracker.remove(productId, token)
      setTracked((prev) => prev.filter((t) => t.product_id !== productId))
    } catch (error) {
      console.error("Failed to remove tracking:", error)
    }
  }

  const getPriceStatus = (current: number, target: number) => {
    if (current <= target) {
      return { icon: <TrendingDown className="w-4 h-4 text-green-500" />, text: "Below target!", color: "text-green-500" }
    }
    const diff = ((current - target) / target) * 100
    if (diff < 10) {
      return { icon: <Minus className="w-4 h-4 text-yellow-500" />, text: `Almost there (${diff.toFixed(0)}% away)`, color: "text-yellow-500" }
    }
    return { icon: <TrendingUp className="w-4 h-4 text-red-500" />, text: `${diff.toFixed(0)}% above target`, color: "text-red-500" }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <TrendingDown className="w-6 h-6" />
        Price Tracker
      </h1>

      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground">Loading...</div>
      ) : tracked.length === 0 ? (
        <div className="text-center py-12">
          <TrendingDown className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No products being tracked</p>
          <a href="/products" className="text-primary hover:underline mt-2 inline-block">
            Browse products to start tracking
          </a>
        </div>
      ) : (
        <div className="space-y-4">
          {tracked.map((item) => {
            const status = getPriceStatus(item.current_price, item.target_price)
            return (
              <div key={item.id} className="border rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {status.icon}
                      <span className={`text-sm font-medium ${status.color}`}>
                        {status.text}
                      </span>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Current Price</p>
                        <p className="font-semibold">{formatCurrency(item.current_price)}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Target Price</p>
                        <p className="font-semibold">{formatCurrency(item.target_price)}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Tracking Since</p>
                        <p className="font-semibold">{formatDate(item.created_at)}</p>
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleRemove(item.product_id)}
                    className="p-2 text-muted-foreground hover:text-destructive"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
