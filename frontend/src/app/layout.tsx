import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'NeoCafeIA - Asistente de Cafetería',
  description: 'Asistente inteligente de IA para cafeterías',
  metadataBase: new URL('http://localhost:3000'),
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" dir="ltr">
      <body>{children}</body>
    </html>
  );
}
