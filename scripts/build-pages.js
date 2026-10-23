const fs = require('fs');
const path = require('path');

const viewsDir = path.join(__dirname, '..', 'views');
if (!fs.existsSync(viewsDir)) {
  fs.mkdirSync(viewsDir, { recursive: true });
}

function transformHtml(html, pageTitle = '') {
  let res = html;

  // Standardize assets
  res = res.replace(/href=["']\/static\/css\/main\.css["']/g, 'href="/static/css/main.css"');
  res = res.replace(/src=["']\/static\/js\/main\.js["']/g, 'src="/static/js/main.js"');
  res = res.replace(/href=["']\/media\/branding\/avatar-navy\.svg["']/g, 'href="/media/branding/avatar-navy.svg"');
  res = res.replace(/src=["']\/media\/branding\/alpresi-logo-light-fit_u\.svg["']/g, 'src="/media/branding/strikepoint-logo.svg"');
  res = res.replace(/src=["']media\/branding\/alpresi-logo-light-fit_u\.svg["']/g, 'src="/media/branding/strikepoint-logo.svg"');

  // Replace text & brand
  res = res.replace(/ALPRESI RESEARCH CAPITAL PRIVATE LIMITED/gi, 'StrikePoint Ventures Private Limited');
  res = res.replace(/ALPRESI RESEARCH/gi, 'STRIKEPOINT VENTURES');
  res = res.replace(/ALPRESI/gi, 'StrikePoint');
  res = res.replace(/ALpresi Research Capital Private Limited/gi, 'StrikePoint Ventures Private Limited');
  res = res.replace(/ALpresi Research/gi, 'StrikePoint Ventures');
  res = res.replace(/ALpresi RTX/gi, 'StrikePoint RTX');
  res = res.replace(/ALpresi Vector/gi, 'StrikePoint Vector');
  res = res.replace(/The ALpresi Foundation/gi, 'The StrikePoint Foundation');
  res = res.replace(/ALpresi/gi, 'StrikePoint');
  res = res.replace(/alpresi-foundation/gi, 'strikepoint-foundation');
  res = res.replace(/alpresi-rtx/gi, 'strikepoint-rtx');
  res = res.replace(/alpresi-vector/gi, 'strikepoint-vector');
  res = res.replace(/wecare@alpresiresearch\.com/gi, 'contact@strikepointventures.com');
  res = res.replace(/https:\/\/x\.com\/alpresiresearch/gi, 'https://x.com/strikepointventures');

  // Internal link normalization
  res = res.replace(/href=["']\/about\/["']/g, 'href="/about"');
  res = res.replace(/href=["']\/team\/["']/g, 'href="/team"');
  res = res.replace(/href=["']\/blog\/["']/g, 'href="/blog"');
  res = res.replace(/href=["']\/contact\/["']/g, 'href="/contact"');
  res = res.replace(/href=["']\/services\/statistical-edge-finding\/["']/g, 'href="/services/statistical-edge-finding"');
  res = res.replace(/href=["']\/services\/software-solutions\/["']/g, 'href="/services/software-solutions"');
  res = res.replace(/href=["']\/services\/alpresi-rtx\/["']/g, 'href="/services/strikepoint-rtx"');
  res = res.replace(/href=["']\/services\/strikepoint-rtx\/["']/g, 'href="/services/strikepoint-rtx"');
  res = res.replace(/href=["']\/services\/alpresi-vector\/["']/g, 'href="/services/strikepoint-vector"');
  res = res.replace(/href=["']\/services\/strikepoint-vector\/["']/g, 'href="/services/strikepoint-vector"');
  res = res.replace(/href=["']\/services\/proprietary-trading\/["']/g, 'href="/services/proprietary-trading"');
  res = res.replace(/href=["']\/services\/alpresi-foundation\/["']/g, 'href="/services/strikepoint-foundation"');
  res = res.replace(/href=["']\/services\/strikepoint-foundation\/["']/g, 'href="/services/strikepoint-foundation"');

  // Footer logo to dark version
  res = res.replace(/(<img\s+src="[^"]*strikepoint-logo\.svg"[^>]*class="footer__logo")/g, '<img src="/media/branding/strikepoint-logo-dark.svg" alt="STRIKEPOINT VENTURES" class="footer__logo"');
  res = res.replace(/(<div class="footer__brand">[\s\S]*?<img\s+src=")[^"]*(")/, '$1/media/branding/strikepoint-logo-dark.svg$2');

  // Fix media paths
  res = res.replace(/src=["']\/media\//g, 'src="/media/');
  res = res.replace(/src=["']media\//g, 'src="/media/');
  res = res.replace(/href=["']\/media\//g, 'href="/media/');
  res = res.replace(/href=["']media\//g, 'href="/media/');

  if (pageTitle) {
    res = res.replace(/<title>[\s\S]*?<\/title>/i, `<title>${pageTitle} — StrikePoint Ventures</title>`);
  }

  return res;
}

// 1. Home
const homeSrc = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
fs.writeFileSync(path.join(viewsDir, 'index.html'), transformHtml(homeSrc, 'StrikePoint Ventures — Quantitative Research & Trading'));

// 2. Subpages
const pageMap = [
  { file: '/tmp/alpresi_about.html', out: 'about.html', title: 'About Us' },
  { file: '/tmp/alpresi_team.html', out: 'team.html', title: 'Our Team & Leadership' },
  { file: '/tmp/alpresi_contact.html', out: 'contact.html', title: 'Contact Us' },
  { file: '/tmp/alpresi_blog.html', out: 'blog.html', title: 'Insights & Research Blog' },
  { file: '/tmp/alpresi_service_statistical-edge-finding.html', out: 'service-edge.html', title: 'Quantitative Edge Research' },
  { file: '/tmp/alpresi_service_software-solutions.html', out: 'service-software.html', title: 'Financial Markets Software' },
  { file: '/tmp/alpresi_service_alpresi-rtx.html', out: 'service-rtx.html', title: 'StrikePoint RTX — Real Time Analytics Terminal' },
  { file: '/tmp/alpresi_service_alpresi-vector.html', out: 'service-vector.html', title: 'StrikePoint Vector — Execution Engine' },
  { file: '/tmp/alpresi_service_proprietary-trading.html', out: 'service-prop.html', title: 'Proprietary Trading Desk' },
  { file: '/tmp/alpresi_service_alpresi-foundation.html', out: 'service-foundation.html', title: 'The StrikePoint Foundation' }
];

pageMap.forEach(({ file, out, title }) => {
  if (fs.existsSync(file)) {
    const raw = fs.readFileSync(file, 'utf8');
    const transformed = transformHtml(raw, title);
    fs.writeFileSync(path.join(viewsDir, out), transformed);
    console.log(`✓ Generated views/${out} (${transformed.length} bytes)`);
  } else {
    console.warn(`File missing: ${file}`);
  }
});

console.log('All views successfully generated!');
