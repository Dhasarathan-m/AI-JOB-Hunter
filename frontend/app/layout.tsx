import type { Metadata } from 'next';
import './globals.css';
import { SiteShell } from '../components/SiteShell';

export const metadata: Metadata = {
  title: 'AI Job Hunter',
  description: 'Dashboard for AI-powered job hunting and resume matching',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SiteShell>{children}</SiteShell>
      </body>
    </html>
  );
}
