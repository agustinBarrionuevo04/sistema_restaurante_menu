import { useState, useEffect } from "react";
import { getCategories, getProducts } from "@menu/api-client";
import type { Category, Product } from "@menu/types";
import { ProductCard } from "@menu/ui";
import { UtensilsCrossed } from "lucide-react";

export default function App() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [productsByCategory, setProductsByCategory] = useState<
    Map<string, Product[]>
  >(new Map());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [cats, prods] = await Promise.all([
          getCategories(),
          getProducts({ status: "active" }),
        ]);

        setCategories(cats);

        const map = new Map<string, Product[]>();
        for (const p of prods) {
          const list = map.get(p.category_id) ?? [];
          list.push(p);
          map.set(p.category_id, list);
        }
        setProductsByCategory(map);
      } catch {
        // Si falla, mostramos vacío
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground animate-pulse">Cargando carta...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-white">
      <header className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b">
        <div className="max-w-lg mx-auto px-4 py-4 flex items-center gap-3">
          <UtensilsCrossed className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-bold tracking-tight">Nuestra Carta</h1>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-8">
        {categories.map((cat) => {
          const products = productsByCategory.get(cat.id) ?? [];
          if (products.length === 0) return null;
          return (
            <section key={cat.id}>
              <h2 className="text-lg font-bold mb-4 pb-2 border-b">
                {cat.name}
              </h2>
              <div className="space-y-4">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            </section>
          );
        })}

        {categories.every(
          (cat) => (productsByCategory.get(cat.id) ?? []).length === 0
        ) && (
          <p className="text-center text-muted-foreground py-12">
            No hay productos disponibles en este momento.
          </p>
        )}
      </main>

      <footer className="max-w-lg mx-auto px-4 py-8 text-center text-xs text-muted-foreground">
        Escaneá el QR para ver nuestra carta
      </footer>
    </div>
  );
}
