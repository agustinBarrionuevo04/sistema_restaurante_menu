import { useState, useEffect, useCallback } from "react";
import { getProducts, createProduct, updateProduct, deleteProduct } from "@menu/api-client";
import type { Product, ProductCreate } from "@menu/types";
import { Button, Input, Badge, Card, CardHeader, CardTitle, CardContent } from "@menu/ui";
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

      <div className="space-y-2">
        {products.map((product) => (
          <div
            key={product.id}
            className="flex items-center gap-4 p-3 rounded-lg border bg-card"
          >
            {product.image_url && (
              <img
                src={product.image_url}
                alt={product.name}
                className="h-14 w-14 rounded-md object-cover shrink-0"
              />
            )}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <p className="font-medium truncate">{product.name}</p>
                <Badge
                  variant={product.status === "active" ? "success" : "warning"}
                  className="text-xs"
                >
                  {product.status === "active" ? "Activo" : "Suspendido"}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">
                ${Number(product.base_price).toFixed(2)}
                {product.addons.length > 0 &&
                  ` · ${product.addons.length} adicionales`}
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
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
        ))}
        {products.length === 0 && (
          <p className="text-muted-foreground text-center py-8">
            No hay productos. Creá el primero.
          </p>
        )}
      </div>
    </div>
  );
}
