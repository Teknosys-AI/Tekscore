/**
 * Dashboard Sidebar - Click to Toggle (Based on Guide)
 * Handles expand/collapse, state persistence, and responsive behavior
 */

(function() {
    'use strict';

    // Get sidebar elements
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarTLogo = document.getElementById('sidebarTLogo');
    const closeButton = document.getElementById('closeButton');
    const wrapper = document.getElementById('wrapper');
    const contentWrapper = document.querySelector('.sidebar-content-wrapper');
    const sidebarOverlay = document.createElement('div');
    sidebarOverlay.className = 'sidebar-overlay';
    document.body.appendChild(sidebarOverlay);

    // Check if sidebar exists
    if (!sidebar) {
        return;
    }
    
    // Add click handler to T logo to toggle sidebar
    if (sidebarTLogo) {
        sidebarTLogo.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleSidebar();
        });
    }

    // Detect screen size
    function isMobile() {
        return window.innerWidth < 768;
    }

    function isTablet() {
        return window.innerWidth >= 768 && window.innerWidth < 1024;
    }

    // Get initial state from localStorage (default: collapsed)
    const isExpanded = localStorage.getItem('sidebarExpanded') === 'true';
    
    // Set initial state
    if (isExpanded && !isMobile()) {
        sidebar.classList.add('expanded');
        if (wrapper) {
            wrapper.classList.add('sidebar-expanded');
        }
    }

    // Toggle sidebar function
    function toggleSidebar() {
        if (isMobile()) {
            // On mobile, toggle opens/closes the sidebar
            sidebar.classList.toggle('expanded');
            if (sidebar.classList.contains('expanded')) {
                sidebarOverlay.classList.add('active');
            } else {
                sidebarOverlay.classList.remove('active');
            }
        } else {
            // On desktop/tablet, toggle expands/collapses
            sidebar.classList.toggle('expanded');
            const isNowExpanded = sidebar.classList.contains('expanded');
            
            // Update wrapper class for CSS selector
            if (wrapper) {
                if (isNowExpanded) {
                    wrapper.classList.add('sidebar-expanded');
                } else {
                    wrapper.classList.remove('sidebar-expanded');
                }
            }
            
            // Save state to localStorage
            localStorage.setItem('sidebarExpanded', isNowExpanded.toString());
        }
    }

    // Close sidebar function
    function closeSidebar() {
        sidebar.classList.remove('expanded');
        sidebarOverlay.classList.remove('active');
        if (wrapper) {
            wrapper.classList.remove('sidebar-expanded');
        }
        if (!isMobile()) {
            localStorage.setItem('sidebarExpanded', 'false');
        }
    }

    // Toggle button click event
    sidebarToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        toggleSidebar();
    });

    // Close button click event
    if (closeButton) {
        closeButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeSidebar();
        });
    }

    // Close sidebar on overlay click (mobile)
    sidebarOverlay.addEventListener('click', function() {
        if (isMobile()) {
            closeSidebar();
        }
    });

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (isMobile()) {
                // On mobile, close sidebar if expanded
                if (sidebar.classList.contains('expanded')) {
                    sidebarOverlay.classList.add('active');
                }
            } else {
                // On desktop/tablet, remove mobile overlay
                sidebarOverlay.classList.remove('active');
            }
        }, 250);
    });

    // Set active menu item based on current page
    function setActiveMenuItem() {
        const currentPath = window.location.pathname;
        const menuLinks = sidebar.querySelectorAll('.nav-link');
        
        menuLinks.forEach(function(link) {
            try {
                const linkPath = new URL(link.href).pathname;
                const listItem = link.closest('li');
                if (linkPath === currentPath || 
                    (currentPath.includes(linkPath) && linkPath !== '/')) {
                    if (listItem) {
                        listItem.classList.add('active');
                    }
                } else {
                    if (listItem) {
                        listItem.classList.remove('active');
                    }
                }
            } catch (e) {
                // Handle invalid URLs gracefully
                console.warn('Invalid URL in sidebar link:', link.href);
            }
        });
    }

    // Close sidebar on link click (mobile)
    const navLinks = sidebar.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (isMobile()) {
                closeSidebar();
            }
        });
    });

    // Initialize active menu item on page load
    document.addEventListener('DOMContentLoaded', function() {
        setActiveMenuItem();
        
        // Set current year in footer (if exists)
        const yearElement = document.getElementById('year');
        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    });

    // Handle keyboard navigation (ESC to close on mobile)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isMobile()) {
            if (sidebar.classList.contains('expanded')) {
                closeSidebar();
            }
        }
    });

    // Smooth scroll for sidebar
    if (sidebar) {
        sidebar.style.scrollBehavior = 'smooth';
    }

})();
