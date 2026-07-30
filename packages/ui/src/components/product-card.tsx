import * as React from "react";
import type { Product, ProductAddOn } from "@menu/types";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { cn } from "../lib/utils";

interface ProductCardProps {
  product: Product;
  className?: string;
}

function addonPrice(addon: ProductAddOn): number {
  return Number(addon.price_override ?? addon.addon.default_price);
}

export function ProductCard({ product, className }: ProductCardProps) {
  return (
    <Card className={cn("overflow-hidden", className)}>
      {product.image_url && (
        <div className="aspect-[4/3] overflow-hidden">
          <img
            src={product.image_url}
            alt={product.name}
            className="h-full w-full object-cover"
          />
        </div>
      )}
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-lg">{product.name}</h3>
          <Badge variant="secondary" className="shrink-0 text-base font-semibold">
            ${Number(product.base_price).toFixed(2)}
          </Badge>
        </div>
        {product.description && (
          <p className="text-sm text-muted-foreground mt-1">
            {product.description}
          </p>
        )}
        {product.addons.length > 0 && (
          <div className="mt-3 border-t pt-3">
            <p className="text-xs font-medium text-muted-foreground mb-2">
              Adicionales disponibles
            </p>
            <ul className="space-y-1">
              {product.addons.map((pa) => (
                <li
                  key={pa.addon.id}
                  className="flex justify-between text-sm"
                >
                  <span>{pa.addon.name}</span>
                  <span className="text-muted-foreground">
                    +${addonPrice(pa).toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
