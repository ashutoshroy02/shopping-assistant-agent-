"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { useAuth } from "@/hooks/useAuth"
import { BarChart3, Search, Heart, MessageCircle, TrendingUp } from "lucide-react"

interface Analytics {
  user_analytics: {
    total_searches: number
    saved_products: number
    total_chats: number
    tracked_products: number
    categories_viewed: string[]
  }
  platform_analytics: {
    total_users: number
    total_products: number
    total_recommendations: number
    popular_categories: { name: string; count: number }[]
    top_rated_products: { id: string; title: string; rating: number; price: number }[]
  }
}

export default function AnalyticsPage() {
  const { token } = useAuth()
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [period, setPeriod] = useState("30d")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [period])

  const fetchAnalytics = async () => {
    setIsLoading(true)
    try {
      const data = await api.analytics.get(period, token || undefined)
      setAnalytics(data as Analytics)
    } catch (error) {
      console.error("Failed to fetch analytics:", error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12 text-muted-foreground">Loading analytics...</div>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12 text-muted-foreground">Failed to load analytics</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <BarChart3 className="w-6 h-6" />
          Analytics
        </h1>
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="px-3 py-2 border rounded-lg"
        >
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          icon={<Search className="w-5 h-5" />}
          label="Total Searches"
          value={analytics.user_analytics.total_searches}
        />
        <StatCard
          icon={<Heart className="w-5 h-5" />}
          label="Saved Products"
          value={analytics.user_analytics.saved_products}
        />
        <StatCard
          icon={<MessageCircle className="w-5 h-5" />}
          label="Chat Sessions"
          value={analytics.user_analytics.total_chats}
        />
        <StatCard
          icon={<TrendingUp className="w-5 h-5" />}
          label="Tracked Products"
          value={analytics.user_analytics.tracked_products}
        />
      </div>

      {analytics.user_analytics.categories_viewed.length > 0 && (
        <div className="border rounded-lg p-6 mb-6">
          <h2 className="font-semibold mb-4">Categories You&apos;ve Explored</h2>
          <div className="flex flex-wrap gap-2">
            {analytics.user_analytics.categories_viewed.map((cat) => (
              <span key={cat} className="px-3 py-1 bg-muted rounded-full text-sm">
                {cat}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="border rounded-lg p-6">
          <h2 className="font-semibold mb-4">Popular Categories</h2>
          {analytics.platform_analytics.popular_categories.length > 0 ? (
            <div className="space-y-3">
              {analytics.platform_analytics.popular_categories.map((cat) => (
                <div key={cat.name} className="flex items-center justify-between">
                  <span className="text-sm">{cat.name}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary"
                        style={{
                          width: `${(cat.count / analytics.platform_analytics.total_products) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-sm text-muted-foreground w-8 text-right">
                      {cat.count}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No data available</p>
          )}
        </div>

        <div className="border rounded-lg p-6">
          <h2 className="font-semibold mb-4">Top Rated Products</h2>
          {analytics.platform_analytics.top_rated_products.length > 0 ? (
            <div className="space-y-3">
              {analytics.platform_analytics.top_rated_products.map((product) => (
                <div key={product.id} className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{product.title}</p>
                    <p className="text-xs text-muted-foreground">
                      ₹{product.price.toLocaleString("en-IN")}
                    </p>
                  </div>
                  <span className="text-sm text-yellow-600">⭐ {product.rating}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No data available</p>
          )}
        </div>
      </div>

      <div className="border rounded-lg p-6 mt-6">
        <h2 className="font-semibold mb-4">Platform Stats</h2>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold">{analytics.platform_analytics.total_users}</p>
            <p className="text-sm text-muted-foreground">Total Users</p>
          </div>
          <div>
            <p className="text-2xl font-bold">{analytics.platform_analytics.total_products}</p>
            <p className="text-sm text-muted-foreground">Products</p>
          </div>
          <div>
            <p className="text-2xl font-bold">{analytics.platform_analytics.total_recommendations}</p>
            <p className="text-sm text-muted-foreground">Recommendations</p>
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: number }) {
  return (
    <div className="border rounded-lg p-4">
      <div className="flex items-center gap-2 text-muted-foreground mb-2">
        {icon}
        <span className="text-sm">{label}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  )
}
