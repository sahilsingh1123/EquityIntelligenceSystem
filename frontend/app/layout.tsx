import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Equity Intelligence",
  description: "Explainable event-centric equity intelligence for Indian markets"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
