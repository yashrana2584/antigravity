/**
 * Portfolio Interactive Logic & DOM Rendering
 */

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  renderPersonalData();
  renderAboutSection();
  renderSkillsSection();
  renderProjectsSection();
  renderTimelineSection();
  renderContactSection();
  initTypewriter();
  initMobileMenu();
  initContactForm();
  initCopyEmail();
  initLucide();
});

// Helper to refresh Lucide icons
function initLucide() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

/**
 * Theme Management (Dark / Light Mode)
 */
function initTheme() {
  const themeToggleBtn = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");
  const appBody = document.getElementById("app-body");

  // Determine initial theme
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const currentTheme = savedTheme ? savedTheme : (prefersDark ? "dark" : "dark"); // Default dark modern

  applyTheme(currentTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const isDark = document.documentElement.classList.contains("dark");
      const newTheme = isDark ? "light" : "dark";
      applyTheme(newTheme);
      localStorage.setItem("theme", newTheme);
    });
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
      document.documentElement.classList.remove("light");
      appBody.className = "min-h-screen bg-slate-900 text-slate-100 transition-colors duration-300 selection:bg-brand-500 selection:text-white bg-mesh-dark";
      if (themeIcon) {
        themeIcon.setAttribute("data-lucide", "sun");
      }
    } else {
      document.documentElement.classList.remove("dark");
      document.documentElement.classList.add("light");
      appBody.className = "min-h-screen bg-slate-50 text-slate-800 transition-colors duration-300 selection:bg-brand-500 selection:text-white bg-mesh-light";
      if (themeIcon) {
        themeIcon.setAttribute("data-lucide", "moon");
      }
    }
    initLucide();
  }
}

/**
 * Populate Personal Info & Hero Section
 */
function renderPersonalData() {
  const { personal, socials } = PORTFOLIO_DATA;

  // Name & Initials
  const nameParts = personal.name.split(" ");
  const initials = nameParts.map(n => n[0]).join("").toUpperCase();

  const navInitials = document.getElementById("nav-initials");
  if (navInitials) navInitials.textContent = initials || "AM";

  const navName = document.getElementById("nav-name");
  if (navName) navName.textContent = personal.name;

  const heroName = document.getElementById("hero-name");
  if (heroName) heroName.textContent = personal.name;

  const heroTagline = document.getElementById("hero-tagline");
  if (heroTagline) heroTagline.textContent = personal.tagline;

  const heroAvatar = document.getElementById("hero-avatar");
  if (heroAvatar && personal.avatar) {
    heroAvatar.src = personal.avatar;
    heroAvatar.alt = `${personal.name} Avatar`;
  }

  const resumeBtn = document.getElementById("hero-resume-btn");
  if (resumeBtn && personal.resumeUrl) {
    resumeBtn.href = personal.resumeUrl;
    if (personal.resumeUrl.endsWith(".pdf")) {
      resumeBtn.setAttribute("download", "resume.pdf");
    }
  }

  // Social Links in Hero
  const heroSocials = document.getElementById("hero-socials");
  if (heroSocials) {
    heroSocials.innerHTML = socials.map(s => `
      <a href="${s.url}" target="_blank" rel="noopener noreferrer" aria-label="${s.name}"
         class="w-10 h-10 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-brand-400 border border-slate-700/60 flex items-center justify-center transition-all hover:scale-105 shadow-sm">
        <i data-lucide="${s.icon}" class="w-4 h-4"></i>
      </a>
    `).join("");
  }

  // Footer Name & Year
  const footerName = document.getElementById("footer-name");
  if (footerName) footerName.textContent = personal.name;

  const footerYear = document.getElementById("footer-year");
  if (footerYear) footerYear.textContent = new Date().getFullYear();
}

/**
 * Typewriter Effect for Hero
 */
