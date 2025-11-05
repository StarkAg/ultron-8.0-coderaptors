# Vercel Deployment Guide for Ultron 8.0 - CodeRaptors

## ⚠️ Important Notes

**Vercel has limitations for Flask apps:**
- Serverless function timeout: 10s (free) / 60s (pro)
- Package size limit: 50MB for serverless functions
- Large datasets (CSV files) may cause issues
- ML model loading might be slow on first request

## 📋 Prerequisites

1. **Vercel account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **GitHub account**: For automatic deployments

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Environment Variables**:
   - Add `SERPAPI_KEY` in Vercel dashboard
   - Settings → Environment Variables

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Deploy via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
cd "hackathons/Ultron 8.0- CodeRaptors"
vercel

# Follow prompts:
# - Link to existing project? (N)
# - Project name: ultron-movie-recommender
# - Directory: ./
# - Override settings? (N)

# Set environment variable
vercel env add SERPAPI_KEY
# Paste your API key when prompted

# Deploy to production
vercel --prod
```

## 🔧 Configuration Files

### `vercel.json`
- Routes all requests to Flask app
- Configures serverless function timeout (60s)
- Sets up static file serving

### `api/index.py`
- Flask app adapted for Vercel serverless functions
- Uses `vercel` package for request handling

## ⚙️ Environment Variables

Add these in Vercel dashboard:

```
SERPAPI_KEY=your-serpapi-key-here
```

**How to add:**
1. Go to project settings
2. Navigate to "Environment Variables"
3. Add `SERPAPI_KEY` with your API key
4. Redeploy

## 📦 Package Size Optimization

**Current issues:**
- Datasets are large (~50MB+)
- ML libraries (pandas, scikit-learn) are heavy

**Solutions:**
1. **Move datasets to external storage** (S3, Cloud Storage)
2. **Use CDN for datasets**
3. **Optimize model loading** (lazy loading, caching)
4. **Consider alternative hosting** (Render, Railway, Fly.io)

## 🔄 Alternative: Better Hosting Options

For Flask apps with ML models, consider:

1. **Render** (Recommended for Flask)
   - Free tier available
   - Better for long-running processes
   - Easy Flask deployment

2. **Railway**
   - Good for Python apps
   - Auto-deploys from GitHub

3. **Fly.io**
   - Docker-based
   - Good performance

4. **Heroku**
   - Classic option
   - Paid tier required now

## 🐛 Troubleshooting

### Issue: Function timeout
- **Solution**: Optimize model loading, use caching
- **Workaround**: Increase timeout in `vercel.json` (requires Pro plan)

### Issue: Package too large
- **Solution**: Remove unnecessary files, optimize datasets
- **Check**: Use `vercel --debug` to see build logs

### Issue: Module not found
- **Solution**: Ensure all dependencies in `requirements.txt`
- **Check**: `api/index.py` imports correctly

### Issue: API key not working
- **Solution**: Verify environment variable is set correctly
- **Check**: Use `vercel env ls` to list variables

## 📝 Notes

- First request will be slow (cold start + model loading)
- Subsequent requests will be faster (caching)
- Consider using Vercel Edge Functions for static content
- Monitor function execution time in Vercel dashboard

## 🔗 Useful Links

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask on Vercel](https://vercel.com/guides/deploying-flask-with-vercel)
- [Vercel CLI Reference](https://vercel.com/docs/cli)

