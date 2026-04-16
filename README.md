# visualization-display-Statistical-Review-of-World-Energy

Project for "Data visualization analysis", buaa, 2026.4.

https://wnymin.github.io/visualization-display-Statistical-Review-of-World-Energy/

## Frontend

- Vue project folder: `webapp-vue`
- Data source file: `EI-Stats-Review-ALL-data.xlsx`

## Local Development

```bash
cd webapp-vue
npm install
npm run dev
```

## Build

```bash
cd /workspaces/visualization-display-Statistical-Review-of-World-Energy
mkdir -p webapp-vue/public/data
cp EI-Stats-Review-ALL-data.xlsx webapp-vue/public/data/
cd webapp-vue
npm run build
```

Build output is generated in `webapp-vue/dist`.

## GitHub Pages Deployment

GitHub Actions workflow file: `.github/workflows/deploy-pages.yml`

Deployment behavior:

1. Trigger on push to `main` (or manual run).
2. Install dependencies in `webapp-vue`.
3. Copy `EI-Stats-Review-ALL-data.xlsx` into `webapp-vue/public/data` before build.
4. Build Vue app with Pages base path.
5. Deploy `webapp-vue/dist` to GitHub Pages.

After enabling GitHub Pages (Source: GitHub Actions), the expected site URL is:

`https://wnymin.github.io/visualization-display-Statistical-Review-of-World-Energy/`