function initTypewriter() {
  const typewriterElem = document.getElementById("typewriter-text");
  if (!typewriterElem) return;

  const roles = PORTFOLIO_DATA.personal.typingRoles || [PORTFOLIO_DATA.personal.role];
  let roleIdx = 0;
  let charIdx = 0;
  let isDeleting = false;
  let typingSpeed = 90;

  function typeStep() {
    const currentRole = roles[roleIdx];

    if (isDeleting) {
      typewriterElem.textContent = currentRole.substring(0, charIdx - 1);
      charIdx--;
      typingSpeed = 45;
    } else {
      typewriterElem.textContent = currentRole.substring(0, charIdx + 1);
      charIdx++;
      typingSpeed = 90;
    }

    if (!isDeleting && charIdx === currentRole.length) {
      // Pause at full word
      isDeleting = true;
      typingSpeed = 1800;
    } else if (isDeleting && charIdx === 0) {
      isDeleting = false;
      roleIdx = (roleIdx + 1) % roles.length;
      typingSpeed = 400;
    }

    setTimeout(typeStep, typingSpeed);
  }

  setTimeout(typeStep, 600);
}

/**
 * About Me Section
 */
function renderAboutSection() {
  const { about } = PORTFOLIO_DATA;

  // Bio Paragraphs
  const storyContainer = document.getElementById("about-story");
  if (storyContainer) {
    storyContainer.innerHTML = about.story.map(p => `<p>${p}</p>`).join("");
  }

  // Quick Stats
  const statsContainer = document.getElementById("about-stats");
  if (statsContainer) {
    statsContainer.innerHTML = about.stats.map(s => `
      <div class="text-center p-3 rounded-2xl bg-slate-800/40 border border-slate-700/50">
        <p class="text-2xl sm:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-cyan-400">${s.value}</p>
        <p class="text-[11px] sm:text-xs text-slate-400 mt-1 font-medium">${s.label}</p>
      </div>
    `).join("");
  }

  // Highlights Pillars
  const highlightsContainer = document.getElementById("about-highlights");
  if (highlightsContainer) {
    highlightsContainer.innerHTML = about.highlights.map(h => `
      <div class="glass-card rounded-2xl p-5 border border-slate-700/60 flex items-start gap-4">
        <div class="w-10 h-10 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center flex-shrink-0 mt-0.5">
          <i data-lucide="${h.icon}" class="w-5 h-5"></i>
        </div>
        <div>
          <h4 class="text-sm sm:text-base font-bold text-white">${h.title}</h4>
          <p class="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">${h.description}</p>
        </div>
      </div>
    `).join("");
  }
}

/**
 * Skills Section
 */
