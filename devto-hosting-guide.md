---
title: "Shared vs VPS vs Cloud Hosting: Which Do You Actually Need?"
published: true
description: "A practical guide to choosing hosting. Real prices, performance comparisons, and when to upgrade from shared hosting."
tags: webdev, hosting, devops, tutorial
canonical_url: https://uriy-as.org/en/blog/how-to-choose-hosting.html
---

# Shared vs VPS vs Cloud Hosting: Which Do You Actually Need?

We've deployed 50+ websites across different hosting providers. The most common mistake: paying for a dedicated server when shared hosting would work, or using cheap shared hosting when the site needs VPS.

Here's how to choose correctly — with real prices and benchmarks.

---

## The Four Types (Simplified)

| Type | Price | Best For | Performance |
|---|---|---|---|
| **Shared** | $3–5/mo | Blogs, landing pages, small business sites | ⭐⭐ |
| **VPS** | $10–30/mo | Growing sites, custom configs, API backends | ⭐⭐⭐⭐ |
| **Cloud** | $15–50/mo | Variable traffic, scalability needed | ⭐⭐⭐⭐⭐ |
| **Dedicated** | $50+/mo | High-traffic sites, resource-heavy apps | ⭐⭐⭐⭐⭐ |

---

## Shared Hosting: When It Works

Shared hosting means your site sits on a server with hundreds of other sites. You share CPU, RAM, and bandwidth.

**Good for:**
- Landing pages and business card sites
- Blogs with <1,000 daily visitors
- WordPress sites with minimal plugins
- Static sites and portfolios

**Bad for:**
- Sites with custom server-side logic
- Anything needing root access
- Sites that get traffic spikes
- E-commerce during sales

**Real-world performance:**
```
Shared hosting (SiteGround):
- TTFB: 400–800ms
- Load time (simple page): 1.5–3s
- Concurrent users before slowdown: ~20
- Downtime during traffic spike: likely
```

**Price range:** $3–5/month. Look for:
- Free SSL (Let's Encrypt)
- PHP 8.x + MySQL
- Daily backups
- SSH access (nice to have)

**Providers we've used:** Hostinger ($3/mo), SiteGround ($5/mo), Namecheap ($4/mo). All work fine for small sites.

---

## VPS: The Sweet Spot

VPS (Virtual Private Server) gives you guaranteed resources and root access. You get a slice of a physical server — typically 1–4 CPU cores, 1–4 GB RAM.

**Good for:**
- Sites getting 1,000+ daily visitors
- Custom applications (Flask, Django, Node.js)
- Multiple sites on one server
- APIs and backends
- Development/staging environments

**Bad for:**
- Complete beginners (requires some Linux knowledge)
- Sites that need auto-scaling
- Very high traffic (>100k daily)

**Real-world performance:**
```
VPS (Hetzner CPX21, $7/mo):
- 3 vCPU, 4 GB RAM
- TTFB: 100–300ms
- Load time (simple page): 0.5–1.5s
- Concurrent users before slowdown: ~200
- Handles traffic spikes easily
```

**Managed vs Unmanaged:**
- **Unmanaged VPS** ($7–15/mo): You manage everything. Cheaper but requires Linux skills.
- **Managed VPS** ($20–40/mo): Provider handles updates, security, backups. More expensive but hands-off.

**Our recommendation:** Hetzner CPX21 ($7/mo) for unmanaged, DigitalOcean ($12/mo) for managed. Both are reliable and fast.

---

## Cloud Hosting: When You Need Scale

Cloud hosting uses multiple servers. If one fails, traffic routes to another. You pay for what you use.

**Good for:**
- E-commerce with traffic spikes (Black Friday, sales)
- SaaS applications
- Sites with unpredictable traffic
- Projects that need auto-scaling

**Bad for:**
- Small sites (overkill and expensive)
- Predictable, steady traffic (VPS is cheaper)
- Budget projects

**Real-world performance:**
```
Cloud (AWS Lightsail, $12/mo):
- 2 vCPU, 2 GB RAM
- TTFB: 50–200ms
- Load time: 0.3–1s
- Auto-scales to handle any traffic
- 99.99% uptime
```

**The catch:** Cloud pricing is usage-based. A small site might cost $12/month, but a traffic spike can push it to $50+. Set billing alerts.

---

## Decision Framework

Ask yourself these questions:

**1. How many daily visitors?**
- <500 → Shared
- 500–10,000 → VPS
- 10,000+ → Cloud or dedicated

**2. Do you need root access?**
- No → Shared is fine
- Yes → VPS minimum

**3. Is traffic predictable?**
- Yes → VPS (fixed cost, guaranteed resources)
- No → Cloud (pay for what you use)

**4. Do you run custom applications?**
- No (just HTML/CSS/JS or WordPress) → Shared
- Yes (Python, Node.js, custom backend) → VPS

**5. What's your budget?**
- <$5/month → Shared
- $5–15/month → VPS
- $15–50/month → Cloud
- $50+/month → Dedicated

---

## The Migration Path

Most sites follow this trajectory:

```
Year 1: Shared hosting ($5/mo)
  ↓ Site grows, need more performance
Year 2: VPS ($10/mo)
  ↓ Traffic spikes, need scalability
Year 3: Cloud ($15–30/mo)
  ↓ High traffic, need dedicated resources
Year 4+: Dedicated ($50+/mo)
```

Don't start with dedicated. Start with shared, monitor performance, and upgrade when you actually need to.

---

## What We Actually Recommend

**For 90% of small business sites:** Shared hosting from Hostinger or SiteGround ($3–5/mo). It's fast enough, cheap, and requires zero maintenance.

**For growing sites and developers:** Hetzner CPX21 ($7/mo). Best price-to-performance ratio. 3 vCPU, 4 GB RAM, NVMe SSD. We run our production sites on Hetzner.

**For e-commerce and SaaS:** DigitalOcean or AWS Lightsail ($12–20/mo). Reliable, scalable, good ecosystem.

**Avoid:** GoDaddy (overpriced, upsells everywhere), Bluehost (slow shared servers), any "unlimited" hosting claim (there's always a limit).

---

## Quick Performance Tips

Regardless of hosting type:

1. **Enable gzip/brotli compression** — reduces payload by 60–80%
2. **Set caching headers** — `Cache-Control: max-age=31536000` for static assets
3. **Use a CDN** — Cloudflare free tier handles most needs
4. **Optimize images** — WebP format, lazy loading
5. **Minimize HTTP requests** — combine CSS/JS files

```nginx
# Nginx caching config
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## The Bottom Line

- **Small site, small budget:** Shared hosting ($3–5/mo)
- **Growing site, need control:** VPS ($7–15/mo)
- **Scaling site, need reliability:** Cloud ($15–30/mo)
- **Don't overpay for resources you won't use**

Start cheap, monitor performance, upgrade when metrics tell you to — not when your hosting provider's sales page tells you to.

---

*We deploy websites on Hetzner, DigitalOcean, and GitHub Pages. Full source code: [github.com/uriy-as/site](https://github.com/uriy-as/site)*
