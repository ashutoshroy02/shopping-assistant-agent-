import Link from "next/link"
import { MessageCircle, Search, TrendingDown, BarChart3 } from "lucide-react"

const features = [
  {
    icon: MessageCircle,
    title: "AI Chat",
    description: "Ask questions in natural language and get instant product recommendations",
    href: "/chat",
  },
  {
    icon: Search,
    title: "Product Search",
    description: "Browse and filter products across categories with smart search",
    href: "/products",
  },
  {
    icon: TrendingDown,
    title: "Price Tracking",
    description: "Track prices and get alerts when they drop to your target",
    href: "/tracker",
  },
  {
    icon: BarChart3,
    title: "Analytics",
    description: "View your search trends, saved products, and insights",
    href: "/analytics",
  },
]

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold mb-4">
          AI Shopping Assistant
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Your intelligent shopping companion. Get personalized recommendations,
          compare products, track prices, and find the best deals.
        </p>
        <div className="mt-8 flex gap-4 justify-center">
          <Link
            href="/chat"
            className="px-8 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90"
          >
            Start Chatting
          </Link>
          <Link
            href="/products"
            className="px-8 py-3 border rounded-lg font-medium hover:bg-muted"
          >
            Browse Products
          </Link>
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature) => (
          <Link
            key={feature.title}
            href={feature.href}
            className="border rounded-lg p-6 hover:shadow-lg transition-shadow"
          >
            <feature.icon className="w-10 h-10 mb-4 text-primary" />
            <h3 className="font-semibold mb-2">{feature.title}</h3>
            <p className="text-sm text-muted-foreground">
              {feature.description}
            </p>
          </Link>
        ))}
      </div>

      <div className="mt-16 bg-muted rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-4">Example Queries</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {[
            "Find the best gaming laptop under ₹1,00,000",
            "Compare iPhone 15 and Samsung S24",
            "Best monitor for programming under ₹20,000",
            "Recommend a DSLR camera for beginners",
          ].map((query) => (
            <Link
              key={query}
              href={`/chat?q=${encodeURIComponent(query)}`}
              className="p-4 bg-background rounded-lg hover:shadow-md transition-shadow text-sm"
            >
              "{query}"
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
