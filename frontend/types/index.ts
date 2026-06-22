export interface User {
  id: string
  name: string
  email: string
  role: string
  preferences: Record<string, unknown>
  created_at: string
}

export interface Product {
  id: string
  title: string
  description?: string
  price: number
  original_price?: number
  rating?: number
  review_count?: number
  category: string
  brand: string
  specifications: Record<string, string>
  images: string[]
  availability: boolean
}

export interface ChatMessage {
  id: string
  role: "user" | "assistant"
  content: string
  metadata?: Record<string, unknown>
  timestamp: string
}

export interface ChatSession {
  id: string
  title?: string
  created_at: string
  updated_at: string
}

export interface Recommendation {
  product_id: string
  title: string
  price: number
  rating?: number
  score: number
  reasoning: string
  pros?: string[]
  cons?: string[]
}

export interface PriceHistory {
  price: number
  source: string
  timestamp: string
}

export interface PriceStatistics {
  current: number
  lowest: number
  highest: number
  average: number
  trend: "increasing" | "decreasing" | "stable"
}

export interface PriceTracking {
  id: string
  product_id: string
  target_price: number
  current_price?: number
  status: string
  created_at: string
}

export interface SavedProduct {
  id: string
  title: string
  price: number
  rating?: number
  brand: string
  category: string
  saved_at: string
}

export interface Analytics {
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
    top_rated_products: Product[]
  }
}

export interface Comparison {
  products: Product[]
  feature_comparison: Record<string, Record<string, string>>
  analysis: {
    winner: string
    reasoning: string
  }
}
