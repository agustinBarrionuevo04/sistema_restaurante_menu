import * as React from "react";
import type { Product, ProductAddOn, LayoutVariant } from "@menu/types";
import { cn, formatPrice } from "../lib/utils";

function addonPrice(addon: ProductAddOn): number {
  return Number(addon.price_override ?? addon.addon.default_price);
}

function Photo({ product, className }: { product: Product; className?: string }) {
  if (!product.image_url) {
    return (
      <div
        className={cn(
          "flex items-center justify-center bg-muted",
          className
        )}
      >
        <span className="text-xs text-muted-foreground">Sin foto</span>
      </div>
    );
  }
  return (
    <div className={cn("overflow-hidden bg-muted", className)}>
      <img
        src={product.image_url}
        alt={product.name}
        loading="lazy"
        className="h-full w-full object-cover transition-transform duration-300 active:scale-[1.02]"
      />
    </div>
  );
}

export interface ProductSelectProps {
  products: Product[];
  onSelect: (product: Product) => void;
  className?: string;
}

/* Grilla — 2 columnas con foto arriba */
export function ProductGrid({ products, onSelect, className }: ProductSelectProps) {
  return (
    <ul className={cn("grid grid-cols-2 gap-3", className)}>
      {products.map((product) => (
        <li key={product.id}>
          <button
            onClick={() => onSelect(product)}
            className="flex h-full w-full flex-col overflow-hidden rounded-xl border bg-card text-left transition-colors hover:bg-accent/40"
          >
            <Photo product={product} className="aspect-[4/3] w-full" />
            <div className="flex flex-1 flex-col p-3">
              <h3 className="font-serif text-base font-semibold leading-snug text-balance">
                {product.name}
              </h3>
              <p className="mt-1 line-clamp-2 flex-1 text-sm leading-relaxed text-muted-foreground">
                {product.description}
              </p>
              <span className="mt-2 font-serif text-base font-semibold text-primary">
                {formatPrice(product.base_price)}
              </span>
            </div>
          </button>
        </li>
      ))}
    </ul>
  );
}

/* Lista — foto a la izquierda */
export function ProductList({ products, onSelect, className }: ProductSelectProps) {
  return (
    <ul className={cn("flex flex-col gap-2.5", className)}>
      {products.map((product) => (
        <li key={product.id}>
          <button
            onClick={() => onSelect(product)}
            className="flex w-full items-stretch gap-3 rounded-xl border bg-card p-2.5 text-left transition-colors hover:bg-accent/40"
          >
            <Photo product={product} className="aspect-[4/3] w-28 shrink-0 rounded-lg sm:w-36" />
            <div className="flex min-w-0 flex-1 flex-col justify-center py-1 pr-1">
              <div className="flex items-start justify-between gap-3">
                <h3 className="font-serif text-lg font-semibold leading-snug text-balance">
                  {product.name}
                </h3>
                <span className="shrink-0 font-serif text-lg font-semibold text-primary">
                  {formatPrice(product.base_price)}
                </span>
              </div>
              <p className="mt-1 line-clamp-2 text-sm leading-relaxed text-muted-foreground">
                {product.description}
              </p>
            </div>
          </button>
        </li>
      ))}
    </ul>
  );
}

/* Carrusel — deslizamiento horizontal */
export function ProductCarousel({ products, onSelect, className }: ProductSelectProps) {
  return (
    <div
      className={cn(
        "-mx-4 overflow-x-auto px-4 pb-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
        className
      )}
    >
      <ul className="flex snap-x snap-mandatory gap-3">
        {products.map((product) => (
          <li key={product.id} className="w-60 shrink-0 snap-start">
            <button
              onClick={() => onSelect(product)}
              className="flex h-full w-full flex-col overflow-hidden rounded-xl border bg-card text-left transition-colors hover:bg-accent/40"
            >
              <Photo product={product} className="aspect-[4/3] w-full" />
              <div className="flex flex-1 flex-col p-3.5">
                <h3 className="font-serif text-lg font-semibold leading-snug text-balance">
                  {product.name}
                </h3>
                <p className="mt-1 line-clamp-2 flex-1 text-sm leading-relaxed text-muted-foreground">
                  {product.description}
                </p>
                <span className="mt-2 font-serif text-lg font-semibold text-primary">
                  {formatPrice(product.base_price)}
                </span>
              </div>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ProductLayout({
  variant,
  products,
  onSelect,
  className,
}: ProductSelectProps & { variant: LayoutVariant }) {
  if (variant === "list") {
    return <ProductList products={products} onSelect={onSelect} className={className} />;
  }
  if (variant === "carousel") {
    return <ProductCarousel products={products} onSelect={onSelect} className={className} />;
  }
  return <ProductGrid products={products} onSelect={onSelect} className={className} />;
}
