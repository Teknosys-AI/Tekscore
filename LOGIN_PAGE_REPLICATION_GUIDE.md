# Login Page Replication Guide

This document provides complete instructions for replicating the login page in another project. Follow these specifications exactly to achieve pixel-perfect replication.

---

## 📋 Table of Contents

1. [Page Structure Overview](#page-structure-overview)
2. [Layout & Grid System](#layout--grid-system)
3. [Global Styles & Theme](#global-styles--theme)
4. [Component Specifications](#component-specifications)
5. [Form Elements](#form-elements)
6. [Decorative Elements](#decorative-elements)
7. [Responsive Behavior](#responsive-behavior)
8. [Assets to Move](#assets-to-move)
9. [Dependencies & Services](#dependencies--services)
10. [Functionality & Logic](#functionality--logic)

---

## Page Structure Overview

The login page uses a **split-screen layout**:
- **Left Side (Desktop)**: White background with login form
- **Right Side (Desktop)**: Decorative background with gradient bubbles and illustration
- **Mobile**: Single column, form only (decorative side hidden)

The page is wrapped in `LandingLayoutComponent` which provides the basic layout structure.

---

## Layout & Grid System

### Desktop Layout
- **Grid**: `grid-template-columns: 1.2fr 0.8fr`
- **Left Column**: Form section (60% width)
- **Right Column**: Decorative section (40% width)
- **Height**: `100vh` (full viewport height)

### Mobile/Tablet Layout
- **Grid**: `grid-template-columns: 1fr` (single column)
- **Height**: `auto`, `min-height: 100vh`
- **Decorative Section**: Hidden (`display: none`)

### Breakpoints
- **Mobile**: `≤768px`
- **Tablet**: `769px - 1024px`
- **Desktop**: `>1024px`
- **Large LCD**: `>1400px`

---

## Global Styles & Theme

### Page Background
- **Color**: `#0c638d` (matches landing page hero/navbar)
- **Full Viewport**: `min-height: 100vh`
- **Overflow**: `hidden` (prevents scrollbars)

### Font Family
- **Primary Font**: `Poppins` (Google Fonts)
- **Font Import**: `@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');`
- **Font Variables**:
  - `--font-family-heading: 'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`
  - `--font-family-body: 'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`

### Color Palette

#### Brand Colors
- **Primary**: `#0d3337` (Dark teal)
- **Primary Dark**: `#082124`
- **Secondary**: `#0c638d` (Blue - used for page background)
- **Accent**: `#39b54a` (Green)

#### Text Colors
- **Text Color**: `#0d3337`
- **Text Color Muted**: `rgba(13, 51, 55, 0.65)`
- **Text Color Invert**: `#ffffff`

#### Error Colors
- **Error**: `#ef4444`
- **Error Background**: `rgba(239, 68, 68, 0.1)`
- **Error Border**: `rgba(239, 68, 68, 0.2)`

### Border Radius
- **Default**: `14px`
- **Small**: `8px` (used for inputs and buttons)
- **Input**: `clamp(10px, 1.5vw, 12px)`

---

## Component Specifications

### Login Container

#### Structure
```html
<div class="login-page">
  <div class="login-container">
    <div class="login-form-section"><!-- Left side --></div>
    <div class="login-decorative"><!-- Right side --></div>
  </div>
</div>
```

#### Styling
- **Display**: `grid`
- **Grid Template Columns**: `1.2fr 0.8fr` (desktop), `1fr` (mobile)
- **Height**: `100vh` (desktop), `auto` (mobile)
- **Position**: `relative`

---

### Left Side: Form Section

#### Background
- **Color**: `#ffffff` (white)
- **Padding**: `clamp(32px, 4vw, 48px)`
- **Overflow**: `overflow-y: auto` (allows scrolling if content exceeds viewport)
- **Alignment**: `align-items: center`, `justify-content: center`

#### Content Container
- **Max Width**: `440px`
- **Display**: `flex`, `flex-direction: column`
- **Gap**: `clamp(24px, 3vw, 32px)`

---

### Logo Section

#### Structure
```html
<div class="login-logo">
  <a routerLink="/">
    <img src="assets/logos/Amplify Logo - Light - Sharp.svg" alt="Amplify Logo" />
  </a>
</div>
```

#### Styling
- **Margin Bottom**: `clamp(20px, 2.5vw, 28px)`
- **Text Align**: `center`
- **Width**: `100%`

#### Logo Image
- **Height**: `clamp(64px, 12vw, 150px)` (desktop)
- **Height (Mobile)**: `clamp(110px, 12vw, 150px)`
- **Width**: `auto`
- **Display**: `block`
- **Margin**: `0 auto` (centered)

#### Link
- **Display**: `inline-block`
- **Text Decoration**: `none`

---

### Header Section

#### Structure
```html
<div class="login-header">
  <p class="login-subtitle">Start your journey</p>
  <h1 class="login-title">Sign In to Amplify</h1>
</div>
```

#### Subtitle
- **Text**: "Start your journey"
- **Font Size**: `clamp(0.875rem, 1.2vw, 1rem)`
- **Color**: `var(--text-color-muted)` (rgba(13, 51, 55, 0.65))
- **Margin**: `0 0 clamp(8px, 1vw, 12px) 0`
- **Font Weight**: `var(--font-weight-regular)` (400)

#### Title (H1)
- **Text**: "Sign In to Amplify"
- **Font Size**: `clamp(1.75rem, 3vw, 2.5rem)` (desktop)
- **Font Size (Mobile)**: `clamp(1.35rem, 2.2vw, 1.75rem)`
- **Font Size (Large LCD)**: `clamp(2.5rem, 3.5vw, 3rem)`
- **Font Weight**: `var(--font-weight-extrabold)` (800)
- **Color**: `var(--text-color)` (#0d3337)
- **Line Height**: `1.2`
- **Font Family**: `var(--font-family-heading)`
- **Margin**: `0`
- **Text Align**: Center (mobile), Left (desktop)

---

### Form Section

#### Structure
```html
<form class="login-form" (ngSubmit)="login()">
  <!-- Error message -->
  <!-- Email input -->
  <!-- Password input -->
  <!-- Submit button -->
  <!-- Forgot password link (mobile only) -->
</form>
```

#### Form Container
- **Display**: `flex`, `flex-direction: column`
- **Gap**: `clamp(16px, 2vw, 20px)` (desktop), `clamp(14px, 1.8vw, 18px)` (mobile)
- **Width**: `100%`

---

## Form Elements

### Error Message

#### Structure
```html
<div *ngIf="errorMessage" class="error-message">{{ errorMessage }}</div>
```

#### Styling
- **Color**: `var(--color-error)` (#ef4444)
- **Background**: `rgba(239, 68, 68, 0.1)`
- **Border**: `1px solid rgba(239, 68, 68, 0.2)`
- **Border Radius**: `var(--border-radius-sm)` (8px)
- **Padding**: `clamp(10px, 1.5vw, 12px)`
- **Font Size**: `clamp(0.875rem, 1.1vw, 0.9rem)`
- **Text Align**: `center`

#### Error Messages
- Empty fields: "Please enter email and password."
- Invalid credentials: "Invalid email or password. Please try again."
- Other errors: Uses `error?.message` or default message

---

### Email Input

#### Structure
```html
<div class="input-wrapper">
  <input
    type="email"
    placeholder="example@email.com"
    [(ngModel)]="email"
    name="email"
    required
    [disabled]="loading"
    class="form-input"
    aria-label="Email address"
  />
  <mat-icon class="input-icon email-icon">email</mat-icon>
</div>
```

#### Input Wrapper
- **Position**: `relative`
- **Width**: `100%`
- **Display**: `flex`, `align-items: center`
- **Gap**: `clamp(4px, 0.8vw, 6px)`
- **Min Height**: `clamp(48px, 7vw, 56px)` (desktop), `clamp(52px, 8vw, 56px)` (mobile)
- **Padding**: `0 clamp(0.875rem, 1.5vw, 1rem)` (desktop), `0 clamp(0.75rem, 1.2vw, 0.875rem)` (mobile)
- **Background**: `rgba(255, 255, 255, 0.08)`
- **Border**: `1px solid rgba(255, 255, 255, 0.25)`
- **Border Radius**: `clamp(10px, 1.5vw, 12px)`
- **Backdrop Filter**: `blur(8px) saturate(160%)`
- **Box Shadow**: `var(--shadow-sm)`
- **Transition**: `box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease`

#### Hover State
- **Background**: `rgba(255, 255, 255, 0.14)`
- **Border Color**: `rgba(255, 255, 255, 0.35)`

#### Focus State
- **Border Color**: `var(--color-primary)` (#0d3337)
- **Box Shadow**: `0 12px 40px rgba(0, 0, 0, 0.06), 0 0 0 clamp(4px, 0.8vw, 6px) rgba(0, 191, 166, 0.06)`

#### Input Field
- **Width**: `100%`
- **Padding**: `clamp(0.5rem, 0.8vw, 0.6rem) clamp(40px, 5vw, 48px) clamp(0.15rem, 0.3vw, 0.2rem) clamp(0.875rem, 1.5vw, 1rem)`
- **Border**: `none`
- **Border Radius**: `0` (border radius on wrapper)
- **Font Size**: `clamp(0.9rem, 1.2vw, 0.95rem)`
- **Font Family**: `var(--font-family-body)`
- **Color**: `var(--text-color)` (#0d3337)
- **Background**: `transparent`
- **Box Shadow**: `none`

#### Placeholder
- **Text**: "example@email.com"
- **Color**: `var(--text-color-muted)` (rgba(13, 51, 55, 0.65))

#### Email Icon
- **Position**: `absolute`
- **Right**: `clamp(12px, 1.8vw, 14px)`
- **Top**: `50%`
- **Transform**: `translateY(-50%)`
- **Color**: `var(--text-color-muted)`
- **Font Size**: `clamp(20px, 2.5vw, 22px)`
- **Width/Height**: `clamp(20px, 2.5vw, 22px)`
- **Icon**: `email` (Material Icons)
- **Pointer Events**: `none`

#### Disabled State
- **Background**: `transparent`
- **Opacity**: `0.6`
- **Cursor**: `not-allowed`

---

### Password Input

#### Structure
```html
<div class="input-wrapper">
  <input
    [type]="showPassword ? 'text' : 'password'"
    placeholder="Password"
    [(ngModel)]="password"
    name="password"
    required
    [disabled]="loading"
    class="form-input"
    aria-label="Password"
  />
  <button
    type="button"
    class="password-toggle"
    (click)="togglePasswordVisibility()"
    [attr.aria-label]="showPassword ? 'Hide password' : 'Show password'"
    tabindex="0"
  >
    <mat-icon>{{ showPassword ? 'visibility_off' : 'visibility' }}</mat-icon>
  </button>
</div>
```

#### Input Wrapper
- Same styling as email input wrapper

#### Input Field
- **Type**: `password` (default), `text` (when `showPassword` is true)
- **Placeholder**: "Password"
- Same styling as email input

#### Password Toggle Button
- **Position**: `absolute`
- **Right**: `clamp(12px, 1.8vw, 14px)`
- **Top**: `50%`
- **Transform**: `translateY(-50%)`
- **Background**: `none`
- **Border**: `none`
- **Cursor**: `pointer`
- **Padding**: `4px`
- **Display**: `flex`, `align-items: center`, `justify-content: center`
- **Color**: `var(--text-color-muted)`
- **Transition**: `color 0.2s ease`

#### Toggle Button Hover
- **Color**: `var(--color-primary)` (#0d3337)

#### Toggle Button Focus
- **Outline**: `2px solid var(--color-primary)`
- **Outline Offset**: `2px`
- **Border Radius**: `4px`

#### Toggle Icon
- **Icon**: `visibility` (show) or `visibility_off` (hide)
- **Font Size**: `clamp(20px, 2.5vw, 22px)`
- **Width/Height**: `clamp(20px, 2.5vw, 22px)`

---

### Submit Button

#### Structure
```html
<button
  type="submit"
  class="login-button"
  [disabled]="loading"
  [class.loading]="loading"
>
  <span *ngIf="!loading">Sign In</span>
  <span *ngIf="loading">Signing in...</span>
</button>
```

#### Styling
- **Width**: `100%`
- **Padding**: `clamp(12px, 1.8vw, 14px) clamp(24px, 3vw, 32px)` (desktop), `clamp(10px, 1.5vw, 12px) clamp(20px, 2.5vw, 24px)` (mobile)
- **Background**: `var(--color-primary)` (#0d3337)
- **Color**: `#ffffff`
- **Border**: `none`
- **Border Radius**: `var(--border-radius-sm)` (8px)
- **Font Size**: `clamp(0.95rem, 1.3vw, 1rem)` (desktop), `clamp(0.9rem, 1.2vw, 0.95rem)` (mobile)
- **Font Weight**: `var(--font-weight-semibold)` (600)
- **Font Family**: `var(--font-family-body)`
- **Cursor**: `pointer`
- **Margin Top**: `clamp(4px, 0.6vw, 8px)`
- **Transition**: `all 0.2s ease`

#### Hover State (Not Disabled)
- **Background**: `var(--color-primary-dark)` (#082124)
- **Transform**: `translateY(-1px)`
- **Box Shadow**: `0 4px 12px rgba(12, 99, 141, 0.3)`

#### Active State (Not Disabled)
- **Transform**: `translateY(0)`

#### Disabled State
- **Opacity**: `0.6`
- **Cursor**: `not-allowed`

#### Loading State
- **Position**: `relative`
- **Color**: `transparent` (hides text)
- **After Pseudo-element** (spinner):
  - **Content**: `''`
  - **Position**: `absolute`
  - **Top**: `50%`
  - **Left**: `50%`
  - **Transform**: `translate(-50%, -50%)`
  - **Width**: `20px`
  - **Height**: `20px`
  - **Border**: `2px solid #ffffff`
  - **Border Top Color**: `transparent`
  - **Border Radius**: `50%`
  - **Animation**: `spin 0.6s linear infinite`

#### Spinner Animation
```css
@keyframes spin {
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}
```

#### Button Text
- **Default**: "Sign In"
- **Loading**: "Signing in..."

---

### Forgot Password Link

#### Structure
```html
<a href="#forgot-password" class="forgot-password-link mobile-only">Forgot password?</a>
```

#### Styling
- **Display**: `none` (desktop), `block` (mobile)
- **Text Align**: `center`
- **Color**: `var(--color-accent)` (#39b54a)
- **Text Decoration**: `none`
- **Font Size**: `clamp(0.85rem, 1.1vw, 0.9rem)`
- **Margin Top**: `clamp(-8px, -1vw, -4px)`
- **Transition**: `color 0.2s ease`

#### Hover State
- **Color**: `var(--color-primary)` (#0d3337)
- **Text Decoration**: `underline`

---

### Footer Section

#### Structure
```html
<div class="login-footer">
  <p class="desktop-text">
    Don't have an account?
    <a routerLink="/" fragment="send-email" class="signup-link">Sign up</a>
  </p>
  <p class="mobile-text">
    Don't have an account?
    <a routerLink="/" fragment="send-email" class="signup-link">Register!</a>
  </p>
</div>
```

#### Footer Container
- **Text Align**: `center`
- **Margin Top**: `clamp(8px, 1vw, 12px)` (desktop), `clamp(12px, 1.5vw, 16px)` (mobile)

#### Desktop Text
- **Display**: `block` (desktop), `none` (mobile)
- **Color**: `var(--text-color-muted)` (rgba(13, 51, 55, 0.65))
- **Font Size**: `clamp(0.85rem, 1.1vw, 0.9rem)`
- **Margin**: `0`
- **Text**: "Don't have an account? Sign up"

#### Mobile Text
- **Display**: `none` (desktop), `block` (mobile)
- **Color**: `var(--text-color)` (#0d3337)
- **Font Size**: `clamp(0.85rem, 1.1vw, 0.9rem)`
- **Margin**: `0`
- **Text**: "Don't have an account? Register!"

#### Signup Link
- **Color**: `var(--color-accent)` (#39b54a)
- **Text Decoration**: `none`
- **Font Weight**: `var(--font-weight-semibold)` (600)
- **Margin Left**: `4px`
- **Transition**: `color 0.2s ease`
- **Router Link**: `/` with fragment `#send-email`

#### Signup Link Hover
- **Color**: `var(--color-primary)` (#0d3337)
- **Text Decoration**: `underline`

---

## Decorative Elements

### Right Side: Decorative Section

#### Structure
```html
<div class="login-decorative">
  <div class="gradient-background">
    <div class="bubble bubble-1"></div>
    <div class="bubble bubble-2"></div>
    <div class="bubble bubble-3"></div>
    <div class="bubble bubble-4"></div>
    <div class="bubble bubble-5"></div>
  </div>
  <img
    class="login-decorative-image"
    src="/assets/images/Login-Image.png"
    alt="Illustration of marketing analytics and messaging"
    loading="lazy"
    decoding="async"
  />
</div>
```

#### Container
- **Display**: `flex` (desktop), `none` (mobile)
- **Align Items**: `center`
- **Justify Content**: `center`
- **Position**: `relative`
- **Overflow**: `visible`

---

### Decorative Image

#### Styling
- **Position**: `relative`
- **Width**: `90%`
- **Height**: `auto`
- **Max Width**: `none`
- **Object Fit**: `contain`
- **Transform**: `translateX(26px) scale(1.9)`
- **Transform Origin**: `center center`
- **Z-Index**: `1`
- **Filter**: `drop-shadow(0 18px 45px rgba(2, 8, 23, 0.55))`

#### Image Source
- **Path**: `/assets/images/Login-Image.png`
- **Alt Text**: "Illustration of marketing analytics and messaging"
- **Loading**: `lazy`
- **Decoding**: `async`

---

### Gradient Background

#### Container
- **Position**: `absolute`
- **Inset**: `0` (covers entire decorative section)
- **Width**: `100%`
- **Height**: `100%`
- **Overflow**: `hidden`

---

### Animated Bubbles

All bubbles have:
- **Position**: `absolute`
- **Border Radius**: `50%`
- **Filter**: `blur(60px)`
- **Opacity**: `0.3`
- **Animation**: `float 20s infinite ease-in-out`

#### Bubble 1
- **Size**: `clamp(300px, 40vw, 500px)`
- **Background**: `radial-gradient(circle, rgba(57, 181, 74, 0.4) 0%, transparent 70%)` (Green)
- **Position**: `top: -10%, right: -5%`
- **Animation Delay**: `0s`

#### Bubble 2
- **Size**: `clamp(250px, 35vw, 400px)`
- **Background**: `radial-gradient(circle, rgba(123, 97, 255, 0.4) 0%, transparent 70%)` (Purple)
- **Position**: `top: 20%, left: -10%`
- **Animation Delay**: `-5s`

#### Bubble 3
- **Size**: `clamp(200px, 30vw, 350px)`
- **Background**: `radial-gradient(circle, rgba(255, 107, 157, 0.4) 0%, transparent 70%)` (Pink)
- **Position**: `bottom: 10%, right: 10%`
- **Animation Delay**: `-10s`

#### Bubble 4
- **Size**: `clamp(180px, 25vw, 300px)`
- **Background**: `radial-gradient(circle, rgba(12, 99, 141, 0.4) 0%, transparent 70%)` (Blue)
- **Position**: `top: 50%, right: 20%`
- **Animation Delay**: `-15s`

#### Bubble 5
- **Size**: `clamp(150px, 20vw, 250px)`
- **Background**: `radial-gradient(circle, rgba(57, 181, 74, 0.3) 0%, transparent 70%)` (Green, lighter)
- **Position**: `bottom: 20%, left: 15%`
- **Animation Delay**: `-7s`

#### Float Animation
```css
@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -30px) scale(1.1);
  }
  50% {
    transform: translate(-15px, 20px) scale(0.9);
  }
  75% {
    transform: translate(30px, 10px) scale(1.05);
  }
}
```

---

## Responsive Behavior

### Mobile/Tablet (≤1024px)

#### Grid Layout
- **Grid Template Columns**: `1fr` (single column)
- **Height**: `auto`, `min-height: 100vh`

#### Form Section
- **Padding**: `clamp(24px, 3vw, 32px)`
- **Padding Top**: `clamp(40px, 5vw, 60px)`
- **Align Items**: `flex-start`
- **Content Max Width**: `100%` (removes max-width constraint)
- **Gap**: `clamp(20px, 2.5vw, 28px)`

#### Logo
- **Height**: `clamp(110px, 12vw, 150px)`
- **Align Self**: `center`
- **Margin Bottom**: `clamp(24px, 3vw, 32px)`

#### Header
- **Text Align**: `center`
- **Margin Bottom**: `clamp(12px, 1.5vw, 16px)`

#### Subtitle
- **Font Size**: `clamp(0.8rem, 1.1vw, 0.95rem)`

#### Title
- **Font Size**: `clamp(1.5rem, 2.5vw, 2rem)`

#### Input Wrapper
- **Min Height**: `clamp(52px, 8vw, 56px)`
- **Padding**: `0 clamp(0.75rem, 1.2vw, 0.875rem)`

#### Form Input
- **Padding (Mobile)**: `clamp(0.6rem, 1vw, 0.7rem) clamp(36px, 4.5vw, 44px) clamp(0.2rem, 0.4vw, 0.3rem) clamp(0.75rem, 1.2vw, 0.875rem)`
- **Font Size (Mobile)**: `clamp(0.875rem, 1.1vw, 0.9rem)`

#### Forgot Password Link
- **Display**: `block` (shown on mobile)

#### Footer
- **Desktop Text**: `display: none`
- **Mobile Text**: `display: block`

#### Decorative Section
- **Display**: `none` (hidden on mobile/tablet)

---

### Mobile Only (≤768px)

#### Form Section
- **Padding**: `clamp(24px, 3vw, 32px) clamp(16px, 2.5vw, 20px)`
- **Padding Top**: `clamp(32px, 4vw, 48px)`

#### Title
- **Font Size**: `clamp(1.35rem, 2.2vw, 1.75rem)`

#### Content Gap
- **Gap**: `clamp(18px, 2vw, 24px)`

---

### Large LCD (>1400px)

#### Form Section
- **Padding**: `clamp(48px, 3vw, 64px)`

#### Input Wrapper
- **Min Height**: `clamp(56px, 6vw, 60px)`
- **Padding**: `0 clamp(1rem, 1.5vw, 1.25rem)`

#### Content
- **Max Width**: `500px`
- **Gap**: `clamp(32px, 2.5vw, 40px)`

#### Title
- **Font Size**: `clamp(2.5rem, 3.5vw, 3rem)`

---

## Assets to Move

### Logo Files
Copy this file to your project's `assets/logos/` directory:
- ✅ `Amplify Logo - Light - Sharp.svg` (used in login page)

### Image Files
Copy this file to your project's `assets/images/` directory:
- ✅ `Login-Image.png` (decorative illustration on right side)

### Asset Paths in Code

#### Logo
```html
<img src="assets/logos/Amplify Logo - Light - Sharp.svg" alt="Amplify Logo" />
```

#### Decorative Image
```html
<img
  src="/assets/images/Login-Image.png"
  alt="Illustration of marketing analytics and messaging"
/>
```

---

## Dependencies & Services

### Required Angular Modules
- `CommonModule`
- `FormsModule` (for `[(ngModel)]`)
- `RouterModule` (for routing and `routerLink`)
- `MatIconModule` (Angular Material Icons)

### Required Services (from Shared Library)
- `AuthService` - handles authentication
- `AccessService` - manages user access data
- `LoggingService` - logging functionality
- `TwoFactorService` - 2FA flow management

### Required Shared Functions
- `storeSetupRequirements()` - stores setup requirements
- `clearSetupRequirements()` - clears setup requirements

### Material Icons Used
- `email` - email input icon
- `visibility` - show password icon
- `visibility_off` - hide password icon

---

## Functionality & Logic

### Component Properties

```typescript
email = '';              // Email input value
password = '';           // Password input value
loading = false;         // Loading state
errorMessage = '';       // Error message to display
showPassword = false;    // Password visibility toggle
```

### Methods

#### togglePasswordVisibility()
- Toggles `showPassword` between `true` and `false`
- Changes input type between `password` and `text`
- Updates icon between `visibility` and `visibility_off`

#### login()
- Validates email and password are not empty
- Sets `loading = true` and clears `errorMessage`
- Calls `authService.signIn(email, password)`
- Handles different login result statuses:
  - `PASSWORD_CHANGE_REQUIRED`: Navigate to password setup
  - `SUCCESS`: Load access data, then navigate to dashboard
  - `2FA_SETUP_REQUIRED`: Navigate to 2FA setup
  - `2FA_REQUIRED`: Navigate to 2FA verification
- On error: Sets `errorMessage` and `loading = false`

### Login Flow

1. **User submits form** → `login()` called
2. **Validation** → Check if email and password are provided
3. **API Call** → `authService.signIn(email, password)`
4. **Handle Response**:
   - **Success**: Load access data → Navigate to dashboard
   - **Password Change Required**: Navigate to `/setup-password`
   - **2FA Setup Required**: Navigate to `/setup-2fa`
   - **2FA Verification Required**: Navigate to `/verify-2fa`
   - **Error**: Display error message

### Return URL
- Default: `/dashboard`
- Can be set via query parameter: `?returnUrl=/path`
- Used after successful authentication

### Form Validation
- **Email**: Required, type `email`
- **Password**: Required, type `password`
- **Client-side**: Basic empty check
- **Server-side**: Actual authentication validation

### Loading States
- **Button**: Shows spinner when `loading = true`
- **Inputs**: Disabled when `loading = true`
- **Button Text**: Changes from "Sign In" to "Signing in..."

### Error Handling
- **Empty Fields**: "Please enter email and password."
- **Invalid Credentials**: "Invalid email or password. Please try again."
- **Other Errors**: Uses `error?.message` or default message
- **Error Display**: Red background, border, centered text

---

## Social Login (Commented Out)

The template includes commented-out social login buttons. If you want to implement them:

### Structure
```html
<div class="social-login desktop-only">
  <p class="social-divider">or sign in with</p>
  <div class="social-buttons">
    <button class="social-button facebook">...</button>
    <button class="social-button google">...</button>
    <button class="social-button apple">...</button>
  </div>
</div>
```

### Styling
- **Display**: `flex` (desktop), `none` (mobile)
- **Gap**: `clamp(12px, 1.8vw, 16px)`
- **Margin Top**: `clamp(8px, 1vw, 12px)`

### Social Divider
- **Text**: "or sign in with"
- **Color**: `var(--text-color-muted)`
- **Font Size**: `clamp(0.85rem, 1.1vw, 0.9rem)`
- **Has decorative lines** (before/after pseudo-elements)

### Social Buttons
- **Size**: `clamp(44px, 5.5vw, 48px)` (desktop), `clamp(48px, 6vw, 52px)` (mobile)
- **Border**: `1px solid rgba(15, 23, 36, 0.12)`
- **Border Radius**: `var(--border-radius-sm)` (8px)
- **Background**: `#ffffff`
- **Hover**: `translateY(-2px)`, shadow

### Button Colors
- **Facebook**: `#1877f2` background, white icon
- **Google**: White background, colored SVG
- **Apple**: `var(--surface)` background, dark icon

---

## Important Notes

1. **Layout Component**: The login page uses `LandingLayoutComponent` which provides basic structure. Ensure this is set up correctly.

2. **Form Submission**: Uses Angular's `(ngSubmit)` event, not `(click)` on button.

3. **Two-Way Binding**: Uses `[(ngModel)]` for form inputs. Requires `FormsModule`.

4. **Password Visibility**: Toggle button is positioned absolutely within input wrapper.

5. **Loading State**: Button shows spinner animation when loading. Inputs are disabled during loading.

6. **Error Messages**: Displayed above form inputs, with red styling.

7. **Responsive**: Decorative side is completely hidden on mobile/tablet.

8. **Accessibility**: 
   - Proper `aria-label` attributes
   - Keyboard navigation support
   - Focus states on interactive elements

9. **Navigation**: 
   - Logo links to home (`/`)
   - Sign up link goes to home with fragment (`/#send-email`)

10. **Color Consistency**: Page background (`#0c638d`) matches landing page hero/navbar.

---

## Implementation Checklist

- [ ] Set up `LandingLayoutComponent`
- [ ] Create login component with all properties
- [ ] Implement form with email and password inputs
- [ ] Add password visibility toggle
- [ ] Implement error message display
- [ ] Add loading state with spinner
- [ ] Style input wrappers with glassmorphism
- [ ] Add decorative section with bubbles and image
- [ ] Implement responsive breakpoints
- [ ] Add logo and footer links
- [ ] Copy required assets (logo, image)
- [ ] Set up routing for `/login`
- [ ] Integrate `AuthService` and other services
- [ ] Test form validation
- [ ] Test loading states
- [ ] Test error handling
- [ ] Test responsive behavior
- [ ] Test password visibility toggle
- [ ] Verify all colors match specifications
- [ ] Verify all fonts and sizes match specifications
- [ ] Test navigation flows (2FA, password setup, etc.)

---

## Final Notes

This guide provides pixel-perfect specifications for replicating the login page. Pay special attention to:

- **Exact color values**: `#0c638d` for background, `#0d3337` for primary, `#39b54a` for accent
- **Glassmorphism effects**: Input wrappers use backdrop-filter and semi-transparent backgrounds
- **Responsive breakpoints**: Decorative section hidden on mobile, form adapts to screen size
- **Animation details**: Bubble float animation with different delays
- **Form states**: Loading, error, disabled states with proper styling
- **Accessibility**: ARIA labels, keyboard navigation, focus states

If you encounter any discrepancies, refer back to the original component files for the exact implementation details.
