import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "chefwho.codes",
  description: "Personal site and codebase for chefwho.codes",
};

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/swm", label: "SWM" },
  { href: "/blog", label: "Blog" },
  { href: "/contact", label: "Contact" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="site-shell">
          <header className="site-header">
            <div className="container">
              <Link className="brand" href="/">
                chefwho.codes
              </Link>
              <nav aria-label="Primary">
                <ul className="nav-list">
                  {navLinks.map((link) => (
                    <li key={link.href}>
                      <Link href={link.href}>{link.label}</Link>
                    </li>
                  ))}
                </ul>
              </nav>
            </div>
          </header>
          <main className="container">{children}</main>
          <footer className="site-footer">
            <div className="container">
              <p>Built with Next.js and shipped from chefwho.codes.</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
