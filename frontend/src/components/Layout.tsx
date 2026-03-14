import type { ReactNode } from "react";

interface LayoutProps {
  title: string;
  subtitle: string;
  children: ReactNode;
}

export default function Layout({ title, subtitle, children }: LayoutProps) {
  return (
    <div className="app-shell">
      <header className="hero">
        <p className="hero__eyebrow">MDLand Front Desk Prototype</p>
        <h1 className="hero__title">{title}</h1>
        <p className="hero__subtitle">{subtitle}</p>
      </header>

      <main className="app-main">{children}</main>
    </div>
  );
}
