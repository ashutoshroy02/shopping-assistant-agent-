"use client"

import Link from "next/link"
import { cn, formatCurrency } from "@/lib/utils"
import { Star } from "lucide-react"

interface ProductCardProps {
  product: Record<string, string>
  compact?: boolean
}

export function ProductCard({ product, compact }: ProductCardProps) {
  return (
    <Link href={`/products/${product.id}`}>
      <div
        className={cn(
          "border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer",
          compact && "p-3"
        )}
      >
        <div className="aspect-square bg-muted rounded-md mb-3 flex items-center justify-center">
          <span className="text-4xl">📦</span>
        </div>
        <h3
          className={cn(
            "font-medium line-clamp-2 mb-1",
            compact ? "text-sm" : "text-base"
          )}
        >
          {product.title}
        </h3>
        <div className="flex items-center gap-2 mb-2">
          {product.rating && (
            <div className="flex items-center gap-1 text-sm">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              <span>{product.rating}</span>
            </div>
          )}
          {product.brand && (
            <span className="text-xs text-muted-foreground">{product.brand}</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className={cn("font-bold", compact ? "text-sm" : "text-lg")}>
            {formatCurrency(product.price)}
          </span>
          {product.original_price &&
            Number(product.original_price) > Number(product.price) && (
              <span className="text-sm text-muted-foreground line-through">
                {formatCurrency(Number(product.original_price))}
              </span>
            )}
        </div>
      </div>
    </Link>
  )
}
