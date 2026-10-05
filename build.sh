#!/bin/sh
# Wraps app.html (the game) into an installable index.html for GitHub Pages.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  printf '<meta name="theme-color" content="#1b8bb4">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
  printf '<meta name="apple-mobile-web-app-title" content="Little Island">\n'
  printf '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icon.svg">\n<link rel="apple-touch-icon" href="icon-192.png">\n'
  printf '</head>\n<body>\n'
  cat app.html
  printf '\n<script>if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(function(){});</script>\n'
  printf '</body>\n</html>\n'
} > index.html
