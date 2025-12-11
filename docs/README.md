# Deploying Documentation to GitHub Pages

## Quick Setup

1. **Push the `docs` folder to your repository:**
   ```bash
   cd path/to/TYIT-Project
   git add docs/
   git commit -m "Add GitHub Pages documentation"
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repository: https://github.com/Tabbyx0X/TYIT-Project
   - Click **Settings** → **Pages**
   - Under "Source", select:
     - Branch: `main`
     - Folder: `/docs`
   - Click **Save**

3. **Wait 2-5 minutes**, then visit:
   ```
   https://tabbyx0x.github.io/TYIT-Project/
   ```

## What's Included

- ✅ Complete project documentation
- ✅ Interactive navigation
- ✅ Installation guide with copy-paste code blocks
- ✅ API endpoint reference
- ✅ Database schema visualization
- ✅ Usage guides for admins and voters
- ✅ Responsive design (mobile-friendly)
- ✅ Modern, professional UI

## Customization

### Change Colors
Edit `docs/styles.css` and modify the `:root` variables:
```css
:root {
    --primary-color: #0d6efd;
    --success-color: #198754;
    /* Add your colors */
}
```

### Add New Sections
Edit `docs/index.html` and add new `<section>` blocks.

### Update Content
All content is in `docs/index.html` - update text, links, or add images as needed.

## Alternative: Use Jekyll Theme

If you prefer a simpler approach with Markdown:

1. Keep the `_config.yml` file
2. Create `docs/index.md` with your documentation in Markdown
3. GitHub will automatically build it with Jekyll

## Custom Domain (Optional)

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. Add `CNAME` file in `docs/` folder:
   ```
   yourdomain.com
   ```
3. Configure DNS records (A records or CNAME)
4. Wait 24-48 hours for propagation

## Troubleshooting

**Page not loading?**
- Check Settings → Pages → Ensure source is set to `/docs`
- Ensure `index.html` exists in the docs folder
- Wait a few minutes after enabling

**Styles not loading?**
- Check that `styles.css` and `script.js` paths are correct
- Clear browser cache (Ctrl+F5)

**Need help?**
- GitHub Pages Docs: https://docs.github.com/pages
- Jekyll Docs: https://jekyllrb.com/docs/

---

Your documentation will be live at: **https://tabbyx0x.github.io/TYIT-Project/** 🚀
