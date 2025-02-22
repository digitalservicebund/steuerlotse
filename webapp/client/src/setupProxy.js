// This file is automatically loaded when starting the development server.

const { createProxyMiddleware } = require("http-proxy-middleware");

function setupProxy(app) {
  app.use(
    createProxyMiddleware(
      [
        "/**", // Proxy all requests, except:
        "!**/*.js", // javascript,
        "!**/*.js.map", // source maps,
        "!**/*.css", // css,
        "!/{static,files,fonts,icons,images}/**", // any other static assets,
        "!/*.hot-update.json", // HMR requests
        "!/robots.txt",
        "!/sitemap.txt",
      ],
      {
        target: process.env.WEBAPP_URL || "http://127.0.0.1:5000",
        changeOrigin: true,
        autoRewrite: true,
      }
    )
  );
}

module.exports = setupProxy;