function renderSkillsSection() {
  const { skills } = PORTFOLIO_DATA;
  const container = document.getElementById("skills-container");
  if (!container) return;

  container.innerHTML = skills.map(category => `
    <div class="glass-card rounded-3xl p-6 sm:p-7 border border-slate-700/60 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-700/60">
          <h3 class="font-bold text-lg text-white flex items-center gap-2">
            <span>${category.category}</span>
          </h3>
          <span class="text-xs font-mono px-2.5 py-1 rounded-md bg-brand-500/10 text-brand-400 font-semibold">
            ${category.items.length} Techs
          </span>
        </div>

        <div class="space-y-4">
          ${category.items.map(skill => `
            <div class="space-y-1.5">
              <div class="flex justify-between text-xs sm:text-sm">
                <span class="font-medium text-slate-200">${skill.name}</span>
                <span class="text-slate-400 font-mono text-xs">${skill.level}%</span>
              </div>
              <div class="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div class="h-full rounded-full bg-gradient-to-r from-brand-500 to-cyan-400 transition-all duration-1000" style="width: ${skill.level}%;"></div>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `).join("");
}

/**
 * Featured Projects Section with Filtering
 */
function renderProjectsSection() {
  const container = document.getElementById("projects-grid");
  const filterBtns = document.querySelectorAll("#project-filters button");
  if (!container) return;

  let activeFilter = "all";

  function renderList() {
    const projects = PORTFOLIO_DATA.projects.filter(p => {
      if (activeFilter === "all") return true;
      return p.category === activeFilter;
    });

    if (projects.length === 0) {
      container.innerHTML = `
        <div class="col-span-full text-center py-12 text-slate-400 text-sm">
          No projects found in this category.
        </div>
      `;
      return;
    }

    container.innerHTML = projects.map(p => `
      <div class="glass-card rounded-3xl overflow-hidden border border-slate-700/60 flex flex-col justify-between group">
        <div>
          <!-- Project Preview Image -->
          <div class="relative h-48 sm:h-52 overflow-hidden bg-slate-800">
            <img 
              src="${p.image}" 
              alt="${p.title}" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/20 to-transparent"></div>
            
            <!-- Category Tag -->
            <span class="absolute top-3 left-3 px-3 py-1 rounded-full text-[11px] font-semibold tracking-wide bg-slate-900/80 text-brand-300 backdrop-blur-md border border-slate-700/80">
              ${p.categoryName}
            </span>

            ${p.featured ? `
              <span class="absolute top-3 right-3 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-brand-500 text-white flex items-center gap-1 shadow-md">
                <i data-lucide="star" class="w-3 h-3 fill-current"></i>
                <span>Featured</span>
              </span>
            ` : ""}
          </div>

          <!-- Project Details -->
          <div class="p-6 space-y-3">
            <h3 class="text-lg font-bold text-white group-hover:text-brand-400 transition-colors">
              ${p.title}
            </h3>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed line-clamp-3">
              ${p.description}
            </p>

            <!-- Tech Tags -->
            <div class="flex flex-wrap gap-1.5 pt-2">
              ${p.tags.map(t => `
                <span class="text-[11px] font-mono px-2 py-0.5 rounded-md bg-slate-800/90 text-slate-300 border border-slate-700/50">
                  ${t}
                </span>
              `).join("")}
            </div>
          </div>
        </div>

        <!-- Action Links -->
        <div class="px-6 pb-6 pt-2 flex items-center gap-3 border-t border-slate-800/60 mt-4">
          <a href="${p.liveUrl}" target="_blank" rel="noopener noreferrer"
             class="flex-1 py-2 px-3 rounded-xl text-xs font-semibold bg-brand-600/90 hover:bg-brand-600 text-white text-center flex items-center justify-center gap-1.5 transition-all">
            <span>Live Demo</span>
            <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
          </a>
          <a href="${p.githubUrl}" target="_blank" rel="noopener noreferrer"
             class="py-2 px-3 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center justify-center gap-1.5 transition-all">
            <i data-lucide="github" class="w-3.5 h-3.5"></i>
            <span>Code</span>
          </a>
        </div>
      </div>
    `).join("");

    initLucide();
  }

  // Filter Buttons Interaction
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => {
        b.classList.remove("bg-brand-600", "text-white", "shadow-md");
        b.classList.add("bg-slate-800", "text-slate-300");
      });

      btn.classList.add("bg-brand-600", "text-white", "shadow-md");
      btn.classList.remove("bg-slate-800", "text-slate-300");

      activeFilter = btn.getAttribute("data-filter");
      renderList();
    });
  });

  renderList();
}

/**
 * Experience & Education Timeline
 */
function renderTimelineSection() {
  const container = document.getElementById("timeline-container");
  if (!container) return;

  const { timeline } = PORTFOLIO_DATA;

  container.innerHTML = timeline.map(item => {
    const isWork = item.type === "work";
    const iconName = isWork ? "briefcase" : "graduation-cap";

    return `
      <div class="relative group">
        <!-- Bullet Marker -->
        <div class="absolute -left-[35px] sm:-left-[43px] top-1.5 w-7 h-7 rounded-full bg-slate-900 border-2 border-brand-500 flex items-center justify-center text-brand-400 group-hover:scale-110 group-hover:bg-brand-500 group-hover:text-white transition-all shadow-md shadow-brand-500/20">
          <i data-lucide="${iconName}" class="w-3.5 h-3.5"></i>
        </div>

        <!-- Card Content -->
        <div class="glass-card rounded-2xl p-5 sm:p-6 border border-slate-700/60 space-y-2">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 sm:gap-4">
            <div>
              <h3 class="text-base sm:text-lg font-bold text-white">${item.role}</h3>
              <p class="text-xs sm:text-sm text-brand-400 font-medium">${item.company} &bull; <span class="text-slate-400">${item.location}</span></p>
            </div>
            <span class="inline-block text-[11px] font-mono px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700/60 self-start sm:self-auto">
              ${item.period}
            </span>
          </div>
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed pt-1">
            ${item.description}
          </p>
        </div>
      </div>
    `;
  }).join("");
}

