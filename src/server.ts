import express, { NextFunction, Request, Response } from 'express';
import fs from 'fs';
import path from 'path';

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 9000;

// Basic hardening: hide the framework, cap request bodies, send safe default headers.
app.disable('x-powered-by'); // nosemgrep: helmet_header_x_powered_by -- informational: confirms the header is removed
app.use(express.json({ limit: '20kb' }));
app.use(express.urlencoded({ extended: false, limit: '20kb' }));
app.use((_req: Request, res: Response, next: NextFunction) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  next();
});

app.use('/assets', express.static(path.join(__dirname, '..', 'assets')));

const pagesPath = path.join(__dirname, '..', 'pages');
// Files are always served by name from a fixed folder (`root`), never from a path built out of request data.
const send = (file: string) => (_req: Request, res: Response) => res.sendFile(file, { root: pagesPath });

// Pages
const routes: Record<string, string> = {
  '/': 'index.html',
  '/preview': 'preview.html',
  '/about': 'about.html',
  '/services': 'services.html',
  '/services/research-technology': 'research-technology.html',
  '/services/atlas-helm': 'atlas-helm.html',
  '/services/proprietary-desk': 'proprietary-desk.html',
  '/blog': 'blog.html',
  '/contact': 'contact.html',
};
Object.entries(routes).forEach(([url, file]) => app.get(url, send(file)));

// Blog posts: /blog/<slug> -> pages/blog/<slug>.html (built from content/blog/*.md).
// Only posts that exist when the server starts are served; anything else falls through to 404.
const blogDir = path.join(pagesPath, 'blog');
const blogPosts = new Map<string, string>();
if (fs.existsSync(blogDir)) {
  for (const f of fs.readdirSync(blogDir)) {
    if (/^[a-z0-9-]+\.html$/.test(f)) blogPosts.set(f.slice(0, -5), f);
  }
}
app.get('/blog/:slug', (req: Request, res: Response, next: NextFunction) => {
  const file = blogPosts.get(req.params.slug);
  if (!file) return next();
  res.sendFile(file, { root: blogDir });
});

// API
app.get('/api/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', brand: 'StrikePoint Ventures', uptime: process.uptime(), timestamp: new Date().toISOString() });
});

const TOPICS = ['Research & Technology', 'Atlas & Helm', 'Proprietary Desk'];
const EMAIL_RE = /^[^\s@]{1,64}@[^\s@]{1,190}\.[^\s@]{2,24}$/;

/** A trimmed string no longer than `max`, or null if the field is missing or the wrong type. */
function field(body: unknown, key: string, max: number): string | null {
  if (typeof body !== 'object' || body === null) return null;
  const v = (body as Record<string, unknown>)[key];
  if (typeof v !== 'string') return null;
  const t = v.trim();
  return t.length > 0 && t.length <= max ? t : null;
}

/** Strip control characters so visitor input can't forge extra log lines. */
// eslint-disable-next-line no-control-regex -- matching control characters is the point here
const forLog = (s: string) => s.replace(/[\u0000-\u001f\u007f]/g, ' ');

app.post('/api/contact', (req: Request, res: Response) => {
  const name = field(req.body, 'name', 120);
  const email = field(req.body, 'email', 254);
  const message = field(req.body, 'message', 5000);
  const rawTopic = field(req.body, 'topic', 200) ?? '';
  if (!name || !email || !message || !EMAIL_RE.test(email)) {
    res.status(400).json({ success: false, message: 'Please fill in your name, a valid email and a message.' });
    return;
  }
  const topic = TOPICS.includes(rawTopic) || rawTopic.startsWith('Other') ? rawTopic : 'Other';
  console.log('[Contact inquiry]', JSON.stringify({
    name: forLog(name), email: forLog(email), topic: forLog(topic), message: forLog(message), date: new Date().toISOString(),
  }));
  res.json({ success: true, message: 'Thank you for contacting StrikePoint Ventures. We will reply within one business day.' });
});

app.use((_req: Request, res: Response) => {
  res.status(404).sendFile('index.html', { root: pagesPath });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`StrikePoint Ventures site running on port ${PORT}`);
});
