import * as React from "react";
import { X } from "lucide-react";
import type { Product, ProductAddOn } from "@menu/types";
import { cn, formatPrice } from "../lib/utils";

function addonPrice(addon: ProductAddOn): number {
  return Number(addon.price_override ?? addon.addon.default_price);
}

interface ProductDetailSheetProps {
  product: Product | null;
  onClose: () => void;
}

export function ProductDetailSheet({ product, onClose }: ProductDetailSheetProps) {
  const open = product !== null;

  React.useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!product) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center sm:items-center"
      role="dialog"
      aria-modal="true"
      aria-label={product.name}
    >
      {/* Backdrop */}
      <button
        aria-label="Cerrar"
        onClick={onClose}
        className="absolute inset-0 animate-in fade-in bg-foreground/40 duration-200"
      />

      {/* Panel */}
      <div
        className={cn(
          "relative flex max-h-[92vh] w-full flex-col overflow-hidden rounded-t-2xl bg-card",
          "sm:max-w-md sm:rounded-2xl animate-in slide-in-from-bottom-4 duration-300"
        )}
      >
        {/* drag handle */}
        <div className="pointer-events-none absolute left-1/2 top-2 z-10 h-1 w-10 -translate-x-1/2 rounded-full bg-foreground/20 sm:hidden" />

        <button
          onClick={onClose}
          aria-label="Cerrar"
          className="absolute right-3 top-3 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-background/80 text-foreground backdrop-blur transition-colors hover:bg-background"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="overflow-y-auto overscroll-contain">
          <div className="aspect-[4/3] w-full overflow-hidden bg-muted">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.name}
                className="h-full w-full object-cover"
              />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-sm text-muted-foreground">
                Sin foto
              </div>
            )}
          </div>

          <div className="px-5 pb-8 pt-5">
            <div className="flex items-start justify-between gap-4">
              <h2 className="font-serif text-2xl font-semibold leading-tight text-balance">
                {product.name}
              </h2>
              <span className="shrink-0 font-serif text-2xl font-semibold text-primary">
                {formatPrice(product.base_price)}
              </span>
            </div>

            {product.description && (
              <p className="mt-3 leading-relaxed text-muted-foreground text-pretty">
                {product.description}
              </p>
            )}

            {product.addons && product.addons.length > 0 && (
              <div className="mt-6">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Adicionales
                </h3>
                <ul className="mt-3 divide-y divide-border">
                  {product.addons.map((pa) => (
                    <li
                      key={pa.addon.id}
                      className="flex items-center justify-between py-2.5 text-sm"
                    >
                      <span className="text-foreground">{pa.addon.name}</span>
                      <span className="font-medium text-muted-foreground">
                        {addonPrice(pa) === 0
                          ? "Sin cargo"
                          : `+ ${formatPrice(addonPrice(pa))}`}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <p className="mt-6 rounded-lg bg-secondary px-4 py-3 text-center text-xs text-secondary-foreground">
              Realizá tu pedido en el mostrador.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
