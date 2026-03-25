# Landing Page Replication Guide

This document provides complete instructions for replicating the initial landing page in another project. Follow these specifications exactly to achieve pixel-perfect replication.

---

## 📋 Table of Contents

1. [Page Structure Overview](#page-structure-overview)
2. [Component Hierarchy](#component-hierarchy)
3. [Global Styles & Theme](#global-styles--theme)
4. [Component-by-Component Specifications](#component-by-component-specifications)
5. [Assets to Move](#assets-to-move)
6. [Dependencies & Shared Components](#dependencies--shared-components)

---

## Page Structure Overview

The landing page consists of the following sections in order:
1. **Navbar (Fixed at top)**
2. **Hero Section**
3. **Features Section**
4. **Use Cases Section**
5. **Pricing Section** (conditionally shown)
6. **Footer**

All sections are wrapped in a `.landing-wrapper` container.

---

## Component Hierarchy

```
LandingComponent
├── NavbarV2Component
├── HeroV2Component
├── FeaturesComponent
├── UseCasesComponent
├── PricingComponent (conditional)
└── FooterComponent
```

---

## Global Styles & Theme

### Font Family
- **Primary Font**: `Poppins` (Google Fonts)
- **Font Import**: `@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');`
- **Font Variables**:
  - `--font-family-heading: 'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`
  - `--font-family-body: 'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`

### Color Palette (Light Mode)

#### Brand Colors
- **Primary**: `#0d3337` (Dark teal)
- **Primary Dark**: `#082124`
- **Primary Light**: `#2a5155`
- **Secondary**: `#0c638d` (Blue)
- **Accent**: `#39b54a` (Green)
- **Success**: `#39b54a`

#### Text Colors
- **Text Color**: `#0d3337`
- **Text Color Muted**: `rgba(13, 51, 55, 0.65)`
- **Text Color Invert**: `#ffffff`

#### Background Colors
- **Background**: `linear-gradient(180deg, #f0f4f6 0%, #ffffff 100%)`
- **Surface**: `#ffffff`
- **Card Background**: `rgba(255, 255, 255, 0.7)` with glassmorphism

#### Glassmorphism Variables
- **Glass Blur**: `12px`
- **Glass Blur Strong**: `18px`
- **Glass Border**: `1px solid rgba(13, 51, 55, 0.08)`
- **Glass Shadow**: `0 2px 8px rgba(13, 51, 55, 0.04)`
- **Glass Shadow Strong**: `0 4px 12px rgba(13, 51, 55, 0.06)`

### Typography Scale
- **Font Weight Variables**:
  - `--font-weight-semibold`: 600
  - `--font-weight-bold`: 700
  - `--font-weight-extrabold`: 800
  - `--font-weight-medium`: 500

### Border Radius
- **Default**: `14px`
- **Small**: `8px`
- **Large**: `22px`

### Landing Wrapper Background
```css
background: radial-gradient(1200px 600px at 20% -10%, rgba(0, 191, 166, 0.06), transparent),
            radial-gradient(900px 500px at 80% 110%, rgba(123, 97, 255, 0.06), transparent);
```

---

## Component-by-Component Specifications

### 1. NavbarV2Component

#### Structure
- Fixed position at top
- Contains: Logo, Navigation Links, Action Buttons (Login, Start Free Trial)
- Mobile: Hamburger menu

#### Colors
- **Background**: `#0c638d` (solid, no transparency)
- **Border**: `1px solid rgba(255, 255, 255, 0.1)`
- **Text Color**: `rgba(255, 255, 255, 0.9)`
- **Hover Text**: `var(--color-accent)` (#39b54a)

#### Logo
- **Path**: `/assets/logos/Amplify Logo - Dark - Sharp.svg`
- **Dimensions**: 
  - Desktop: `clamp(40px, 6vw, 50px)` height
  - Large LCD: `clamp(50px, 5vw, 60px)` height

#### Navigation Links
- **Font Size**: `clamp(0.875rem, 1.2vw, 0.95rem)`
- **Font Weight**: `var(--font-weight-semibold)` (600)
- **Gap**: `clamp(16px, 2.5vw, 20px)`
- **Links**: Home, Features, Use cases, Pricing (conditional)

#### Buttons
- **Primary Button** (Start Free Trial):
  - Background: `var(--color-accent)` (#39b54a)
  - Hover: `#5cda71`
  - Color: `#ffffff`
  - Border: `none`
  - Padding: `clamp(0.65rem, 1vw, 0.75rem) clamp(1rem, 1.5vw, 1.25rem)`
  - Border Radius: `var(--border-radius)` (8px)
  
- **Ghost Button** (Login):
  - Background: `transparent`
  - Border: `1px solid rgba(255, 255, 255, 0.3)`
  - Color: `rgba(255, 255, 255, 0.9)`
  - Hover: `rgba(255, 255, 255, 0.1)` background

#### Mobile Menu
- **Background**: `#0c638d`
- **Border**: `1px solid rgba(255, 255, 255, 0.1)`
- **Border Radius**: `16px`
- **Box Shadow**: `0 8px 24px rgba(0, 0, 0, 0.3)`
- **Position**: Fixed, below navbar

#### Z-Index
- Navbar: `1000`
- Mobile Menu: `1000`
- Overlay: `999`

---

### 2. HeroV2Component

#### Structure
- Two-column grid layout (1.1fr : 0.9fr)
- Left: Text content (heading, subtitle, description, CTA)
- Right: Phone preview carousel with gradient bubbles

#### Background
- **Color**: `#0c638d` (solid)
- **Full width**: `100%`
- **No padding/margin on container**

#### Grid Layout
- **Max Width**: `1400px` (desktop), `none` on large screens
- **Gap**: `clamp(40px, 5vw, 80px)`
- **Padding**: `clamp(60px, 8vw, 100px) clamp(80px, 10vw, 120px)`
- **Mobile**: Single column, centered text

#### Heading (H1)
- **Text**: "Launch Targeted SMS Campaigns in Minutes"
- **Font Size**: `clamp(2rem, 4vw, 3.25rem)`
- **Font Weight**: `var(--font-weight-extrabold)` (800)
- **Color**: `#ffffff`
- **Line Height**: `1.2`
- **Letter Spacing**: `-0.02em`
- **Text Align**: Left (center on mobile)

#### Subtitle
- **Text**: "Drop Marketing Messages Directly Into Their Hands"
- **Font Size**: `clamp(1.125rem, 1.75vw, 1.5rem)`
- **Font Weight**: `var(--font-weight-semibold)` (600)
- **Color**: `var(--color-accent)` (#39b54a)
- **Line Height**: `1.4`

#### Description
- **Text**: "Build targeted campaigns with our 4-step builder, advanced demographic and geo-targeting, and real-time analytics."
- **Font Size**: `clamp(0.95rem, 1.4vw, 1.125rem)`
- **Color**: `rgba(255, 255, 255, 0.85)`
- **Line Height**: `1.6`
- **Max Width**: `90%`

#### CTA Button
- **Label**: "View Demo"
- **Variant**: Primary
- **Background**: `var(--color-accent)` (#39b54a)
- **Hover**: `#5cda71`
- **Min Width**: `clamp(160px, 20vw, 180px)`

#### Phone Carousel
- **Width**: `clamp(220px, 22vw, 360px)`
- **Min Height**: `clamp(480px, 50vw, 640px)`
- **Transform Scale**: `1.15` (desktop), `1.1` (tablet), `1.05` (mobile)
- **Slides**: Auto-rotate every 3500ms
- **Transitions**: `460ms cubic-bezier(0.19, 1, 0.22, 1)`

#### Gradient Bubbles (Background Decoration)
Three animated gradient bubbles:
1. **Large Bubble**:
   - Size: `clamp(400px, 50vw, 600px)`
   - Position: `top: -20%, right: -10%`
   - Color: `radial-gradient(circle, rgba(57, 181, 74, 0.3) 0%, transparent 70%)`
   - Blur: `60px`
   - Opacity: `0.25`

2. **Medium Bubble**:
   - Size: `clamp(300px, 35vw, 450px)`
   - Position: `top: 50%, left: 50%` (centered)
   - Color: `radial-gradient(circle, rgba(13, 51, 55, 0.4) 0%, transparent 70%)`

3. **Small Bubble**:
   - Size: `clamp(200px, 25vw, 300px)`
   - Position: `bottom: -10%, left: -5%`
   - Color: `radial-gradient(circle, rgba(57, 181, 74, 0.25) 0%, transparent 70%)`

#### Phone Preview Slides
1. **Logo Slide**:
   - Type: Splash screen
   - Image: `/assets/logos/Amplify Logo - Light - Sharp.svg`
   - Alt: "Amplify logo splash"

2. **Message Slide**:
   - Type: SMS preview
   - Title: "Campaign Preview"
   - Sender: "Amplify"
   - Channel: "SMS"
   - Execution: "Scheduled"
   - Message: "Get 20% off your next purchase! Limited time offer."

---

### 3. FeaturesComponent

#### Structure
- Centered content with heading, intro, and 4-column grid
- Each feature card has flip animation on hover

#### Heading (H2)
- **Text**: "The Amplify Advantage"
- **Font Size**: `clamp(1.5rem, 3vw, 2.25rem)`
- **Font Weight**: `var(--font-weight-extrabold)` (800)
- **Color**: `var(--text-color)` (#0d3337)
- **Text Align**: Center
- **Letter Spacing**: `-0.02em`

#### Intro Text
- **Text**: "All-in-one platform for SMS marketing with advanced targeting, real-time analytics, and budget control"
- **Font Size**: `clamp(0.9rem, 1.3vw, 1rem)`
- **Color**: `var(--text-color-muted)`
- **Max Width**: `60ch`
- **Text Align**: Center

#### Grid Layout
- **Desktop**: 4 columns
- **Tablet (≤1200px)**: 3 columns
- **Tablet (≤900px)**: 2 columns
- **Mobile (≤768px)**: 1 column
- **Gap**: `clamp(12px, 1.5vw, 18px)`

#### Feature Cards
Each card has:
- **Front Side** (visible by default):
  - Icon (Material Icons)
  - Title (H3)
  
- **Back Side** (flips on hover):
  - Description paragraph

- **Card Styling**:
  - Background: `var(--card-bg, rgba(255, 255, 255, 0.7))`
  - Backdrop Filter: `blur(16px)`
  - Border: `var(--glass-border)`
  - Border Radius: `20px`
  - Box Shadow: `var(--glass-shadow)`
  - Padding: `clamp(16px, 2vw, 24px)`
  - Min Height: `200px`
  - Perspective: `1000px` (for 3D flip)
  - Transition: `0.6s ease`

- **Hover Effect**:
  - Transform: `rotateY(180deg)`
  - Box Shadow: `var(--glass-shadow-strong)`

#### Feature Icons
- **Container**:
  - Size: `clamp(48px, 5vw, 56px)`
  - Border Radius: `clamp(14px, 1.5vw, 16px)`
  - Background: `linear-gradient(135deg, rgba(0, 191, 166, 0.25), rgba(123, 97, 255, 0.25))`
  - Border: `1px solid rgba(0, 191, 166, 0.15)`
  - Box Shadow: `0 4px 12px rgba(0, 191, 166, 0.15), 0 2px 4px rgba(123, 97, 255, 0.1)`

- **Icon**:
  - Color: `var(--color-primary)` (#0d3337)
  - Size: `clamp(24px, 2.8vw, 28px)`

#### Feature Titles (H3)
- **Font Size**: `clamp(1.125rem, 1.6vw, 1.375rem)`
- **Font Weight**: `var(--font-weight-bold)` (700)
- **Color**: `var(--text-color)` (#0d3337)
- **Text Align**: Center
- **Hover Color**: `var(--color-primary)`

#### Feature Descriptions
- **Font Size**: `clamp(0.85rem, 1.2vw, 0.95rem)`
- **Color**: `var(--text-color-muted)`
- **Line Height**: `1.6`
- **Text Align**: Center

#### Feature List (8 features)
1. **Campaign Builder** (icon: `send`)
   - Description: "4-step builder: Basic Info → Audience → Message → Review. Schedule campaigns and set budget caps. Launch in minutes."

2. **Segment Builder** (icon: `pie_chart`)
   - Description: "Build dynamic segments with demographics, geo-targeting, and device filters. Upload custom lists or create segments instantly."

3. **Message Builder** (icon: `message`)
   - Description: "Create SMS templates with custom sender titles and content. Track character count, enable delivery reports, and reuse templates across campaigns."

4. **Analytics Dashboard** (icon: `insights`)
   - Description: "Monitor real-time metrics: campaigns, spend, balance, and SMS sent. View interactive charts tracking delivery rates and performance."

5. **Geo-Targeting** (icon: `place`)
   - Description: "Target audiences by location using polygon boundaries on an interactive map. Combine with province and city filters for precise regional campaigns."

6. **Demographic Targeting** (icon: `people`)
   - Description: "Filter audiences by age groups, gender, income class, device type, and operating system. Create highly targeted segments for better engagement."

7. **Budget Control** (icon: `account_balance`)
   - Description: "Set campaign caps to control spending and prevent overspending. Track total spend and current balance in real-time through the analytics dashboard."

8. **Delivery Reports** (icon: `track_changes`)
   - Description: "Track message delivery status in real-time. Monitor sent vs delivered rates, view detailed reports, and optimize campaigns based on delivery performance."

#### Reveal Animation
- Cards fade in and slide up on scroll
- Staggered delays: 0ms, 80ms, 160ms, 240ms, 320ms, 400ms, 480ms, 560ms
- Transition: `600ms ease`

---

### 4. UseCasesComponent

#### Structure
- Centered content with heading, intro, and 3-column grid

#### Heading (H2)
- **Text**: "Use Cases"
- **Font Size**: `clamp(1.5rem, 3vw, 2.25rem)`
- **Font Weight**: `var(--font-weight-extrabold)` (800)
- **Color**: `var(--text-color)` (#0d3337)
- **Text Align**: Center
- **Letter Spacing**: `-0.02em`

#### Intro Text
- **Text**: "See how businesses use Amplify to reach their audiences with targeted SMS campaigns"
- **Font Size**: `clamp(0.9rem, 1.3vw, 1rem)`
- **Color**: `var(--text-color-muted)`
- **Max Width**: `60ch`
- **Text Align**: Center

#### Grid Layout
- **Desktop**: 3 columns
- **Tablet (≤1024px)**: 2 columns
- **Mobile (≤768px)**: 1 column
- **Gap**: `clamp(12px, 1.5vw, 18px)`

#### Use Case Cards
- **Background**: `var(--card-bg, rgba(255, 255, 255, 0.7))`
- **Backdrop Filter**: `blur(16px)`
- **Border**: `var(--glass-border)`
- **Border Radius**: `20px`
- **Box Shadow**: `var(--glass-shadow)`
- **Padding**: `clamp(16px, 2vw, 24px)`
- **Text Align**: Left
- **Hover Effect**: `translateY(-4px)`, stronger shadow

#### Card Titles (H3)
- **Font Size**: `clamp(1rem, 1.5vw, 1.125rem)`
- **Font Weight**: `var(--font-weight-bold)` (700)
- **Color**: `var(--text-color)` (#0d3337)
- **Margin Bottom**: `clamp(6px, 0.8vw, 8px)`

#### Card Descriptions
- **Font Size**: `clamp(0.85rem, 1.2vw, 0.95rem)`
- **Color**: `var(--text-color-muted)`
- **Line Height**: `1.5`

#### Use Case List (6 cards)
1. **Promotional Campaigns**
   - Description: "Launch targeted promotions using demographic filters and geo-targeting. Create segments for specific regions, schedule campaigns, and track performance with real-time analytics."

2. **Regional Marketing**
   - Description: "Target specific provinces and cities with polygon geo-targeting. Combine location filters with demographic data to reach the right audience with personalized messages."

3. **Customer Segmentation**
   - Description: "Build dynamic segments using age groups, gender, income class, and device filters. Create highly targeted campaigns that resonate with specific customer personas."

4. **Budget-Controlled Campaigns**
   - Description: "Set campaign caps to control spending and prevent overspending. Monitor total spend and balance in real-time, ensuring campaigns stay within budget while maximizing reach."

5. **Delivery Tracking**
   - Description: "Track message delivery status with real-time reports. Monitor sent vs delivered rates, optimize campaigns based on delivery performance, and ensure messages reach your audience."

6. **Performance Optimization**
   - Description: "Use real-time analytics dashboard to track campaign performance and view interactive charts. Make data-driven decisions and optimize targeting and messaging based on actionable insights."

#### Reveal Animation
- Cards fade in and slide up on scroll
- Staggered delays: 0ms, 80ms, 160ms, 240ms, 320ms, 400ms
- Transition: `600ms ease`

---

### 5. PricingComponent

#### Structure
- Centered content with heading, intro, and 3-column grid

#### Heading (H2)
- **Text**: "Simple, transparent pricing"
- **Font Size**: `clamp(1.5rem, 3vw, 2.25rem)`
- **Font Weight**: `var(--font-weight-extrabold)` (800)
- **Color**: `var(--text-color)` (#0d3337)
- **Text Align**: Center
- **Letter Spacing**: `-0.02em`

#### Intro Text
- **Text**: "Choose the plan that fits your business. All plans include a 14-day free trial."
- **Font Size**: `clamp(0.9rem, 1.3vw, 1rem)`
- **Color**: `var(--text-color-muted)`
- **Max Width**: `60ch`
- **Text Align**: Center

#### Grid Layout
- **Desktop**: 3 columns
- **Tablet (≤1024px)**: 2 columns
- **Mobile (≤768px)**: 1 column
- **Gap**: `clamp(12px, 1.5vw, 18px)`
- **Max Width**: `1100px` (desktop), `none` on large screens

#### Pricing Cards
- **Background**: `var(--card-bg, rgba(255, 255, 255, 0.7))`
- **Backdrop Filter**: `blur(16px)`
- **Border**: `var(--glass-border)`
- **Border Radius**: `20px`
- **Box Shadow**: `var(--glass-shadow)`
- **Padding**: `clamp(16px, 2vw, 24px)`
- **Hover Effect**: `translateY(-4px)`, stronger shadow

#### Popular Plan Styling
- **Border**: `2px solid var(--color-primary)` (#0d3337)
- **Background**: `linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.7))`
- **Box Shadow**: `0 8px 32px rgba(0, 191, 166, 0.15)`
- **Badge**: "Most Popular" (top right)

#### Plan Structure
Each plan has:
1. **Plan Name** (H3):
   - Font Size: `clamp(1.25rem, 2vw, 1.5rem)`
   - Font Weight: `var(--font-weight-bold)` (700)
   - Color: `var(--text-color)` (#0d3337)
   - Text Align: Center

2. **Plan Card**:
   - **Plan Head**:
     - Price Row (price + period)
     - Badge (if popular)
     - Border Bottom: `1px solid rgba(15, 23, 36, 0.08)`
   
   - **Price**:
     - Font Size: `clamp(1.5rem, 3vw, 2rem)`
     - Font Weight: `var(--font-weight-extrabold)` (800)
     - Color: `var(--text-color)` (#0d3337)
   
   - **Period**:
     - Font Size: `var(--font-size-sm)`
     - Color: `var(--text-color-muted)`
   
   - **Feature List**:
     - List style: None
     - Check mark: `✔` (green: `var(--color-success)` #39b54a)
     - Font Size: `clamp(0.95rem, 1.3vw, 1.05rem)`
     - Line Height: `var(--line-height-relaxed)`
     - Margin: `clamp(8px, 1vw, 12px)` between items
   
   - **CTA Button**:
     - Width: `100%`
     - Padding: `clamp(10px, 1.2vw, 12px) clamp(16px, 2vw, 20px)`
     - Border Radius: `12px`
     - Font Weight: `var(--font-weight-semibold)` (600)
     - Font Size: `clamp(0.875rem, 1.1vw, 0.95rem)`
     - Background: `rgba(255, 255, 255, 0.8)`
     - Border: `1px solid rgba(15, 23, 36, 0.12)`
     - Popular Plan: Background `var(--color-primary)`, color `#fff`, no border

3. **Plan Blurb**:
   - Font Size: `clamp(0.9rem, 1.2vw, 1rem)`
   - Color: `var(--text-color-muted)`
   - Text Align: Center

#### Pricing Plans (3 plans)

1. **Basic Plan**:
   - Name: "Basic"
   - Price: "$8"
   - Period: "per month"
   - Blurb: "Best for individuals getting started."
   - CTA: "Sign up"
   - Popular: `false`
   - Features:
     - 4-step campaign builder
     - Basic segment builder
     - SMS message templates
     - Location-based targeting
     - Basic analytics dashboard
     - Email support

2. **Advanced Plan** (Popular):
   - Name: "Advanced"
   - Price: "$29"
   - Period: "per month"
   - Blurb: "Best for growing teams ready to scale."
   - CTA: "Start free trial"
   - Popular: `true`
   - Features:
     - Everything in Basic
     - Advanced segment builder with demographic filters
     - Polygon geo-targeting
     - Budget control & campaign capping
     - Real-time analytics with charts
     - Delivery reports & tracking
     - Priority support

3. **Premium Plan**:
   - Name: "Premium"
   - Price: "Custom"
   - Period: "per month"
   - Blurb: "Best for large orgs with custom needs."
   - CTA: "Talk to sales"
   - Popular: `false`
   - Features:
     - Everything in Advanced
     - Custom segment filters
     - File upload for segments
     - Advanced analytics & reporting
     - Custom integrations
     - Dedicated account manager
     - Tailored onboarding & training

#### Reveal Animation
- Cards fade in and slide up on scroll
- Staggered delays: 0ms, 120ms, 240ms
- Transition: `600ms ease`

---

### 6. FooterComponent

#### Structure
- Three-column grid (Product, Company, Newsletter)
- Social media icons
- Copyright notice

#### Background
- **Color**: `#ffffff`
- **Border Top**: `1px solid rgba(12, 18, 38, 0.06)`

#### Footer Content
- **Max Width**: `1200px` (desktop), `none` on large screens
- **Padding**: `clamp(20px, 2.5vw, 28px) clamp(16px, 2vw, 24px)`
- **Gap**: `clamp(1rem, 1.5vw, 1.25rem)`

#### Column Grid
- **Desktop**: 3 columns
- **Tablet (≤768px)**: 2 columns
- **Mobile (≤600px)**: 1 column
- **Gap**: `clamp(24px, 3vw, 40px)`
- **Text Align**: Left (center on small mobile)

#### Column Headings (H4)
- **Font Size**: `clamp(0.95rem, 1.3vw, 1rem)`
- **Font Weight**: `var(--font-weight-semibold)` (600)
- **Color**: `var(--text-color)` (#0d3337)
- **Margin Bottom**: `clamp(8px, 1vw, 10px)`

#### Column Links
- **Font Size**: `clamp(0.85rem, 1.1vw, 0.9rem)`
- **Color**: `var(--text-color-muted)`
- **Hover Color**: `var(--color-primary)` (#0d3337)
- **Margin**: `clamp(4px, 0.6vw, 6px)` between links

#### Column 1: Product
- **Links**:
  - Features (href: `#features`)
  - Use cases (href: `#use-cases`)

#### Column 2: Company
- **Links**:
  - About (href: `https://teknosys.ai/#about`, target: `_blank`)
  - Contact (href: `https://teknosys.ai/#contact`, target: `_blank`)

#### Column 3: Newsletter
- **Heading**: "Stay in the loop"
- **Content**: Email link
  - Email: `contact@amplify.com`
  - Color: `var(--color-primary)` (#0d3337)
  - Hover: Underline, darker color

#### Social Media Icons
- **Icons**: Twitter, LinkedIn, Facebook
- **Font Size**: `clamp(1rem, 1.4vw, 1.1rem)`
- **Color**: `var(--text-color-muted)`
- **Hover Color**: `var(--color-primary)` (#0d3337)
- **Min Size**: `44px × 44px` (touch target)
- **Gap**: `clamp(0.75rem, 1.2vw, 1rem)`

#### Footer Bottom
- **Border Top**: `1px solid rgba(12, 18, 38, 0.06)`
- **Padding Top**: `clamp(0.625rem, 1vw, 0.875rem)`
- **Font Size**: `clamp(0.75rem, 1vw, 0.85rem)`
- **Text**: "© 2025 Teknosys. All rights reserved."
- **Text Align**: Center

---

## Assets to Move

### Logo Files
Copy these files to your project's `assets/logos/` directory:
- `Amplify Logo - Dark - Sharp.svg` (used in navbar)
- `Amplify Logo - Light - Sharp.svg` (used in hero phone carousel)

### Video Files
Copy this file to your project's `assets/videos/` directory:
- `product-demo.mp4` (used in video modal)

### Note on Assets
- Ensure all asset paths match exactly: `/assets/logos/...` and `/assets/videos/...`
- If your project structure differs, update all asset references in components

---

## Dependencies & Shared Components

### Required Shared Components
You'll need these components from the shared library:

1. **SectionContainer**
   - Wraps each section
   - Provides consistent padding and background handling
   - Accepts `backgroundColor` input

2. **ButtonComponent**
   - Used for CTAs
   - Variants: `primary`, `ghost`
   - Accepts `label` and `clicked` event

3. **PhonePreviewComponent**
   - Displays phone mockup with message preview
   - Variants: `splash`, `default`
   - Accepts `model` (PhonePreviewModel) and `splashImageSrc`

4. **VideoModalComponent**
   - Modal for video playback
   - Accepts `open`, `videoSrc`, and `closed` event

5. **RevealOnScrollDirective**
   - Adds reveal animation on scroll
   - Applied to grid containers

### Required Directives
- `RevealOnScrollDirective` - for scroll-triggered animations

### Required Services
- `FeatureFlagsService` - for conditional rendering (pricing section, buttons)

### Material Icons
- Import `MatIconModule` for feature icons
- Icons used: `send`, `pie_chart`, `message`, `insights`, `place`, `people`, `account_balance`, `track_changes`

### Angular Modules
- `CommonModule`
- `RouterModule`
- `MatIconModule` (Angular Material)

---

## Responsive Breakpoints

The project uses custom breakpoint mixins. Key breakpoints:
- **Mobile**: `≤768px`
- **Tablet**: `769px - 1024px`
- **Desktop**: `>1024px`
- **Large LCD**: `>1400px`

### Breakpoint Mixin Usage
```scss
@include mobile { /* styles */ }
@include tablet { /* styles */ }
@include desktop { /* styles */ }
@include large-lcd { /* styles */ }
@include mobile-tablet { /* styles */ }
```

---

## Section Spacing

All sections (except hero) have:
- **Padding Top**: `120px` (desktop), `60px` (mobile)
- **Padding Bottom**: `120px` (desktop), `60px` (mobile)
- **Scroll Margin Top**: `80px` (for anchor links)

---

## Animation Details

### Hero Phone Carousel
- **Auto-advance**: Every `3500ms`
- **Transition**: `460ms cubic-bezier(0.19, 1, 0.22, 1)`
- **Transform**: `translateY(18px) scale(0.96)` → `translateY(0) scale(1)`

### Feature Card Flip
- **Trigger**: Hover (desktop), Active/Tap (mobile)
- **Duration**: `0.6s ease`
- **Transform**: `rotateY(180deg)`
- **Perspective**: `1000px`

### Reveal Animations
- **Duration**: `600ms ease`
- **Transform**: `translateY(10px)` → `translateY(0)`
- **Opacity**: `0` → `1`
- **Staggered delays**: See individual sections

---

## Important Notes

1. **Hero Background**: The hero section has a solid `#0c638d` background that overrides the landing wrapper gradient.

2. **Glassmorphism**: All cards use glassmorphism effects with:
   - `backdrop-filter: blur(16px)`
   - Semi-transparent backgrounds
   - Subtle borders and shadows

3. **Color Variables**: Use CSS custom properties (variables) for all colors to maintain consistency and enable theme switching.

4. **Font Loading**: Ensure Poppins font is loaded before rendering to avoid FOUT (Flash of Unstyled Text).

5. **Mobile Menu**: The mobile menu is positioned fixed and appears below the navbar when opened.

6. **Touch Targets**: All interactive elements have minimum `44px × 44px` touch targets for accessibility.

7. **Z-Index Hierarchy**:
   - Navbar: `1000`
   - Mobile Menu: `1000`
   - Overlay: `999`
   - Hero: `2`
   - Landing Wrapper Overlay: `0`

8. **Feature Flags**: The pricing section and some buttons are conditionally rendered based on feature flags. You may need to implement a simple feature flag service or remove the conditions.

---

## Implementation Checklist

- [ ] Set up global theme CSS with all color variables
- [ ] Import Poppins font from Google Fonts
- [ ] Create shared components (SectionContainer, Button, PhonePreview, VideoModal)
- [ ] Create RevealOnScrollDirective
- [ ] Implement NavbarV2Component
- [ ] Implement HeroV2Component with phone carousel
- [ ] Implement FeaturesComponent with flip cards
- [ ] Implement UseCasesComponent
- [ ] Implement PricingComponent
- [ ] Implement FooterComponent
- [ ] Copy all required assets (logos, videos)
- [ ] Set up routing for landing page
- [ ] Test responsive breakpoints
- [ ] Test animations and interactions
- [ ] Verify all colors match specifications
- [ ] Verify all fonts and sizes match specifications
- [ ] Test mobile menu functionality
- [ ] Verify scroll behavior and anchor links

---

## Final Notes

This guide provides pixel-perfect specifications for replicating the landing page. Pay special attention to:
- Exact color values (especially `#0c638d` for hero/navbar and `#39b54a` for accent)
- Font sizes using `clamp()` for responsive typography
- Glassmorphism effects on all cards
- Animation timings and easing functions
- Responsive grid layouts that adapt at specific breakpoints

If you encounter any discrepancies, refer back to the original component files for the exact implementation details.
