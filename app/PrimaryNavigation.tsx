"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";

type NavItem = readonly string[];

function normalizePath(path: string) {
  if (!path || path === "/") return "/";
  return path.replace(/\/+$/, "");
}

function isActivePath(currentPath: string, href: string) {
  return normalizePath(currentPath) === normalizePath(href);
}

export function PrimaryNavigation({ items }: { items: NavItem[] }) {
  const currentPath = normalizePath(usePathname() || "/");
  const [menuOpen, setMenuOpen] = useState(false);
  const mobileNavRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!menuOpen) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const handlePointerDown = (event: PointerEvent) => {
      if (!mobileNavRef.current?.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMenuOpen(false);
      }
    };

    document.addEventListener("pointerdown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("pointerdown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [menuOpen]);

  const renderLink = ([label, href]: NavItem) => {
    const targetHref = href || "/";
    const itemLabel = label || "";
    const active = isActivePath(currentPath, targetHref);
    return (
      <Link
        key={targetHref}
        href={targetHref}
        className={active ? "active" : undefined}
        aria-current={active ? "page" : undefined}
        onClick={() => {
          setMenuOpen(false);
        }}
      >
        {itemLabel}
      </Link>
    );
  };

  return (
    <>
      <nav className="desktop-nav" aria-label="主导航">
        {items.map(renderLink)}
      </nav>
      <div className={`mobile-nav${menuOpen ? " open" : ""}`} ref={mobileNavRef}>
        <button
          type="button"
          className="mobile-nav-toggle"
          aria-label={menuOpen ? "关闭主导航" : "打开主导航"}
          aria-expanded={menuOpen}
          aria-controls="mobile-primary-nav"
          onClick={() => setMenuOpen((open) => !open)}
        >
          <span />
          菜单
        </button>
        {menuOpen && (
          <nav id="mobile-primary-nav" className="mobile-nav-panel" aria-label="移动端主导航">
            {items.map(renderLink)}
          </nav>
        )}
      </div>
    </>
  );
}
