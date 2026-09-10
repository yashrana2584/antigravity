# Modern Personal Portfolio Website

A clean, responsive, high-performance personal developer portfolio website featuring dark/light mode, dynamic typing hero banner, skill breakdowns, filterable project showcase, interactive timeline, and a working contact form.

---

## 🚀 Quick Start (Previewing Locally)

You have two simple ways to view the portfolio:

### Option 1: Open Directly in Browser
Simply double-click [`index.html`](./index.html) or right-click and choose **Open with > Chrome / Edge / Firefox**.

### Option 2: Run a Local HTTP Server (Recommended)
Using Python (pre-installed on most machines):
```bash
cd C:\Users\ASUS\.gemini\antigravity\scratch\portfolio
python -m http.server 8000
```
Then visit [`http://localhost:8000`](http://localhost:8000) in your browser.

---

## 🎨 How to Personalize Your Portfolio

All your data is centrally managed in **[`portfolio-data.js`](./portfolio-data.js)**. You don't need to touch HTML!

Open [`portfolio-data.js`](./portfolio-data.js) to customize:
1. **Personal Info**:
   - `personal.name`: Your full name.
   - `personal.role`: Your main title (e.g. *Full-Stack Developer*).
   - `personal.tagline`: Catchy introduction sentence.
   - `personal.typingRoles`: Array of titles that animate in the hero banner.
   - `personal.avatar`: URL or relative path to your profile picture (e.g. `images/avatar.jpg`).
   - `personal.location` & `personal.email`: Your location and contact email.
   - `personal.resumeUrl`: Link to your resume or file path (e.g. `resume.pdf`).
2. **Socials**:
   - Add or update GitHub, LinkedIn, Twitter/X, and Email URLs.
3. **About Me**:
   - `about.story`: Paragraphs describing your background and passion.
   - `about.stats`: Number badges (e.g., years of experience, projects completed).
   - `about.highlights`: 4 core strengths or principles.
4. **Skills**:
   - Grouped into *Frontend*, *Backend & Database*, and *Tools & DevOps* with proficiency percentages.
5. **Projects**:
   - Add titles, summaries, tags, live URLs, GitHub repository links, category tags (`fullstack`, `frontend`, `ai`, `mobile`, `tools`), and cover images.
6. **Experience & Education**:
   - Add roles, companies/schools, dates, and accomplishment summaries.

---

## 🌐 Deploying Your Portfolio (100% Free)

### Option A: GitHub Pages
1. Create a new GitHub repository named `portfolio` (or `<your-username>.github.io`).
2. Push all the files in this directory to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio release"
   git branch -M main
   git remote add origin https://github.com/<your-username>/portfolio.git
   git push -u origin main
   ```
3. Go to **Settings > Pages > Branch**, select `main` and `/ (root)`, and save.
4. Your portfolio will be live at `https://<your-username>.github.io/portfolio`!

### Option B: Vercel / Netlify
- Drag and drop the `portfolio` folder directly into [Netlify Drop](https://app.netlify.com/drop) or import from GitHub into [Vercel](https://vercel.com) for instant deployment with free SSL.

---

## 🛠️ Built With
- **HTML5 & CSS3**
- **Tailwind CSS** (via CDN with zero build steps)
- **Vanilla JavaScript (ES6+)**
- **Lucide Icons**
- **Google Fonts** (Plus Jakarta Sans & JetBrains Mono)
