import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Synapse Logistics | AI Negotiation Command Center',
  description: 'A polished multi-agent logistics negotiation workspace for crisis response and planning.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, background: '#020617' }}>{children}</body>
    </html>
  );
}
