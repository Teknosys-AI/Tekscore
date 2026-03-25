# Side Menu Component - Complete Replication Guide

This guide provides detailed instructions for replicating the side menu (sidebar) component, including all hover effects, icon colors, expansion logic, section behavior, and styling details.

---

## 📋 Table of Contents

1. [Component Overview](#component-overview)
2. [File Structure](#file-structure)
3. [Component TypeScript Logic](#component-typescript-logic)
4. [HTML Template Structure](#html-template-structure)
5. [SCSS Styling Details](#scss-styling-details)
6. [Expansion/Collapse Logic](#expansioncollapse-logic)
7. [Hover Effects](#hover-effects)
8. [Icon Colors & States](#icon-colors--states)
9. [Section Behavior](#section-behavior)
10. [Responsive Behavior](#responsive-behavior)
11. [Integration with Layout](#integration-with-layout)
12. [Theme Variables Required](#theme-variables-required)

---

## 🎯 Component Overview

The side menu is a fixed navigation sidebar that:
- Expands/collapses on desktop
- Acts as a drawer overlay on mobile/tablet
- Shows/hides menu item labels based on expansion state
- Displays tooltips on hover when collapsed
- Groups navigation items into sections with titles
- Has a help icon button at the bottom

**Component Selector:** `app-sidebar`

**Location:** `packages/shared/src/lib/components/sidebar/`

---

## 📁 File Structure

```
packages/shared/src/lib/components/sidebar/
├── sidebar.component.ts       # Component logic
├── sidebar.component.html    # Template
└── sidebar.component.scss    # Styles
```

**Dependencies:**
- `@angular/common` (CommonModule)
- `@angular/router` (RouterLink, RouterLinkActive)
- `@angular/material/icon` (MatIconModule)
- `@angular/core/rxjs-interop` (takeUntilDestroyed)
- Shared services: `FeatureFlagsService`, `AccessService`, `AccessHelperService`, `UnifiedAccessService`
- Shared models: `MODULES`, `FEATURES`

---

## 💻 Component TypeScript Logic

### Component Class

```typescript
import { Component, Input, Output, EventEmitter, inject, OnInit, OnDestroy, DestroyRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FeatureFlagsService, AccessService, AccessHelperService, UnifiedAccessService } from '../../core/services';
import { MODULES, FEATURES } from '../../core/models';

interface NavItem {
  label: string;
  icon: string; // Material icon name
  route: string;
}

interface NavSection {
  title?: string;
  items: NavItem[];
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, MatIconModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements OnInit, OnDestroy {
  @Input() isExpanded = false;
  @Input() isMobile = false;
  @Input() isTablet = false;
  @Output() toggleSidebar = new EventEmitter<void>();
  @Output() closeSidebar = new EventEmitter<void>();

  protected readonly featureFlags = inject(FeatureFlagsService);
  private readonly access = inject(AccessService);
  private readonly accessHelper = inject(AccessHelperService);
  private readonly unifiedAccess = inject(UnifiedAccessService);
  private readonly destroyRef = inject(DestroyRef);

  navSections: NavSection[] = [];

  ngOnInit() {
    this.buildNavSections();
    
    // Subscribe to access changes to rebuild nav sections when permissions change
    // This ensures sidebar updates immediately after plan changes, role changes, etc.
    this.access.access$
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => {
        this.buildNavSections();
      });
  }

  ngOnDestroy() {
    // Cleanup handled by takeUntilDestroyed
  }

  private buildNavSections(): void {
    const items: NavItem[] = [];

    if (this.access.canSeeModule(MODULES.CAMPAIGNS)) {
      items.push({ label: 'Dashboard', icon: 'dashboard', route: '/dashboard' });
      items.push({ label: 'Campaigns', icon: 'campaign', route: '/dashboard/campaigns' });
    }

    // Segments - check SEGMENTS module visibility (plan-controlled)
    if (this.access.canSeeModule(MODULES.SEGMENTS)) {
      items.push({ label: 'Segments', icon: 'category', route: '/dashboard/segments' });
    }

    // Meta - check META module visibility (backend provides dynamically)
    if (this.accessHelper.canViewMeta()) {
      items.push({ label: 'Meta', icon: 'facebook', route: '/dashboard/meta' });
    }

    // Communications - check CAMPAIGNS module visibility
    if (this.access.canSeeModule(MODULES.CAMPAIGNS)) {
      items.push({ label: 'Communications', icon: 'message', route: '/dashboard/communications' });
    }

    // Analytics - check ANALYTICS module visibility (plan-controlled)
    if (
      this.featureFlags.isAnalyticsMenuItemEnabled() &&
      this.access.canSeeModule(MODULES.ANALYTICS)
    ) {
      items.push({ label: 'Analytics', icon: 'insights', route: '/dashboard/analytics' });
    }

    if (
      this.featureFlags.isNotificationsMenuItemEnabled() &&
      this.access.canSeeModule(MODULES.BILLING)
    ) {
      items.push({
        label: 'Notifications',
        icon: 'notifications',
        route: '/dashboard/notifications',
      });
    }

    // Subscription - check SUBSCRIPTIONS module visibility (plan-controlled)
    if (this.access.canSeeModule(MODULES.SUBSCRIPTIONS)) {
      items.push({
        label: 'Subscription',
        icon: 'subscriptions',
        route: '/dashboard/subscription',
      });
    }

    this.navSections = [
      {
        title: 'Pages',
        items,
      },
      {
        title: 'Account Pages',
        items: [
          ...(this.featureFlags.isProfileMenuItemEnabled() &&
          this.access.canSeeModule(MODULES.USERS)
            ? [{ label: 'Profile', icon: 'person', route: '/dashboard/profile' }]
            : []),
          { label: 'Integrations', icon: 'integration_instructions', route: '/dashboard/integrations' },
          { label: 'Settings', icon: 'settings', route: '/dashboard/settings' },
        ],
      },
    ];
  }

  toggle() {
    if (this.isMobile || this.isTablet) {
      // On mobile/tablet, toggle closes the sidebar
      this.closeSidebar.emit();
    } else {
      // On desktop, toggle expands/collapses
      this.isExpanded = !this.isExpanded;
      this.toggleSidebar.emit();
    }
  }

  onLinkClick() {
    // Close sidebar on mobile when a link is clicked
    if (this.isMobile) {
      this.closeSidebar.emit();
    }
  }
}
```

### Key Logic Points:

1. **Navigation Building:** `buildNavSections()` dynamically builds menu items based on user permissions and feature flags
2. **Reactive Updates:** Subscribes to `access.access$` to rebuild menu when permissions change
3. **Toggle Logic:** 
   - Desktop: Toggles `isExpanded` state
   - Mobile/Tablet: Emits `closeSidebar` event
4. **Link Click:** On mobile, closes sidebar when a navigation link is clicked

---

## 🏗️ HTML Template Structure

```html
<nav
  class="sidebar"
  [class.expanded]="isExpanded"
  [class.mobile]="isMobile"
  [class.tablet]="isTablet"
>
  <!-- Sidebar Header -->
  <div class="sidebar-header">
    <mat-icon class="menu-icon material-icons-outlined" (click)="toggle()">menu</mat-icon>
    <div *ngIf="isExpanded || isMobile" class="brand-section">
      <span class="logo-text">Amplify</span>
    </div>
    <button
      *ngIf="isMobile && isExpanded"
      class="close-button"
      (click)="closeSidebar.emit()"
      aria-label="Close sidebar"
    >
      <mat-icon class="material-icons-outlined">close</mat-icon>
    </button>
  </div>

  <!-- Navigation Sections -->
  <div class="nav-sections">
    <div *ngFor="let section of navSections" class="nav-section">
      <div *ngIf="section.title && (isExpanded || isMobile)" class="section-title">
        {{ section.title }}
      </div>
      <ul class="nav-links">
        <li
          *ngFor="let item of section.items"
          routerLinkActive="active"
          [routerLinkActiveOptions]="{ exact: item.route === '/dashboard' }"
        >
          <a [routerLink]="[item.route]" (click)="onLinkClick()">
            <mat-icon class="material-icons-outlined">{{ item.icon }}</mat-icon>
            <span *ngIf="isExpanded || isMobile">{{ item.label }}</span>
          </a>
        </li>
      </ul>
    </div>
  </div>

  <!-- Help icon only, anchored at the bottom -->
  <div class="sidebar-footer">
    <button
      class="help-icon-button"
      type="button"
      aria-label="Contact support or view documentation"
      matTooltip="Need help? Reach out to support or view documentation."
      matTooltipPosition="right"
    >
      <mat-icon class="help-icon">help_outline</mat-icon>
    </button>
  </div>
</nav>
```

### Template Key Points:

1. **Conditional Classes:** `expanded`, `mobile`, `tablet` classes control behavior
2. **Brand Section:** Only shows when `isExpanded || isMobile`
3. **Close Button:** Only shows on mobile when expanded
4. **Section Titles:** Only show when `isExpanded || isMobile`
5. **Menu Labels:** Only show when `isExpanded || isMobile`
6. **Active State:** Uses `routerLinkActive="active"` with exact matching for dashboard route

---

## 🎨 SCSS Styling Details

### Base Sidebar Styles

```scss
@use "styles/styles/breakpoints" as *;

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: var(--sidebar-collapsed-width);
  background: var(--surface);
  backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturation));
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturation));

  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, width 0.3s ease, background 0.45s ease;
  overflow: hidden;
  z-index: 100;

  // Desktop & Large LCD: Default behavior
  &.expanded {
    width: var(--sidebar-expanded-width);
  }

  // Tablet: Overlay behavior, collapsed by default
  &.tablet {
    width: 64px; // Always collapsed on tablet unless expanded
    transform: translateX(0);

    &.expanded {
      width: 240px;
      transform: translateX(0);
    }
  }

  // Mobile: Drawer pattern, hidden by default
  &.mobile {
    width: 280px;
    transform: translateX(-100%); // Hidden off-screen
    z-index: 101; // Above overlay
    // Use a solid, slightly softened surface on mobile for stronger text contrast.
    background: var(--surface-soft);

    &.expanded {
      transform: translateX(0); // Slide in
    }
  }

  // Hide text labels when collapsed (desktop only)
  &:not(.expanded):not(.mobile) .nav-links a span {
    display: none;
  }

  // Show tooltip on hover when collapsed (desktop only)
  &:not(.expanded):not(.mobile) .nav-links a:hover span {
    display: inline;
    position: absolute;
    left: calc(var(--sidebar-collapsed-width) + 8px);
    background: var(--surface);
    padding: 4px 8px;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    white-space: nowrap;
    z-index: 102;
  }
}
```

### Sidebar Header

```scss
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: clamp(0.75rem, 2vw, 1rem) clamp(1rem, 3vw, 1.25rem);
  font-weight: 600;
  color: var(--text-color);
  position: relative;
  height: clamp(56px, 8vh, 64px);
  box-shadow: 0 1px 0 rgba(15, 23, 42, 0.08);

  @include mobile {
    padding: clamp(0.75rem, 2vw, 1rem) clamp(1rem, 2vw, 1.25rem);
    height: clamp(56px, 8vh, 60px);
    box-shadow: none; // cleaner look on mobile
  }

  @include tablet {
    padding: 1rem clamp(1rem, 2.5vw, 1.25rem);
    height: 60px; // matches topbar tablet height
  }

  @include desktop {
    padding: 1.25rem 1.5rem;
    height: 64px; // matches topbar desktop height
  }

  @include large-lcd {
    padding: 1.5rem 2rem;
    height: clamp(68px, 8vh, 72px); // matches topbar large-lcd height
  }

  // When expanded, space between hamburger and brand
  .sidebar.expanded:not(.mobile) & {
    justify-content: space-between;
  }

  // When collapsed, keep hamburger in same left position
  .sidebar:not(.expanded):not(.mobile) & {
    justify-content: flex-start;
    padding-left: clamp(1rem, 2vw, 1.5rem);
    padding-right: clamp(1rem, 2vw, 1.5rem);

    @include large-lcd {
      padding-left: clamp(1rem, 2vw, 1.5rem);
      padding-right: clamp(1rem, 2vw, 1.5rem);
    }
  }
}
```

### Menu Icon

```scss
.menu-icon {
  position: relative;
  width: clamp(20px, 5vw, 24px);
  height: clamp(20px, 5vw, 24px);
  color: var(--text-color);
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s ease;
  padding: clamp(6px, 1.5vw, 8px);
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0; // Remove any auto margins

  @include mobile {
    width: 24px;
    height: 24px;
    padding: 6px;
  }

  @include large-lcd {
    width: 28px;
    height: 28px;
    padding: 10px;
    min-width: 48px;
    min-height: 48px;
  }

  &:hover {
    background: rgba(0, 191, 166, 0.1);
    color: var(--color-primary);
  }

  &:active {
    background: rgba(0, 191, 166, 0.15);
    transform: scale(0.95);
  }
}
```

### Close Button (Mobile Only)

```scss
.close-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(15, 23, 36, 0.05);
  border-radius: 8px;
  color: var(--text-color);
  cursor: pointer;
  transition: background 0.2s ease;

  @include mobile {
    display: flex;
  }

  @include tablet {
    display: none;
  }

  @include desktop {
    display: none;
  }

  &:hover {
    background: rgba(15, 23, 36, 0.1);
  }

  mat-icon {
    font-size: 20px;
  }
}
```

### Brand Section

```scss
.brand-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.1rem;
  flex: 1;

  @include mobile {
    align-items: flex-start;
    padding-left: 0.5rem;
  }
}

.logo-text {
  font-weight: 700;
  font-size: clamp(1rem, 3vw, 1.2rem);
  color: var(--text-color);
  letter-spacing: 0.5px;

  @include mobile {
    font-size: 1.1rem;
  }

  @include large-lcd {
    font-size: 1.4rem;
    letter-spacing: 0.75px;
  }
}
```

### Navigation Sections Container

```scss
.nav-sections {
  flex: 1;
  overflow-y: auto;
  padding: clamp(0.5rem, 2vw, 0.75rem) 0;
  box-shadow: 2px 0 0 rgba(15, 23, 42, 0.08);

  @include mobile {
    padding: 0.5rem 0;
  }

  @include large-lcd {
    padding: 1.25rem 0;
  }

  // Custom scrollbar
  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(13, 51, 55, 0.2);
    border-radius: 2px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }
}
```

### Navigation Section

```scss
.nav-section {
  margin-bottom: clamp(1rem, 3vw, 1.5rem);

  &:last-child {
    margin-bottom: 0;
  }

  @include mobile {
    margin-bottom: 1.25rem;
  }

  @include large-lcd {
    margin-bottom: 2.25rem;
  }
}
```

### Section Title

```scss
.section-title {
  font-size: clamp(0.7rem, 2vw, 0.75rem);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-color-muted);
  padding: clamp(0.5rem, 2vw, 0.75rem) clamp(0.75rem, 2vw, 1rem);
  margin-bottom: 0.5rem;
  opacity: 0.7;

  @include mobile {
    padding: 0.5rem 1rem;
  }

  @include large-lcd {
    font-size: 0.85rem;
    padding: 0.875rem 1.5rem;
    letter-spacing: 0.75px;
  }
}
```

### Navigation Links

```scss
.nav-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: clamp(0.25rem, 1vw, 0.5rem);
  padding: 0 clamp(0.5rem, 2vw, 0.75rem);
  background: transparent;

  @include mobile {
    gap: 0.25rem;
    padding: 0 0.5rem;
  }

  @include large-lcd {
    gap: 0.625rem;
    padding: 0 1.25rem;
  }
}

.nav-links li {
  margin-bottom: 0.25rem;
}

.nav-links a {
  display: flex;
  align-items: center;
  gap: clamp(0.75rem, 2vw, 1rem);
  text-decoration: none;
  color: var(--text-color-muted);
  padding: clamp(0.625rem, 2vw, 0.75rem) clamp(0.75rem, 2vw, 1rem);
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
  min-height: 44px; // Touch target
  overflow: hidden; // Prevent text from overflowing the highlight area

  @include mobile {
    // On mobile/overlay sidebar, use full text color for better contrast
    color: var(--text-color);
    gap: 1rem;
    padding: 0.75rem 1rem;
    min-height: 48px;
  }

  @include large-lcd {
    gap: 1.5rem;
    padding: 1rem 1.5rem;
    min-height: 56px;
  }

  mat-icon {
    width: clamp(18px, 4vw, 20px);
    height: clamp(18px, 4vw, 20px);
    font-size: clamp(18px, 4vw, 20px);
    flex-shrink: 0;

    @include mobile {
      width: 22px;
      height: 22px;
      font-size: 22px;
    }

    @include large-lcd {
      width: 26px;
      height: 26px;
      font-size: 26px;
    }
  }

  span {
    font-size: clamp(0.875rem, 2.5vw, 0.95rem);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    min-width: 0; // Allow flex shrinking

    @include mobile {
      font-size: 0.95rem;
    }

    @include large-lcd {
      font-size: 1.05rem;
      font-weight: 500;
    }
  }
}
```

### Navigation Link Hover & Active States

```scss
.nav-links a:hover,
.nav-links li.active a {
  background: rgba(0, 191, 166, 0.15);
  color: var(--color-primary);
}

.nav-links li.active a {
  background: rgba(0, 191, 166, 0.2);
  font-weight: 600;
}
```

### Sidebar Footer

```scss
.sidebar-footer {
  margin-top: auto;
  padding: clamp(0.75rem, 2.5vw, 1rem);
  display: flex;
  justify-content: flex-start;
  padding-left: clamp(1rem, 2vw, 1.5rem);
  padding-right: clamp(1rem, 2vw, 1.5rem);
  box-shadow: 2px 0 0 rgba(15, 23, 42, 0.08);
  background: transparent;

  @include large-lcd {
    padding: 1.25rem clamp(1rem, 2vw, 1.5rem);
  }

  // Ensure consistent left alignment in both collapsed and expanded states
  .sidebar:not(.mobile) & {
    justify-content: flex-start;
  }
}
```

### Help Icon Button

```scss
.help-icon {
  font-size: clamp(1.25rem, 3vw, 1.5rem);
  width: clamp(1.25rem, 3vw, 1.5rem);
  height: clamp(1.25rem, 3vw, 1.5rem);
  line-height: clamp(1.25rem, 3vw, 1.5rem);
  color: var(--color-primary);

  @include large-lcd {
    font-size: 1.75rem;
    width: 1.75rem;
    height: 1.75rem;
    line-height: 1.75rem;
  }
}

.help-icon-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: 1px solid rgba(13, 51, 55, 0.18);
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;

  &:hover,
  &:focus-visible {
    background: rgba(0, 191, 166, 0.08);
    border-color: rgba(0, 191, 166, 0.5);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  @include mobile {
    width: 36px;
    height: 36px;
  }

  @include large-lcd {
    width: 48px;
    height: 48px;
    border-width: 1.5px;
  }
}
```

---

## 🔄 Expansion/Collapse Logic

### Desktop Behavior

1. **Default State:** Collapsed (width: `--sidebar-collapsed-width`, typically 80px)
2. **Expanded State:** Expanded (width: `--sidebar-expanded-width`, typically 200px)
3. **Toggle:** Clicking menu icon toggles `isExpanded` state
4. **Transition:** Width animates with `transition: width 0.3s ease`

### Tablet Behavior

1. **Default State:** Collapsed (64px width), always visible
2. **Expanded State:** 240px width when expanded
3. **Toggle:** Clicking menu icon closes sidebar (emits `closeSidebar`)
4. **Overlay:** Sidebar overlays content, doesn't push it

### Mobile Behavior

1. **Default State:** Hidden off-screen (`transform: translateX(-100%)`)
2. **Expanded State:** Slides in (`transform: translateX(0)`)
3. **Toggle:** Clicking menu icon closes sidebar
4. **Backdrop:** Dark overlay appears behind sidebar when open
5. **Auto-close:** Clicking any nav link closes sidebar

### Section Visibility Logic

- **Section Titles:** Only visible when `isExpanded || isMobile`
- **Menu Labels:** Only visible when `isExpanded || isMobile`
- **Icons:** Always visible
- **Tooltips:** Show on hover when collapsed (desktop only)

---

## 🖱️ Hover Effects

### Menu Icon Hover

```scss
.menu-icon:hover {
  background: rgba(0, 191, 166, 0.1);  // Light teal background
  color: var(--color-primary);           // Primary color
}
```

**Effect:** Light teal background appears, icon color changes to primary

### Menu Icon Active

```scss
.menu-icon:active {
  background: rgba(0, 191, 166, 0.15);   // Slightly darker teal
  transform: scale(0.95);               // Slight scale down
}
```

**Effect:** Darker background, slight scale animation

### Navigation Link Hover

```scss
.nav-links a:hover {
  background: rgba(0, 191, 166, 0.15);   // Light teal background
  color: var(--color-primary);           // Primary color text
}
```

**Effect:** Entire link gets light teal background, text and icon change to primary color

### Active Navigation Link

```scss
.nav-links li.active a {
  background: rgba(0, 191, 166, 0.2);    // Stronger teal background
  font-weight: 600;                       // Bold text
  color: var(--color-primary);           // Primary color
}
```

**Effect:** Stronger background, bold text, primary color

### Close Button Hover

```scss
.close-button:hover {
  background: rgba(15, 23, 36, 0.1);     // Slightly darker background
}
```

**Effect:** Subtle background darkening

### Help Icon Button Hover

```scss
.help-icon-button:hover {
  background: rgba(0, 191, 166, 0.08);   // Light teal background
  border-color: rgba(0, 191, 166, 0.5); // Teal border
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); // Subtle shadow
}
```

**Effect:** Light teal background, teal border, shadow appears

### Collapsed Tooltip (Desktop Only)

When sidebar is collapsed and not on mobile:
- Hovering over a nav link shows the label as a tooltip
- Tooltip appears to the right of the sidebar
- Positioned absolutely at `left: calc(var(--sidebar-collapsed-width) + 8px)`
- White background with shadow
- `z-index: 102` (above sidebar)

---

## 🎨 Icon Colors & States

### Default State

- **Menu Icon:** `var(--text-color)` (typically `#0d3337`)
- **Nav Icons:** `var(--text-color-muted)` (typically `rgba(13, 51, 55, 0.65)`)
- **Help Icon:** `var(--color-primary)` (typically `#0d3337`)

### Hover State

- **Menu Icon:** `var(--color-primary)` with light teal background
- **Nav Icons:** `var(--color-primary)` with light teal background
- **Help Icon:** Remains `var(--color-primary)`, button gets teal background

### Active State

- **Active Nav Link Icon:** `var(--color-primary)` with stronger teal background
- **Active Nav Link Text:** `var(--color-primary)` with `font-weight: 600`

### Mobile State

- **Nav Icons:** `var(--text-color)` (full opacity for better contrast)
- **Nav Text:** `var(--text-color)` (full opacity)

### Icon Sizes

- **Menu Icon:**
  - Mobile: 24px × 24px
  - Desktop: 20-24px (clamped)
  - Large LCD: 28px × 28px

- **Nav Icons:**
  - Mobile: 22px × 22px
  - Desktop: 18-20px (clamped)
  - Large LCD: 26px × 26px

- **Help Icon:**
  - Mobile: 1.25-1.5rem (clamped)
  - Large LCD: 1.75rem

---

## 📑 Section Behavior

### Section Structure

Sections are defined in the `navSections` array:

```typescript
navSections: NavSection[] = [
  {
    title: 'Pages',
    items: [/* navigation items */]
  },
  {
    title: 'Account Pages',
    items: [/* account items */]
  }
]
```

### Section Title Display

- **Visibility:** Only shown when `isExpanded || isMobile`
- **Styling:** Uppercase, muted color, small font size
- **Spacing:** Margin bottom of `0.5rem` after title

### Section Spacing

- **Between Sections:** `clamp(1rem, 3vw, 1.5rem)` margin-bottom
- **Last Section:** No margin-bottom
- **Responsive:**
  - Mobile: `1.25rem`
  - Large LCD: `2.25rem`

### Section Items

- Items are rendered in a `<ul class="nav-links">` list
- Each item is a `<li>` with `routerLinkActive="active"`
- Active state is determined by current route matching

---

## 📱 Responsive Behavior

### Breakpoints

The component uses breakpoint mixins from `styles/breakpoints`:

- **Mobile:** `< 768px` OR height `< 600px`
- **Tablet:** `768px - 1023px`
- **Desktop:** `≥ 1024px`
- **Large LCD:** `≥ 1440px` (typically)

### Desktop (≥ 1024px)

- **Collapsed Width:** `var(--sidebar-collapsed-width)` (80px)
- **Expanded Width:** `var(--sidebar-expanded-width)` (200px)
- **Behavior:** Sidebar pushes content, can be expanded/collapsed
- **Labels:** Hidden when collapsed, shown when expanded
- **Tooltips:** Shown on hover when collapsed

### Tablet (768px - 1023px)

- **Collapsed Width:** 64px
- **Expanded Width:** 240px
- **Behavior:** Sidebar overlays content
- **Labels:** Hidden when collapsed, shown when expanded
- **Toggle:** Closes sidebar instead of toggling

### Mobile (< 768px or height < 600px)

- **Width:** 280px
- **Behavior:** Drawer pattern, slides in from left
- **Transform:** `translateX(-100%)` when hidden, `translateX(0)` when shown
- **Backdrop:** Dark overlay with blur appears behind sidebar
- **Labels:** Always visible when sidebar is open
- **Auto-close:** Clicking nav link or backdrop closes sidebar
- **Close Button:** Visible in header when expanded

### Large LCD (≥ 1440px)

- **Increased Padding:** All padding values scale up
- **Larger Icons:** Icon sizes increase
- **Larger Text:** Font sizes increase
- **More Spacing:** Gaps and margins increase

---

## 🔗 Integration with Layout

### Dashboard Layout Component

The sidebar is integrated into the dashboard layout:

```typescript
<app-sidebar
  [isExpanded]="isSidebarExpanded"
  [isMobile]="isMobile"
  [isTablet]="isTablet"
  (toggleSidebar)="toggleSidebar()"
  (closeSidebar)="closeSidebar()"
></app-sidebar>
```

### Layout State Management

```typescript
export class DashboardLayoutComponent {
  isSidebarExpanded = false;
  isMobile = false;
  isTablet = false;

  private checkScreenSize() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const isPhoneLikeHeight = height < 600;

    this.isMobile = width < 768 || isPhoneLikeHeight;
    this.isTablet = !this.isMobile && width >= 768 && width < 1024;
  }

  toggleSidebar() {
    this.isSidebarExpanded = !this.isSidebarExpanded;
  }

  closeSidebar() {
    this.isSidebarExpanded = false;
  }
}
```

### Content Area Adjustment

The main content area adjusts its margin based on sidebar state:

```scss
.dashboard-main {
  margin-left: var(--sidebar-collapsed-width);
  width: calc(100% - var(--sidebar-collapsed-width));

  &.sidebar-expanded {
    margin-left: var(--sidebar-expanded-width);
    width: calc(100% - var(--sidebar-expanded-width));
  }

  @include tablet {
    margin-left: 0;
    width: 100%;
  }

  @include mobile {
    margin-left: 0;
    width: 100%;
  }
}
```

### Mobile Overlay Backdrop

```html
<div
  *ngIf="isMobile && isSidebarExpanded"
  class="sidebar-overlay"
  (click)="closeSidebar()"
  aria-label="Close sidebar"
></div>
```

```scss
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99; /* Below sidebar (100) but above content */
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}
```

---

## 🎨 Theme Variables Required

### CSS Variables (from `theme.css`)

```css
/* Sidebar Dimensions */
--sidebar-collapsed-width: 80px;
--sidebar-expanded-width: 200px;

/* Colors */
--color-primary: #0d3337;
--color-primary-rgb: 13, 51, 55;
--text-color: #0d3337;
--text-color-muted: rgba(13, 51, 55, 0.65);
--text-color-invert: #ffffff;

/* Surfaces */
--surface: #ffffff;
--surface-soft: rgba(255, 255, 255, 0.95);

/* Glassmorphism */
--glass-blur: 12px;
--glass-saturation: 180%;
--glass-border: 1px solid rgba(13, 51, 55, 0.08);
--glass-shadow: 0 2px 8px rgba(13, 51, 55, 0.04);

/* Border Radius */
--border-radius: 14px;
```

### Large LCD Overrides

```css
@include large-lcd {
  --sidebar-collapsed-width: 100px;
  --sidebar-expanded-width: 260px;
}
```

---

## 📝 Summary Checklist

### Component Setup
- [ ] Create component files (`.ts`, `.html`, `.scss`)
- [ ] Import required Angular modules
- [ ] Import shared services and models
- [ ] Set up component inputs/outputs

### Template
- [ ] Add sidebar `<nav>` element with conditional classes
- [ ] Add sidebar header with menu icon and brand
- [ ] Add navigation sections loop
- [ ] Add section titles (conditional)
- [ ] Add navigation links with icons and labels
- [ ] Add sidebar footer with help icon
- [ ] Add routerLinkActive for active states

### Styling
- [ ] Base sidebar styles (position, dimensions, transitions)
- [ ] Desktop expanded/collapsed states
- [ ] Tablet overlay behavior
- [ ] Mobile drawer behavior
- [ ] Header styles with responsive padding
- [ ] Menu icon hover/active states
- [ ] Navigation link styles
- [ ] Hover and active states for links
- [ ] Section title styles
- [ ] Footer and help icon styles
- [ ] Custom scrollbar styles
- [ ] Collapsed tooltip styles

### Logic
- [ ] Build navigation sections method
- [ ] Permission-based menu item filtering
- [ ] Toggle method (desktop vs mobile/tablet)
- [ ] Link click handler (mobile auto-close)
- [ ] Access subscription for reactive updates

### Integration
- [ ] Add to dashboard layout
- [ ] Set up responsive state management
- [ ] Add mobile overlay backdrop
- [ ] Adjust content area margins
- [ ] Handle window resize events

### Testing
- [ ] Test desktop expand/collapse
- [ ] Test tablet overlay behavior
- [ ] Test mobile drawer behavior
- [ ] Test hover effects
- [ ] Test active route highlighting
- [ ] Test tooltips when collapsed
- [ ] Test responsive breakpoints
- [ ] Test permission-based menu visibility

---

## 🎯 Key Implementation Notes

1. **Material Icons:** Use `material-icons-outlined` class for outlined style
2. **RouterLinkActive:** Use exact matching for dashboard route: `{ exact: item.route === '/dashboard' }`
3. **Responsive Detection:** Check both width and height for mobile detection
4. **Z-Index Layers:** Sidebar (100), Overlay (99), Tooltip (102)
5. **Transitions:** Use `0.3s ease` for width/transform, `0.2s ease` for hover effects
6. **Touch Targets:** Minimum 44px height for mobile accessibility
7. **Glassmorphism:** Use `backdrop-filter` with blur and saturation
8. **Color System:** Use CSS variables for all colors to support theming
9. **Accessibility:** Include `aria-label` attributes, proper button semantics
10. **Performance:** Use `takeUntilDestroyed` for subscription cleanup

---

This guide covers every aspect of the side menu component. Follow it step-by-step to achieve an exact replication.
