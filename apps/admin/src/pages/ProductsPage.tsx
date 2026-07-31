import { useState, useEffect, useCallback } from "react";
import { getProducts, createProduct, updateProduct, deleteProduct } from "@menu/api-client";
import type { Product, ProductCreate } from "@menu/types";
import { Button, Badge, Card, CardHeader, CardTitle, CardContent } from "@menu/ui";
import { Plus, Pencil, Trash2 } from "lucide-react";
import ProductForm from "../components/ProductForm";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Product | null>(null);

  const fetchProducts = useCallback(async () => {
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar productos");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleToggleStatus = async (product: Product) => {
    const newStatus = product.status === "active" ? "suspended" : "active";
    try {
      await updateProduct(product.id, { status: newStatus });
      fetchProducts();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al cambiar estado");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("¿Eliminar definitivamente este producto?")) return;
    try {
      await deleteProduct(id);
      fetchProducts();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al eliminar");
    }
  };

  if (loading) {
    return <p className="text-muted-foreground">Cargando...</p>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Productos</h2>
        <Button
          onClick={() => {
            setEditing(null);
            setShowForm(true);
          }}
        >
          <Plus className="h-4 w-4 mr-2" />
          Nuevo
        </Button>
      </div>

      {error && (
        <p className="text-sm text-destructive mb-4">{error}</p>
      )}

      {showForm && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-lg">
              {editing ? "Editar producto" : "Nuevo producto"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ProductForm
              product={editing}
              onSuccess={() => {
                setShowForm(false);
                setEditing(null);
                fetchProducts();
              }}
              onCancel={() => {
                setShowForm(false);
                setEditing(null);
              }}
            />
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        {products.map((product) => (
          <div
            key={product.id}
            className="flex h-full flex-col overflow-hidden rounded-xl border bg-card"
          >
            {product.image_url && (
              <img
                src={product.image_url}
                alt={product.name}
                className="aspect-[4/3] w-full object-cover"
              />
            )}
            <div className="flex flex-1 flex-col p-3">
              <div className="flex items-start justify-between gap-2">
                <p className="font-medium line-clamp-1">{product.name}</p>
                <Badge
                  variant={product.status === "active" ? "success" : "warning"}
                  className="shrink-0 text-xs"
                >
                  {product.status === "active" ? "Activo" : "Suspendido"}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground mt-1">
                ${Number(product.base_price).toFixed(2)}
                {product.addons.length > 0 &&
                  ` · ${product.addons.length} adicionales`}
              </p>
              <div className="mt-auto flex items-center gap-1 pt-3">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1"
                  onClick={() => handleToggleStatus(product)}
                >
                  {product.status === "active" ? "Suspender" : "Activar"}
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => {
                    setEditing(product);
                    setShowForm(true);
                  }}
                >
                  <Pencil className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={() => handleDelete(product.id)}>
                  <Trash2 className="h-4 w-4 text-destructive" />
                </Button>
              </div>
            </div>
          </div>
        ))}
        {products.length === 0 && (
          <p className="text-muted-foreground text-center py-8 col-span-full">
            No hay productos. Creá el primero.
          </p>
        )}
      </div>
    </div>
  );
}
