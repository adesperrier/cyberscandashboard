document.addEventListener('DOMContentLoaded', function() {
    initSmoothScroll();
    initNavbarHighlight();
    initScrollReveal();
    initAOS();
    initOSTabs();
    initCopyButtons();
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

// OS Tabs for installation section
function initOSTabs() {
    const tabs = document.querySelectorAll('.os-tab');
    const contents = document.querySelectorAll('.os-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const os = this.getAttribute('data-os');

            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            const target = document.getElementById('os-' + os);
            if (target) target.classList.add('active');
        });
    });
}

// Copy to clipboard for code blocks
function initCopyButtons() {
    const copyBtns = document.querySelectorAll('.copy-btn');

    copyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const codeEl = this.closest('.code-block').querySelector('code');
            const text = codeEl ? codeEl.innerText : '';

            if (!text) return;

            navigator.clipboard.writeText(text).then(() => {
                this.classList.add('copied');
                this.innerHTML = '<i class="bi bi-clipboard-check"></i>';
                setTimeout(() => {
                    this.classList.remove('copied');
                    this.innerHTML = '<i class="bi bi-clipboard"></i>';
                }, 2000);
            }).catch(() => {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);

                this.classList.add('copied');
                this.innerHTML = '<i class="bi bi-clipboard-check"></i>';
                setTimeout(() => {
                    this.classList.remove('copied');
                    this.innerHTML = '<i class="bi bi-clipboard"></i>';
                }, 2000);
            });
        });
    });
}
