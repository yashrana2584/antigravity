/**
 * Personal Portfolio Configuration & Data
 * Easily customize your portfolio by modifying the values in this file!
 */

const PORTFOLIO_DATA = {
  // General & Personal Information
  personal: {
    name: "Yash Rana",
    role: "Full-Stack Developer & Problem Solver",
    tagline: "Building scalable web applications, modern user interfaces, and intuitive digital experiences.",
    avatar: "https://img.magnific.com/premium-photo/memoji-emoji-handsome-smiling-man-white-background_826801-6987.jpg?semt=ais_hybrid&w=740&q=80",
    location: "San Francisco, CA (Open to Remote)",
    email: "ranayash2584@gmail.com",
    availableForHire: true,
    resumeUrl: "#resume", // Replace with your resume link or file path (e.g. 'resume.pdf')
    typingRoles: [
      "Full-Stack Developer",
      "UI/UX Enthusiast",
      "Open Source Contributor",
      "Cloud & API Architect"
    ]
  },

  // Social Links
  socials: [
    { name: "GitHub", icon: "github", url: "https://github.com/yashrana2584" },
    { name: "LinkedIn", icon: "linkedin", url: "https://linkedin.com" },
    { name: "Twitter / X", icon: "twitter", url: "https://twitter.com" },
    { name: "Email", icon: "mail", url: "mailto:ranayash2584@gmail.com" }
  ],

  // About Me Section
  about: {
    story: [
      "Hello! I'm a passionate developer who loves transforming complex problems into elegant, user-centric software solutions.",
      "With a strong foundation in modern web technologies, I specialize in crafting performant frontend interfaces and robust backend architectures. When I'm not writing code, you can find me exploring new tech stacks, contributing to open-source projects, or sharing learnings with the tech community."
    ],
    stats: [
      { label: "Years of Experience", value: "3+" },
      { label: "Projects Completed", value: "25+" },
      { label: "Satisfied Clients / Teams", value: "15+" },
      { label: "GitHub Contributions", value: "1,200+" }
    ],
    highlights: [
      {
        icon: "code",
        title: "Clean Architecture",
        description: "Writing maintainable, scalable, and well-tested code that adheres to industry best practices."
      },
      {
        icon: "layout",
        title: "Responsive Design",
        description: "Pixel-perfect mobile-first designs optimized for accessibility, speed, and smooth UX."
      },
      {
        icon: "zap",
        title: "Fast Performance",
        description: "Optimized bundle sizes, SEO-friendly structures, and blazing-fast loading speeds."
      },
      {
        icon: "git-pull-request",
        title: "Collaborative Mindset",
        description: "Experienced with agile sprints, code reviews, cross-functional collaboration, and CI/CD."
      }
    ]
  },

  // Skills Categorized
  skills: [
    {
      category: "Frontend",
      items: [
        { name: "HTML5 / CSS3", level: 95 },
        { name: "JavaScript (ES6+)", level: 90 },
        { name: "TypeScript", level: 85 },
        { name: "React / Next.js", level: 88 },
        { name: "Tailwind CSS", level: 92 },
        { name: "Vue.js", level: 75 }
      ]
    },
    {
      category: "Backend & Database",
      items: [
        { name: "Node.js / Express", level: 88 },
        { name: "Python / FastAPI", level: 82 },
        { name: "PostgreSQL", level: 85 },
        { name: "MongoDB", level: 80 },
        { name: "RESTful & GraphQL APIs", level: 90 },
        { name: "Redis", level: 72 }
      ]
    },
    {
      category: "Tools & DevOps",
      items: [
        { name: "Git & GitHub", level: 92 },
        { name: "Docker", level: 78 },
        { name: "AWS / Vercel", level: 80 },
        { name: "Jest & Cypress", level: 75 },
        { name: "Figma", level: 70 },
        { name: "Linux / Shell", level: 82 }
      ]
    }
  ],

  // Featured Projects
  projects: [
    {
      id: 1,
      title: "TaskFlow - Collaborative PM Suite",
      description: "A real-time Kanban and project management tool with live synchronization, drag-and-drop workflow, and role-based permissions.",
      category: "fullstack",
      categoryName: "Full Stack",
      image: "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80",
      tags: ["React", "Node.js", "Socket.io", "PostgreSQL", "Tailwind CSS"],
      liveUrl: "https://example.com",
      githubUrl: "https://github.com",
      featured: true
    },
    {
      id: 2,
      title: "PulseAnalytics - SaaS Dashboard",
      description: "High-performance metrics and analytics dashboard featuring interactive charts, automated reports, and dark/light modes.",
      category: "frontend",
      categoryName: "Frontend",
      image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
      tags: ["Next.js", "TypeScript", "Chart.js", "Tailwind CSS"],
      liveUrl: "https://example.com",
      githubUrl: "https://github.com",
      featured: true
    },
    {
      id: 3,
      title: "DevForge - AI Code Assistant",
      description: "A developer productivity extension leveraging LLM APIs to generate documentation, generate unit tests, and explain legacy code.",
      category: "ai",
      categoryName: "AI / Tooling",
      image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
      tags: ["Python", "FastAPI", "OpenAI API", "React"],
      liveUrl: "https://example.com",
      githubUrl: "https://github.com",
      featured: true
    },
    {
      id: 4,
      title: "Zenith - Minimalist E-Commerce",
      description: "Fast, accessible modern e-commerce storefront with Stripe checkout integration, cart drawer, and inventory tracking.",
      category: "fullstack",
      categoryName: "Full Stack",
      image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
      tags: ["React", "Stripe API", "Node.js", "MongoDB"],
      liveUrl: "https://example.com",
      githubUrl: "https://github.com",
      featured: false
    },
    {
      id: 5,
      title: "FitTrack - Workout & Habit Tracker",
      description: "Mobile-responsive PWA for tracking workouts, set progress, rest timers, and daily health metrics offline.",
      category: "mobile",
      categoryName: "Mobile / PWA",
      image: "https://images.unsplash.com/photo-1476480868586-765e80b21646?auto=format&fit=crop&w=800&q=80",
      tags: ["Vue.js", "Tailwind", "IndexedDB", "PWA"],
      liveUrl: "https://example.com",
      githubUrl: "https://github.com",
      featured: false
    },
    {
      id: 6,
      title: "CloudVault - Encrypted Storage CLI",
      description: "Secure cross-platform command-line tool for encrypting, backing up, and synchronizing local secrets to cloud storage.",
      category: "tools",
      categoryName: "CLI & Tools",
      image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80",
      tags: ["Go / Python", "AES-256", "AWS S3", "CLI"],
      liveUrl: "https://example.com",
      githubUrl: "https://github.com",
      featured: false
    }
  ],

  // Experience & Education Timeline
  timeline: [
    {
      type: "work",
      role: "Senior Full-Stack Developer",
      company: "TechNova Solutions",
      period: "2023 - Present",
      location: "San Francisco, CA",
      description: "Spearheaded development of high-traffic customer-facing web applications. Led architecture migration to microservices, boosting page load speeds by 42%."
    },
    {
      type: "work",
      role: "Frontend Software Engineer",
      company: "PixelCraft Digital",
      period: "2021 - 2023",
      location: "Austin, TX (Remote)",
      description: "Built responsive, reusable UI component libraries used across 6 enterprise products. Collaborated closely with design team in Figma."
    },
    {
      type: "education",
      role: "B.S. in Computer Science",
      company: "University of California",
      period: "2017 - 2021",
      location: "California, USA",
      description: "Graduated with Honors. Coursework focused on Algorithms, Distributed Systems, Software Engineering, and Database Systems."
    }
  ]
};

// Export for module systems or attach to window for plain HTML
if (typeof module !== "undefined" && module.exports) {
  module.exports = PORTFOLIO_DATA;
}
