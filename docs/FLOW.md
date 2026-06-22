# User Flow Document

## Primary User Journeys

### Journey 1: First-Time User Onboarding

```mermaid
flowchart TD
    A[User visits app] --> B{Has account?}
    B -->|No| C[Register page]
    C --> D[Enter name, email, password]
    D --> E[Submit registration]
    E --> F{Success?}
    F -->|Yes| G[Login page]
    F -->|No| D
    B -->|Yes| G
    G --> H[Enter credentials]
    H --> I[Submit login]
    I --> J{Success?}
    J -->|Yes| K[Dashboard]
    J -->|No| G
    K --> L[Welcome modal]
    L --> M[Set preferences]
    M --> N[Main chat interface]
```

### Journey 2: Product Search & Recommendation

```mermaid
flowchart TD
    A[User opens chat] --> B[Types query]
    B --> C[AI processes query]
    C --> D[Extracts intent]
    D --> E[Searches products]
    E --> F[Analyzes reviews]
    F --> G[Compares options]
    G --> H[Generates recommendations]
    H --> I[Reflection validates]
    I --> J{Valid?}
    J -->|Yes| K[Display results]
    J -->|No| C
    K --> L[User selects product]
    L --> M[View details]
    M --> N{Actions}
    N -->|Save| O[Add to wishlist]
    N -->|Track| P[Track price]
    N -->|Compare| Q[Compare with others]
    N -->|New search| A
```

### Journey 3: Price Tracking Setup

```mermaid
flowchart TD
    A[User views product] --> B[Clicks Track Price]
    B --> C[Set target price]
    C --> D[Choose alert type]
    D --> E[Confirm tracking]
    E --> F[Product added to tracker]
    F --> G[Price check runs daily]
    G --> H{Price <= target?}
    H -->|Yes| I[Send notification]
    H -->|No| J[Continue monitoring]
    I --> K[User clicks notification]
    K --> L[View product deal]
    L --> M[Purchase or continue]
```

### Journey 4: Autonomous Research

```mermaid
flowchart TD
    A[User enters research query] --> B[Clicks Start Research]
    B --> C[System begins autonomous research]
    C --> D[Phase 1: Product Discovery]
    D --> E[Phase 2: Review Analysis]
    E --> F[Phase 3: Comparison]
    F --> G[Phase 4: Deal Finding]
    G --> H[Phase 5: Price Forecast]
    H --> I[Phase 6: Report Generation]
    I --> J[Display comprehensive report]
    J --> K{User action}
    K -->|Save report| L[Save to account]
    K -->|Share| M[Share report]
    K -->|Refine| N[Ask follow-up question]
    N --> C
```

## Edge Cases & Error States

| Scenario | User Sees | System Action |
|----------|-----------|---------------|
| No products found | "No products match your criteria" | Suggest broadening search |
| API timeout | "Research is taking longer..." | Continue in background |
| Invalid query | "I didn't understand that" | Suggest clarifying questions |
| Price tracking error | "Unable to track price" | Log error, notify admin |
| Rate limit exceeded | "Please wait a moment" | Show countdown timer |
| Session expired | "Please log in again" | Redirect to login |
| Network error | "Connection lost" | Retry automatically |
| Product unavailable | "This product is no longer available" | Suggest alternatives |

## Onboarding Flow

```mermaid
journey
    title User Onboarding Journey
    section Discovery
        Visit landing page: 5: User
        Read features: 4: User
        Click Get Started: 5: User
    section Registration
        Fill form: 3: User
        Submit: 4: User
        Verify email: 2: User
    section First Use
        Login: 5: User
        Set preferences: 3: User
        Ask first question: 5: User
        Get recommendations: 5: User
    section Engagement
        Save product: 4: User
        Track price: 4: User
        Return next day: 5: User
```

## Screen Inventory

| Screen | Route | Auth | Description |
|--------|-------|------|-------------|
| Landing | `/` | No | Marketing page, features, CTA |
| Login | `/login` | No | Email/password login |
| Register | `/register` | No | New account creation |
| Dashboard | `/dashboard` | Yes | Main overview, recent activity |
| Chat | `/chat` | Yes | Conversational shopping interface |
| Chat Session | `/chat/[id]` | Yes | Specific conversation |
| Products | `/products` | Yes | Browse all products |
| Product Detail | `/products/[id]` | Yes | Single product view |
| Compare | `/compare` | Yes | Side-by-side comparison |
| Saved Products | `/saved` | Yes | User's wishlist |
| Price Tracker | `/tracker` | Yes | Price monitoring dashboard |
| Analytics | `/analytics` | Yes | User insights and trends |
| Settings | `/settings` | Yes | Account preferences |
| Admin | `/admin` | Yes (Admin) | Platform management |

## Component States

### Chat Interface
- **Empty State**: Welcome message, suggested queries
- **Loading State**: Typing indicator, "Analyzing your request..."
- **Error State**: Error message, retry button
- **Success State**: Product cards, comparison tables

### Product Cards
- **Default**: Image, title, price, rating
- **Hover**: Quick actions (save, track, compare)
- **Loading**: Skeleton placeholders
- **Error**: Retry message

### Price Tracker
- **Active**: Current price, trend graph
- **Alert Triggered**: Notification badge
- **Paused**: Muted indicator
- **No Data**: "Start tracking" prompt

## Accessibility Considerations

1. **Keyboard Navigation**: All interactive elements focusable
2. **Screen Reader**: ARIA labels on all components
3. **Color Contrast**: WCAG AA compliance
4. **Focus Indicators**: Visible focus rings
5. **Error Announcements**: Live regions for errors
6. **Skip Links**: Skip to main content
