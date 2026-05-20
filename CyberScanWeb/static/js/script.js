document.addEventListener('DOMContentLoaded', function() {
    initSmoothScroll();
    initNavbarHighlight();
    initScrollReveal();
    initAOS();
});

// Smooth scroll pour les liens internes
function initSmoothScroll() {
    const scrollLinks = document.querySelectorAll('.scroll-link');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                document.querySelector('.navbar-collapse').classList.remove('show');
            }
        });
    });
}

// Navbar highlight basé sur scroll
function initNavbarHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.scroll-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// Révélation des sections au scroll (Intersection Observer)
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const elementsToObserve = document.querySelectorAll(
        '.feature-card, .tech-badge, .screenshot-card, .installation-step, .roadmap-card'
    );

    elementsToObserve.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
}

// Animations légères au scroll (AOS style)
function initAOS() {
    const items = document.querySelectorAll('[data-aos]');
    if (items.length === 0) return;

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const aosType = entry.target.getAttribute('data-aos');
                entry.target.classList.add('aos-animate', aosType);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    items.forEach(item => observer.observe(item));
}

// Débounce helper pour les événements
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Gestion du scroll pour effets parallax légers
window.addEventListener('scroll', debounce(() => {
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
        const scrollPosition = window.scrollY;
        heroBackground.style.transform = `translateY(${scrollPosition * 0.5}px)`;
    }
}, 10));

// Animation du badge au scroll
const observeBadge = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
        }
    });
}, { threshold: 0.5 });

const badge = document.querySelector('.hero-badge');
if (badge) {
    badge.style.opacity = '0';
    observeBadge.observe(badge);
}

// Performance: Lazy load images (si nécessaire)
if ('IntersectionObserver' in window) {
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        observer.observe(img);
    });
}

// ==================== INSTALLATION FUNCTIONS ====================

// Copy to clipboard with visual feedback
function copyToClipboard(text) {
    // Use modern Clipboard API
    navigator.clipboard.writeText(text).then(() => {
        showCopyFeedback(event.target);
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showCopyFeedback(event.target);
    });
}

// Show visual feedback after copying
function showCopyFeedback(element) {
    const originalText = element.innerHTML;
    element.innerHTML = '<i class="bi bi-check-circle"></i> Copié !';
    element.style.backgroundColor = 'rgba(0, 255, 136, 0.2)';
    
    setTimeout(() => {
        element.innerHTML = originalText;
        element.style.backgroundColor = '';
    }, 2000);
}

// Auto-detect OS and select appropriate tab
function detectAndSelectOS() {
    const userAgent = navigator.userAgent;
    let osTab = 'windows-tab';
    
    if (userAgent.includes('Windows')) {
        osTab = 'windows-tab';
    } else if (userAgent.includes('Linux')) {
        osTab = 'linux-tab';
    } else if (userAgent.includes('Mac')) {
        osTab = 'mac-tab';
    }
    
    const tab = document.getElementById(osTab);
    if (tab) {
        const bsTab = new bootstrap.Tab(tab);
        bsTab.show();
    }
}

// Check Python (basic check message)
function checkPython() {
    alert('Pour vérifier votre version de Python, ouvrez votre terminal et tapez:\n\npython --version\n\nOu sur Linux/Mac:\npython3 --version\n\nVous devez avoir Python 3.10 ou plus récent.');
}

// Initialize installation section
function initInstallationSection() {
    // Auto-select OS on page load
    window.addEventListener('load', () => {
        setTimeout(detectAndSelectOS, 500);
    });
    
    // Add copy functionality to all code blocks
    const copyButtons = document.querySelectorAll('.btn-copy, .btn-copy-code');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const codeBlock = this.closest('.code-block') || this.closest('.code-block-quick');
            if (codeBlock) {
                const code = codeBlock.querySelector('code').textContent;
                copyToClipboard(code);
            }
        });
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initInstallationSection();
});
