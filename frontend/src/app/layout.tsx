import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FINN - Financial Investment Agent",
  description: "AI-powered intelligence layer for high-conviction public markets investment.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-finn-dark text-white min-h-screen antialiased flex flex-col justify-between selection:bg-blue-600 selection:text-white">
        <main className="flex-1 pb-20">
          {children}
        </main>
      </body>
    </html>
  );
}
