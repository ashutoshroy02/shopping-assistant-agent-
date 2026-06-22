"use client"

import { useState, useRef, useEffect } from "react"
import { api } from "@/lib/api"
import { useAuth } from "@/hooks/useAuth"
import { ChatMessage } from "@/components/chat/ChatMessage"
import { ChatInput } from "@/components/chat/ChatInput"
import { ProductCard } from "@/components/products/ProductCard"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  products?: unknown[]
  timestamp: string
}

export default function ChatPage() {
  const { token } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | undefined>()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await api.chat.send(content, sessionId, token || undefined)

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response,
        products: response.products,
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, assistantMessage])
      setSessionId(response.session_id)
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <h1 className="text-2xl font-bold mb-4">AI Shopping Assistant</h1>
              <p className="text-muted-foreground mb-8">
                Ask me anything about products, comparisons, or recommendations
              </p>
              <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
                {[
                  "Find gaming laptops under ₹1,00,000",
                  "Compare iPhone 15 vs Samsung S24",
                  "Best monitors for programming",
                  "Budget headphones with good bass",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => handleSend(suggestion)}
                    className="p-3 text-left text-sm border rounded-lg hover:bg-accent transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div key={message.id}>
              <ChatMessage message={message} />
              {message.role === "assistant" && message.products && message.products.length > 0 && (
                <div className="ml-12 mt-2 grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {(message.products as unknown[]).slice(0, 4).map((product: unknown) => (
                    <ProductCard key={(product as Record<string, string>).id} product={product as Record<string, string>} compact />
                  ))}
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex items-center gap-2 text-muted-foreground">
              <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:0.4s]" />
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  )
}
