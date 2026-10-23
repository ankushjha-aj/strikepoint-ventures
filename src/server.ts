import express, { Request, Response } from 'express';
import path from 'path';

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 9000;

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static Assets
app.use('/static', express.static(path.join(__dirname, '..', 'static')));
app.use('/media', express.static(path.join(__dirname, '..', 'media')));

const viewsPath = path.join(__dirname, '..', 'views');

// Helper to send view files
const renderView = (filename: string) => {
  return (_req: Request, res: Response) => {
    res.sendFile(path.join(viewsPath, filename));
  };
};

// --- Page Routes ---
app.get('/', renderView('index.html'));
app.get('/home', renderView('index.html'));
app.get('/about', renderView('about.html'));
app.get('/team', renderView('team.html'));
app.get('/services', renderView('services.html'));
app.get('/blog', renderView('blog.html'));
app.get('/contact', renderView('contact.html'));
app.get('/logo-showcase', renderView('logo-showcase.html'));

// Services Sub-routes
app.get('/services/statistical-edge-finding', renderView('service-edge.html'));
app.get('/services/software-solutions', renderView('service-software.html'));
app.get('/services/strikepoint-rtx', renderView('service-rtx.html'));
app.get('/services/strikepoint-vector', renderView('service-vector.html'));
app.get('/services/proprietary-trading', renderView('service-prop.html'));
app.get('/services/strikepoint-foundation', renderView('service-foundation.html'));

// Legacy compatibility routes
app.get('/services/alpresi-rtx', renderView('service-rtx.html'));
app.get('/services/alpresi-vector', renderView('service-vector.html'));
app.get('/services/alpresi-foundation', renderView('service-foundation.html'));

// --- API Endpoints ---
app.get('/api/health', (_req: Request, res: Response) => {
  res.json({
    status: 'ok',
    brand: 'StrikePoint Ventures',
    port: PORT,
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

app.post('/api/contact', (req: Request, res: Response) => {
  const { name, email, phone, message } = req.body;
  console.log('[StrikePoint Contact Inquiry Received]:', { name, email, phone, message, date: new Date() });
  res.json({
    success: true,
    message: 'Thank you for contacting StrikePoint Ventures. Our desk will review your inquiry and respond within 1 business day.'
  });
});

app.post('/api/set-logo', (req: Request, res: Response) => {
  const { conceptId } = req.body;
  const fs = require('fs');
  const path = require('path');
  
  const conceptMap: Record<number, { light: string; dark: string }> = {
    1: { light: 'concept-1-sv-intertwined.svg', dark: 'concept-1-sv-intertwined-dark.svg' },
    2: { light: 'concept-2-stp-monogram.svg', dark: 'concept-2-stp-monogram-dark.svg' },
    3: { light: 'concept-3-stv-shield.svg', dark: 'concept-3-stv-shield-dark.svg' },
    4: { light: 'concept-4-stp-pillar.svg', dark: 'concept-4-stp-pillar-dark.svg' },
    5: { light: 'concept-5-sv-compass.svg', dark: 'concept-5-sv-compass-dark.svg' }
  };

  const selected = conceptMap[conceptId];
  if (!selected) {
    return res.status(400).json({ error: 'Invalid conceptId' });
  }

  const conceptsDir = path.join(__dirname, '..', 'media', 'branding', 'concepts');
  const brandingDir = path.join(__dirname, '..', 'media', 'branding');

  try {
    fs.copyFileSync(path.join(conceptsDir, selected.light), path.join(brandingDir, 'strikepoint-logo.svg'));
    fs.copyFileSync(path.join(conceptsDir, selected.dark), path.join(brandingDir, 'strikepoint-logo-dark.svg'));
    return res.json({ success: true, conceptId, message: `Active logo updated to Concept ${conceptId} successfully!` });
  } catch (err) {
    console.error('Error applying logo:', err);
    return res.status(500).json({ error: 'Failed to update logo files' });
  }
});

// 404 Handler
app.use((_req: Request, res: Response) => {
  res.status(404).sendFile(path.join(viewsPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`=================================================`);
  console.log(`🚀 StrikePoint Ventures Server Live`);
  console.log(`📡 URL: http://0.0.0.0:${PORT}`);
  console.log(`=================================================`);
});
