# 🎨 Search Feature UI Preview

## Visual Mockup of the New Search Interface

### Full Page View

```
╔═══════════════════════════════════════════════════════════════════╗
║  MatrimonyMatch                    Browse Profiles    Admin    👤 ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Discover Your Match                                              ║
║  Browse through profiles and find your perfect partner            ║
║                                                                   ║
║  ┌─────────────────────────────────────────────────────────────┐ ║
║  │ 🔍 Search by name, occupation, location, education...        │ ║
║  │ ┌──────────────────────────────┐ ┌────────┐ ┌────────────┐  │ ║
║  │ │ [                          ] │ │ Search │ │  Filters ▼ │  │ ║
║  │ └──────────────────────────────┘ └────────┘ └────────────┘  │ ║
║  │ Found 42 profiles                                            │ ║
║  └─────────────────────────────────────────────────────────────┘ ║
║                                                                   ║
║  ╔═══════════════════════════════════════════════════════════╗  ║
║  ║ 🔧 Advanced Filters                                       ║  ║
║  ╠═══════════════════════════════════════════════════════════╣  ║
║  ║                                                            ║  ║
║  ║  Gender         Min Age       Max Age        Location      ║  ║
║  ║  [   All  ▼]   [  18   ]    [  60   ]    [            ]  ║  ║
║  ║                                                            ║  ║
║  ║  Occupation     Education         Marital Status          ║  ║
║  ║  [         ]    [            ]    [   All      ▼]        ║  ║
║  ║                                                            ║  ║
║  ║  [ Apply Filters ]  [ Clear All ]                         ║  ║
║  ╚═══════════════════════════════════════════════════════════╝  ║
║                                                                   ║
║  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       ║
║  │               │  │               │  │               │       ║
║  │  [Profile]    │  │  [Profile]    │  │  [Profile]    │       ║
║  │               │  │               │  │               │       ║
║  │   25 yrs      │  │   28 yrs      │  │   26 yrs      │       ║
║  │               │  │               │  │               │       ║
║  │ Priya Sharma  │  │  Raj Patel    │  │ Neha Kapoor   │       ║
║  │ 📍 Mumbai     │  │ 📍 Delhi      │  │ 📍 Bangalore  │       ║
║  │ 💼 Doctor     │  │ 💼 Engineer   │  │ 💼 Teacher    │       ║
║  │ 🎓 MBBS       │  │ 🎓 B.Tech     │  │ 🎓 M.Ed       │       ║
║  │               │  │               │  │               │       ║
║  │ [View] [Send] │  │ [View] [Send] │  │ [View] [Send] │       ║
║  └───────────────┘  └───────────────┘  └───────────────┘       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Component Breakdown

### 1. Search Bar Component (Always Visible)

```
┌─────────────────────────────────────────────────────────────────┐
│ [🔍] Search by name, occupation, location, education...          │
│                                                                   │
│  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━]  [Search]  [Filters ▼]       │
│                                                                   │
│  Found 42 profiles                                               │
└─────────────────────────────────────────────────────────────────┘

