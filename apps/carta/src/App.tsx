import { useState, useEffect, useRef } from "react";
import { getCategories, getProducts, getSettings } from "@menu/api-client";
import type { Category, Product, AppSettings } from "@menu/types";
import { ProductLayout, ProductDetailSheet } from "@menu/ui";

export default function App() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [productsByCategory, setProductsByCategory] = useState<
    Map<string, Product[]>
  >(new Map());
  const [layout, setLayout] = useState<AppSettings["layout"]>("grid");
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Product | null>(null);

  const [activeCategory, setActiveCategory] = useState<string>("");
  const sectionRefs = useRef<Record<string, HTMLElement | null>>({});
  const isClicking = useRef(false);

  useEffect(() => {
    async function load() {
      try {
        const [cats, prods, settings] = await Promise.all([
          getCategories(),
          getProducts({ status: "active" }),
          getSettings(),
        ]);

        const sorted = [...cats].sort((a, b) => a.order - b.order);
        setCategories(sorted);
        setLayout(settings.layout);

        const map = new Map<string, Product[]>();
        for (const p of prods) {
          const list = map.get(p.category_id) ?? [];
          list.push(p);
          map.set(p.category_id, list);
        }
        setProductsByCategory(map);
        if (sorted.length > 0) setActiveCategory(sorted[0].id);
      } catch {
        // Si falla, mostramos vacío
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // Scroll spy: resalta la categoría visible
  useEffect(() => {
    if (categories.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (isClicking.current) return;
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]) {
          setActiveCategory(visible[0].target.id);
        }
      },
      { rootMargin: "-140px 0px -55% 0px", threshold: [0, 0.25, 0.5, 1] }
    );
    Object.values(sectionRefs.current).forEach((el) => el && observer.observe(el));
    return () => observer.disconnect();
  }, [categories]);

  const handleSelectCategory = (id: string) => {
    setActiveCategory(id);
    isClicking.current = true;
    sectionRefs.current[id]?.scrollIntoView({ behavior: "smooth", block: "start" });
    window.setTimeout(() => {
      isClicking.current = false;
    }, 700);
  };

  if (loading) {
    return (
      <div className="min-h-dvh flex items-center justify-center bg-background">
        <p className="text-muted-foreground animate-pulse">Cargando carta...</p>
      </div>
    );
  }

  const hasProducts = categories.some(
    (cat) => (productsByCategory.get(cat.id) ?? []).length > 0
  );

  return (
    <div className="min-h-dvh bg-background">
      <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur-md">
        <div className="mx-auto max-w-2xl px-4">
          <div className="flex items-center justify-between gap-3 py-4">
            <h1 className="font-serif text-xl font-semibold leading-none">
              Nuestra Carta
            </h1>
          </div>
          {categories.length > 0 && (
            <nav
              aria-label="Categorías"
              className="-mx-4 overflow-x-auto px-4 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
            >
              <ul className="flex gap-1.5 pb-2">
                {categories.map((cat) => {
                  const active = cat.id === activeCategory;
                  return (
                    <li key={cat.id}>
                      <button
                        onClick={() => handleSelectCategory(cat.id)}
                        aria-current={active ? "true" : undefined}
                        className={`whitespace-nowrap rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                          active
                            ? "bg-primary text-primary-foreground"
                            : "bg-secondary text-secondary-foreground hover:bg-accent"
                        }`}
                      >
                        {cat.name}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </nav>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-2xl px-4">
        {hasProducts ? (
          <div className="mb-16">
            {categories.map((cat) => {
              const products = productsByCategory.get(cat.id) ?? [];
              if (products.length === 0) return null;
              return (
                <section
                  key={cat.id}
                  id={cat.id}
                  ref={(el) => {
                    sectionRefs.current[cat.id] = el;
                  }}
                  className="scroll-mt-32 pt-8"
                >
                  <h2 className="mb-4 font-serif text-2xl font-semibold">
                    {cat.name}
                  </h2>
                  <ProductLayout
                    variant={layout}
                    products={products}
                    onSelect={setSelected}
                  />
                </section>
              );
            })}
          </div>
        ) : (
          <p className="text-center text-muted-foreground py-16">
            No hay productos disponibles en este momento.
          </p>
        )}
      </main>

      <footer className="mx-auto max-w-2xl px-4 pb-12 pt-6 text-center text-xs text-muted-foreground">
        <p>Escaneá el QR para ver nuestra carta</p>
      </footer>

      <ProductDetailSheet product={selected} onClose={() => setSelected(null)} />
    </div>
  );
}
