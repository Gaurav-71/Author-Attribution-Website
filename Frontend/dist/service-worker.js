if(!self.define){let e,i={};const n=(n,r)=>(n=new URL(n+".js",r).href,i[n]||new Promise((i=>{if("document"in self){const e=document.createElement("script");e.src=n,e.onload=i,document.head.appendChild(e)}else e=n,importScripts(n),i()})).then((()=>{let e=i[n];if(!e)throw new Error(`Module ${n} didn’t register its module`);return e})));self.define=(r,l)=>{const s=e||("document"in self?document.currentScript.src:"")||location.href;if(i[s])return;let o={};const u=e=>n(e,s),t={module:{uri:s},exports:o,require:u};i[s]=Promise.all(r.map((e=>t[e]||u(e)))).then((e=>(l(...e),o)))}}define(["./workbox-79ffe3e0"],(function(e){"use strict";e.setCacheNameDetails({prefix:"author-attribution"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.496da054.css",revision:null},{url:"/css/chunk-vendors.d606a616.css",revision:null},{url:"/img/chandrika.a6901967.png",revision:null},{url:"/img/compression.4b0ee5a1.png",revision:null},{url:"/img/grap.a4f2c907.png",revision:null},{url:"/img/graph.9aacbda2.png",revision:null},{url:"/img/instance.164cf19f.png",revision:null},{url:"/img/jaggi.c35863d2.png",revision:null},{url:"/img/lstm.fe54ce76.png",revision:null},{url:"/img/profile.d163d4ac.png",revision:null},{url:"/img/rit.21e2730d.png",revision:null},{url:"/img/upload.e4f4afe7.svg",revision:null},{url:"/img/wip.86173582.svg",revision:null},{url:"/index.html",revision:"b2836003b6b80df2bc5134b8e731f632"},{url:"/js/app.3fd82a6e.js",revision:null},{url:"/js/chunk-vendors.6e2f4e83.js",revision:null},{url:"/manifest.json",revision:"394fbf4bc07c6a6adf3bf89e591ef30d"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map
