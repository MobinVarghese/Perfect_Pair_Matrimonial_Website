# 🎨 TailwindCSS Component Reference

## Common Patterns Used Across Pages

### 1. Gradient Backgrounds

```jsx
// Full page gradient
<div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-rose-100">

// Button gradient
<button className="bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700">

// Card gradient header
<div className="bg-gradient-to-r from-blue-500 to-blue-600">
```

### 2. Form Inputs

```jsx
// Standard input
<input
  className="block w-full px-4 py-3 border border-gray-300 rounded-lg 
             focus:ring-2 focus:ring-red-500 focus:border-transparent 
             transition duration-150"
/>

// Input with error
<input
  className={`block w-full px-4 py-3 border ${
    error ? 'border-red-300' : 'border-gray-300'
  } rounded-lg focus:ring-2 focus:ring-red-500`}
/>

// Input with icon
<div className="relative">
  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
    <svg className="h-5 w-5 text-gray-400">...</svg>
  </div>
  <input className="block w-full pl-10 pr-3 py-3 border..." />
</div>
```

### 3. Buttons

```jsx
// Primary button
<button className="w-full bg-gradient-to-r from-red-600 to-pink-600 text-white 
                   px-6 py-3 rounded-lg hover:from-red-700 hover:to-pink-700 
                   transition duration-150 transform hover:scale-105">

// Secondary button
<button className="border-2 border-red-600 text-red-600 px-6 py-3 rounded-lg 
                   hover:bg-red-50 transition duration-150">

// Disabled button
<button disabled 
        className="... disabled:opacity-50 disabled:cursor-not-allowed">
```

### 4. Cards

```jsx
// Basic card
<div className="bg-white rounded-xl shadow-md p-6">

// Card with hover effect
<div className="bg-white rounded-xl shadow-md overflow-hidden card-hover">

// Profile card
<div className="bg-white rounded-xl shadow-md overflow-hidden">
  <div className="relative h-64 bg-gradient-to-br from-pink-100 to-red-100">
    {/* Image */}
  </div>
  <div className="p-5">
    {/* Content */}
  </div>
</div>
```

### 5. Alerts/Notifications

```jsx
// Success alert
<div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
  <div className="flex">
    <svg className="h-5 w-5 text-green-400">...</svg>
    <p className="ml-3 text-sm text-green-700">Success message</p>
  </div>
</div>

// Error alert
<div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
  <div className="flex">
    <svg className="h-5 w-5 text-red-400">...</svg>
    <p className="ml-3 text-sm text-red-700">Error message</p>
  </div>
</div>

// Info alert
<div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
  <div className="flex">
    <svg className="h-5 w-5 text-blue-400">...</svg>
    <p className="ml-3 text-sm text-blue-700">Info message</p>
  </div>
</div>
```

### 6. Loading Spinners

```jsx
// Centered spinner
<div className="flex justify-center items-center py-20">
  <svg className="animate-spin h-12 w-12 text-red-600" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
</div>

// Inline spinner (in button)
<svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
</svg>
```

### 7. Grid Layouts

```jsx
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Items */}
</div>

// Stats grid
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  {/* Stats cards */}
</div>

// Form grid
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  {/* Form fields */}
</div>
```

### 8. Tables

```jsx
<div className="overflow-x-auto">
  <table className="min-w-full divide-y divide-gray-200">
    <thead className="bg-gray-50">
      <tr>
        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
          Header
        </th>
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-200">
      <tr className="hover:bg-gray-50">
        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          Data
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

### 9. Badges

```jsx
// Status badge
<span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
               bg-green-100 text-green-800">
  Active
</span>

// Age badge (on profile image)
<div className="absolute top-3 right-3 bg-white rounded-full px-3 py-1 
               text-xs font-semibold text-gray-700">
  25 yrs
</div>
```

### 10. Dropdown Menus

```jsx
// User menu dropdown
<div className="relative">
  <button onClick={() => setIsOpen(!isOpen)}>
    Menu
  </button>
  {isOpen && (
    <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl 
                    py-1 border border-gray-200 animate-fadeIn">
      <a className="block px-4 py-2 text-sm text-gray-700 hover:bg-red-50 
                    hover:text-red-600 transition">
        Option
      </a>
    </div>
  )}
</div>
```

### 11. Tabs

```jsx
// Tab buttons
<nav className="flex -mb-px">
  <button className={`flex items-center px-6 py-4 border-b-2 font-medium text-sm ${
    isActive 
      ? 'border-red-600 text-red-600' 
      : 'border-transparent text-gray-500 hover:text-gray-700'
  }`}>
    Tab Label
  </button>
