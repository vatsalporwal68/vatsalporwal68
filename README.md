# 👋 Hello, I'm Vatsal Porwal (@vatsalporwal68)

> A personalized developer profile powered by code that generates and updates itself automatically. No third-party widgets, zero external dependencies, and every pixel rendered right inside this repository.

---

### /// SELF-TYPING ASCII PORTRAIT

<div align="center">
  <img src="assets/portrait.svg" alt="Animated ASCII Portrait" width="460"/>
</div>

<br/>

> [!NOTE]
> **To personalize your ASCII portrait:**
> Add your photo named `portrait.jpg` (or `portrait.png`) to this repository root and run:
> ```bash
> python scripts/generate_ascii.py --input portrait.jpg --output assets/portrait.svg
> ```

---

### /// ABOUT ME & TECH STACK

<samp>
- 🚀 <b>Building:</b> Innovative Software, Full-Stack Applications, & AI Tools.<br/>
- 💡 <b>Focus:</b> Clean Architecture, Automated Pipelines, & Modern Web Tech.<br/>
- 🛠️ <b>Tech Stack:</b> Python, JavaScript, TypeScript, React, Node.js, C++.<br/>
- 📫 <b>GitHub:</b> <a href="https://github.com/vatsalporwal68">@vatsalporwal68</a>
</samp>

---

### /// LIVE STATS & CONTRIBUTION METRICS

<div align="center">

| Activity Stats | Streak Tracker |
| :---: | :---: |
| <img src="assets/stats.svg" alt="GitHub Stats" width="420"/> | <img src="assets/streak.svg" alt="GitHub Streak" width="420"/> |

</div>

<br/>

<div align="center">

| Top Languages | 365-Day Contribution Density |
| :---: | :---: |
| <img src="assets/langs.svg" alt="Top Languages" width="420"/> | <img src="assets/year.svg" alt="Year-in-ASCII Graph" width="500"/> |

</div>

---

### ⚙️ HOW IT WORKS UNDER THE HOOD

```
+------------------+     +------------------------+     +-------------------+
| Input Photo      | --> | scripts/generate_ascii | --> | assets/portrait   |
| (portrait.jpg)   |     | (Bilateral, CLAHE, SMIL) |     | (.svg)            |
+------------------+     +------------------------+     +-------------------+

+------------------+     +------------------------+     +-------------------+
| GitHub GraphQL   | --> | scripts/generate_stats | --> | assets/*.svg      |
| API (Nightly)    |     | (Pinned UTC, Public)   |     | (Stats/Streak/Yr) |
+------------------+     +------------------------+     +-------------------+
```

- **Zero Fragility:** All SVG graphics are generated directly within this repository using Python and committed back by GitHub Actions (`.github/workflows/refresh.yml`).
- **Determinism Fixes:** Date queries are pinned to whole UTC days (`00:00:00Z` to `23:59:59Z`) and filtered to public repositories to ensure stable Git commits.
- **SMIL Animation:** The ASCII portrait uses native SVG `<clipPath>` SMIL animations that type out smoothly in light and dark mode without client-side JavaScript.

---

<div align="center">
  <samp>Generated autonomously with Antigravity AI • Powered by GitHub Actions</samp>
</div>