Colors:
- Background: White (#FFFFFF)
- Border: Gray 300 (#D1D5DB)
- Search button: Red-Pink gradient
- Filters button: Gray border
- Result count: Red 600 text (#DC2626)
```

### 2. Advanced Filters Panel (Collapsible)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔧 Advanced Filters                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Row 1: [Gender ▼] [Min Age] [Max Age] [Location]               │
│  Row 2: [Occupation] [Education] [Marital Status ▼]             │
│                                                                   │
│  [Apply Filters] [Clear All]                                     │
└─────────────────────────────────────────────────────────────────┘

Layout:
- 4 columns on large screens (lg:grid-cols-4)
- 2 columns on medium screens (md:grid-cols-2)
- 1 column on mobile (grid-cols-1)
- Slides down with fadeIn animation
```

### 3. Profile Cards (Search Results)

```
┌─────────────────┐
│                 │  ← Profile Picture (h-64)
│   [  IMAGE  ]   │
│                 │
│      28 yrs     │  ← Age badge (top-right)
├─────────────────┤
│ John Doe        │  ← Name (bold)
│ 📍 Mumbai, MH   │  ← Location
│ 💼 Engineer     │  ← Occupation
│ 🎓 B.Tech       │  ← Education
│                 │
│ [View Profile]  │  ← View button (border)
│ [Send Interest] │  ← Interest button (gradient)
└─────────────────┘

Grid Layout:
- 3 columns on large screens (lg:grid-cols-3)
- 2 columns on medium screens (md:grid-cols-2)
- 1 column on mobile (grid-cols-1)
- Gap of 1.5rem between cards (gap-6)
```

---

## Interactive States

### Search Bar States

**1. Default State**
```
[🔍] Search by name, occupation, location...  [Search] [Filters ▼]
```

**2. Typing State**
```
[🔍] software engineer▌                        [Search] [Filters ▼]
```

**3. With Results**
```
[🔍] software engineer                         [Search] [Filters ▼]
Found 12 profiles
```

**4. No Results**
```
[🔍] zzzzzzzzz                                 [Search] [Filters ▼]
Found 0 profiles
```

**5. Loading State**
```
[🔍] doctor                                    [⟳] [Filters ▼]
Searching...
```

---

### Advanced Filters States

**1. Collapsed (Default)**
```
[Search Bar]
[Filters ▼] ← Button shows "Advanced Filters"
```

**2. Expanded**
```
[Search Bar]
[Filters ▲] ← Button shows "Hide Filters"

┌─ Advanced Filters Panel ─┐
│  [Filter inputs...]       │
│  [Apply] [Clear]          │
└──────────────────────────┘
```

**3. With Active Filters**
```
[Search Bar with filters]
Found 8 profiles ← Count updates

[Filters ▲]
┌─ Advanced Filters Panel ─┐
│ Gender: Female ✓          │
│ Age: 25-30 ✓              │
│ Location: Mumbai ✓        │
└──────────────────────────┘
```

---

## Color Palette Used

### Primary Colors
```
Red 600:     #DC2626  ━━━  Search button, result count
Pink 600:    #DB2777  ━━━  Gradient end color
Red 700:     #B91C1C  ━━━  Hover state
Pink 700:    #BE185D  ━━━  Hover gradient end
```

### Neutral Colors
```
White:       #FFFFFF  ━━━  Card backgrounds
Gray 50:     #F9FAFB  ━━━  Page background
Gray 300:    #D1D5DB  ━━━  Borders
Gray 600:    #4B5563  ━━━  Secondary text
Gray 900:    #111827  ━━━  Primary text
```

### Accent Colors
```
Green 400:   #4ADE80  ━━━  Success notifications
Red 400:     #F87171  ━━━  Error notifications
Blue 400:    #60A5FA  ━━━  Info messages
```

---

## Typography

### Headings
```
H1 (Page Title):     text-3xl font-bold text-gray-900
H2 (Section):        text-lg font-semibold text-gray-900
H3 (Profile Name):   text-xl font-bold text-gray-900
```

### Body Text
```
Normal:              text-sm text-gray-600
Small:               text-xs text-gray-500
Bold:                font-semibold
```

### Inputs
```
Input text:          text-gray-900
Placeholder:         text-gray-400
Focus state:         focus:ring-2 focus:ring-red-500
```

---

## Spacing System

### Padding
```
Card padding:        p-6 (1.5rem)
Button padding:      px-6 py-3 (1.5rem × 0.75rem)
Input padding:       px-3 py-2 (0.75rem × 0.5rem)
```

### Margins
```
Section margin:      mb-8 (2rem)
Element margin:      mb-4 (1rem)
Small margin:        mb-2 (0.5rem)
```

### Gap (Grid/Flex)
```
Card grid gap:       gap-6 (1.5rem)
Filter grid gap:     gap-4 (1rem)
Button group:        space-x-4 (1rem)
```

---

## Animations

### fadeIn
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Used for:**
- Advanced filters panel slide-down
- Notification toasts
- New results appearing

### Spinner (Loading)
```html
<svg class="animate-spin h-5 w-5">
  <!-- Spinner SVG -->
</svg>
```

**Used for:**
- Search button during API call
- Page loading state

### Hover Effects
```css
.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
```

**Used for:**
- Profile cards
- Buttons (scale-105)

---

## Responsive Breakpoints

### Mobile (< 768px)
```
- 1 column grid
- Full-width search bar
- Stacked buttons
- Simplified filters
```

### Tablet (768px - 1024px)
```
- 2 column grid
- Compact search bar
- Side-by-side buttons
- 2-column filters
```

### Desktop (> 1024px)
```
- 3 column grid
- Full search bar
- All buttons visible
- 4-column filters
```

---

## Accessibility Features

✅ **Keyboard Navigation**
- Tab through all inputs
- Enter to search
- Escape to close filters

✅ **ARIA Labels**
```html
<button aria-label="Search profiles">Search</button>
<button aria-label="Toggle advanced filters">Filters</button>
```

✅ **Focus States**
```css
focus:ring-2 focus:ring-red-500 focus:outline-none
```

✅ **Screen Reader Text**
```html
<span class="sr-only">Loading search results...</span>
```

---

## Summary

**Visual Identity:**
- Clean, modern design with red-pink gradient theme
- Professional matrimonial site aesthetic
- Focus on usability and clarity

**Key UI Elements:**
1. Prominent search bar with icon
2. Gradient action buttons
3. Collapsible advanced filters
4. Live result count
5. Responsive profile grid
6. Smooth animations

**User Experience:**
- Intuitive single search bar
- Progressive disclosure (advanced filters)
- Instant visual feedback
- Clear call-to-actions
- Mobile-optimized

This is a **production-ready** search interface! 🎨✨