</nav>
```

### 12. Avatar/Profile Pictures

```jsx
// Small avatar
<div className="h-8 w-8 rounded-full bg-gradient-to-br from-red-400 to-pink-500 
               flex items-center justify-center">
  <span className="text-white font-semibold text-sm">A</span>
</div>

// Large profile picture
<div className="h-32 w-32 rounded-full bg-gradient-to-br from-pink-100 to-red-100 
               flex items-center justify-center overflow-hidden">
  <img src="..." className="h-full w-full object-cover" />
</div>
```

### 13. Icons with Text

```jsx
<div className="flex items-center">
  <svg className="w-4 h-4 mr-2 text-red-600">...</svg>
  <span>Text</span>
</div>
```

### 14. Section Headers

```jsx
<h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
  <svg className="w-6 h-6 mr-2 text-red-600">...</svg>
  Section Title
</h2>
```

### 15. Empty States

```jsx
<div className="text-center py-20">
  <svg className="mx-auto h-16 w-16 text-gray-400 mb-4">...</svg>
  <h3 className="text-xl font-semibold text-gray-900 mb-2">No Results</h3>
  <p className="text-gray-600">Try adjusting your filters</p>
</div>
```

## 📱 Responsive Breakpoints

```
sm:  640px  (small devices)
md:  768px  (medium devices)
lg:  1024px (large devices)
xl:  1280px (extra large devices)
```

### Usage Examples:

```jsx
// Hide on mobile, show on desktop
<div className="hidden md:block">

// 1 column mobile, 2 columns tablet, 3 columns desktop
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Full width mobile, fixed width desktop
<div className="w-full md:w-1/2 lg:w-1/3">

// Different padding on different screens
<div className="px-4 md:px-6 lg:px-8">
```

## 🎨 Custom Animations (in index.css)

### Fade In Animation

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

.animate-fadeIn {
  animation: fadeIn 0.5s ease-out;
}
```

Usage:
```jsx
<div className="animate-fadeIn">
  Fades in from below
</div>
```

### Card Hover Effect

```css
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
```

Usage:
```jsx
<div className="bg-white rounded-xl shadow-md card-hover">
  Lifts up on hover
</div>
```

## 🎯 Color Palette

### Primary Colors (Red/Pink)
```
red-50   #fef2f2  - Lightest backgrounds
red-100  #fee2e2  - Light backgrounds
red-600  #dc2626  - Primary buttons
red-700  #b91c1c  - Hover states

pink-50  #fdf2f8  - Lightest backgrounds
pink-600 #db2777  - Accent color
```

### Neutral Colors
```
gray-50   #f9fafb  - Very light backgrounds
gray-100  #f3f4f6  - Light backgrounds
gray-300  #d1d5db  - Borders
gray-500  #6b7280  - Secondary text
gray-700  #374151  - Primary text
gray-900  #111827  - Headings
```

### Status Colors
```
green-100  #dcfce7  - Success background
green-500  #22c55e  - Success border
green-700  #15803d  - Success text

blue-100   #dbeafe  - Info background
blue-500   #3b82f6  - Info border
blue-700   #1d4ed8  - Info text

yellow-100 #fef3c7  - Warning background
yellow-500 #eab308  - Warning border
yellow-700 #a16207  - Warning text

red-100    #fee2e2  - Error background
red-500    #ef4444  - Error border
red-700    #b91c1c  - Error text
```

## 💡 Pro Tips

### 1. Consistent Spacing
```jsx
// Use gap utilities for spacing
<div className="space-y-6">  {/* Vertical spacing */}
<div className="space-x-4">  {/* Horizontal spacing */}
<div className="gap-6">      {/* Grid/flex gap */}
```

### 2. Transitions
```jsx
// Always add transition for smooth effects
className="... transition duration-150 ease-in-out"
```

### 3. Focus States
```jsx
// Always include focus states for accessibility
className="... focus:ring-2 focus:ring-red-500 focus:outline-none"
```

### 4. Disabled States
```jsx
// Always style disabled states
className="... disabled:opacity-50 disabled:cursor-not-allowed"
```

### 5. Hover Effects
```jsx
// Add subtle hover effects for interactivity
className="... hover:bg-gray-50 hover:text-red-600 transition"
```

## 🔧 Utility Combinations

### Centered Content
```jsx
<div className="flex items-center justify-center min-h-screen">
```

### Card with Shadow
```jsx
<div className="bg-white rounded-xl shadow-md p-6">
```

### Button Group
```jsx
<div className="flex space-x-4">
  <button>...</button>
  <button>...</button>
</div>
```

### Truncated Text
```jsx
<p className="truncate">Long text that will be truncated...</p>
```

### Full Width on Mobile, Auto on Desktop
```jsx
<div className="w-full md:w-auto">
```

---

**Use this reference while building new components!** 🎨
