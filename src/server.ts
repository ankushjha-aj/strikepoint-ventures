import express, { Request, Response } from 'express';
import path from 'path';

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 9000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/assets', express.static(path.join(__dirname, '..', 'assets')));

const pagesPath = path.join(__dirname, '..', 'pages');
const send = (file: string) => (_req: Request, res: Response) => res.sendFile(path.join(pagesPath, file));

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

// API
app.get('/api/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', brand: 'StrikePoint Ventures', uptime: process.uptime(), timestamp: new Date().toISOString() });
});

app.post('/api/contact', (req: Request, res: Response) => {
  const { name, email, topic, message } = req.body;
  console.log('[Contact inquiry]', { name, email, topic, message, date: new Date() });
  res.json({ success: true, message: 'Thank you for contacting StrikePoint Ventures. We will reply within one business day.' });
});

app.use((_req: Request, res: Response) => {
  res.status(404).sendFile(path.join(pagesPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`StrikePoint Ventures site running on port ${PORT}`);
});