/**
 * Contact Details & Socials
 */
function renderContactSection() {
  const { personal, socials } = PORTFOLIO_DATA;

  const contactLocation = document.getElementById("contact-location");
  if (contactLocation) contactLocation.textContent = personal.location;

  const contactEmail = document.getElementById("contact-email");
  if (contactEmail) contactEmail.textContent = personal.email;

  const contactSocials = document.getElementById("contact-socials");
  if (contactSocials) {
    contactSocials.innerHTML = socials.map(s => `
      <a href="${s.url}" target="_blank" rel="noopener noreferrer" aria-label="${s.name}"
         class="w-9 h-9 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-brand-400 border border-slate-700/60 flex items-center justify-center transition-all hover:scale-105">
        <i data-lucide="${s.icon}" class="w-4 h-4"></i>
      </a>
    `).join("");
  }
}

/**
 * Mobile Navigation Drawer Toggle
 */
function initMobileMenu() {
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const navLinks = document.querySelectorAll(".mobile-nav-link");

  if (!menuBtn || !mobileMenu) return;

  menuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("hidden");
  });

  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      mobileMenu.classList.add("hidden");
    });
  });

  // Close on outside click
  document.addEventListener("click", (e) => {
    if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
      mobileMenu.classList.add("hidden");
    }
  });
}

/**
 * 1-Click Copy Email to Clipboard
 */
function initCopyEmail() {
  const copyBtn = document.getElementById("copy-email-btn");
  const copyBtnText = document.getElementById("copy-btn-text");

  if (!copyBtn) return;

  copyBtn.addEventListener("click", async () => {
    const email = PORTFOLIO_DATA.personal.email;
    try {
      await navigator.clipboard.writeText(email);
      if (copyBtnText) copyBtnText.textContent = "Copied!";
      showToast(`Email copied: ${email}`);

      setTimeout(() => {
        if (copyBtnText) copyBtnText.textContent = "Copy";
      }, 2500);
    } catch (err) {
      showToast("Unable to copy to clipboard", "error");
    }
  });
}

/**
 * Contact Form Mock Handler
 */
function initContactForm() {
  const form = document.getElementById("contact-form");
  const submitBtn = document.getElementById("form-submit-btn");
  const submitLabel = document.getElementById("submit-btn-label");

  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("form-name").value.trim();
    const email = document.getElementById("form-email").value.trim();
    const subject = document.getElementById("form-subject").value.trim();
    const message = document.getElementById("form-message").value.trim();

    if (!name || !email || !message) {
      showToast("Please fill out all required fields.", "error");
      return;
    }

    // UI Loading state
    if (submitBtn) submitBtn.disabled = true;
    if (submitLabel) submitLabel.textContent = "Sending...";

    setTimeout(() => {
      showToast(`Thanks ${name}! Your message has been sent successfully.`);
      form.reset();
      if (submitBtn) submitBtn.disabled = false;
      if (submitLabel) submitLabel.textContent = "Send Message";
    }, 900);
  });
}

/**
 * Toast Notification Component
 */
let toastTimeout = null;
function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  const toastMsg = document.getElementById("toast-message");
  const iconContainer = document.getElementById("toast-icon-container");

  if (!toast || !toastMsg) return;

  toastMsg.textContent = message;

  if (iconContainer) {
    if (type === "error") {
      iconContainer.className = "w-8 h-8 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center flex-shrink-0";
      iconContainer.innerHTML = '<i data-lucide="alert-circle" class="w-4 h-4"></i>';
    } else {
      iconContainer.className = "w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0";
      iconContainer.innerHTML = '<i data-lucide="check" class="w-4 h-4"></i>';
    }
    initLucide();
  }

  toast.classList.remove("hide");
  toast.classList.add("show");

  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
    toast.classList.add("hide");
  }, 3500);
}
