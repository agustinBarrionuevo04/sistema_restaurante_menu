import { useState, useEffect, useCallback } from "react";
import { getCategories, createCategory, updateCategory, deleteCategory } from "@menu/api-client";
import type { Category } from "@menu/types";
import { Button, Input, Card, CardHeader, CardTitle, CardContent } from "@menu/ui";
import { Plus, Pencil, Trash2, GripVertical } from "lucide-react";

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Category | null>(null);
  const [name, setName] = useState("");
  const [order, setOrder] = useState(0);

  const fetchCategories = useCallback(async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar categorías");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  const resetForm = () => {
    setShowForm(false);
    setEditing(null);
    setName("");
    setOrder(0);
    setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (editing) {
        await updateCategory(editing.id, { name, order });
      } else {
        await createCategory({ name, order });
      }
      resetForm();
      fetchCategories();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar");
    }
  };

  const handleEdit = (cat: Category) => {
    setEditing(cat);
    setName(cat.name);
    setOrder(cat.order);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("¿Eliminar esta categoría?")) return;
    try {
      await deleteCategory(id);
      fetchCategories();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al eliminar");
    }
  };

  const handleMoveUp = async (cat: Category, idx: number) => {
    if (idx === 0) return;
    const prev = categories[idx - 1];
    await updateCategory(cat.id, { order: prev.order });
    await updateCategory(prev.id, { order: cat.order });
    fetchCategories();
  };

  const handleMoveDown = async (cat: Category, idx: number) => {
    if (idx === categories.length - 1) return;
    const next = categories[idx + 1];
    await updateCategory(cat.id, { order: next.order });
    await updateCategory(next.id, { order: cat.order });
    fetchCategories();
  };

  if (loading) {
    return <p className="text-muted-foreground">Cargando...</p>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Categorías</h2>
        <Button
          onClick={() => {
            resetForm();
            setShowForm(true);
          }}
        >
          <Plus className="h-4 w-4 mr-2" />
          Nueva
        </Button>
      </div>

      {error && (
        <p className="text-sm text-destructive mb-4">{error}</p>
      )}

      {showForm && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-lg">
              {editing ? "Editar categoría" : "Nueva categoría"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-sm font-medium block mb-1">Nombre</label>
                <Input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  placeholder="Ej: Entradas"
                />
              </div>
              <div>
                <label className="text-sm font-medium block mb-1">Orden</label>
                <Input
                  type="number"
                  value={order}
                  onChange={(e) => setOrder(Number(e.target.value))}
                  required
                />
              </div>
              <div className="flex gap-2">
                <Button type="submit">
                  {editing ? "Guardar cambios" : "Crear"}
                </Button>
                <Button type="button" variant="outline" onClick={resetForm}>
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="space-y-2">
        {categories.map((cat, idx) => (
          <div
            key={cat.id}
            className="flex items-center gap-3 p-3 rounded-lg border bg-card"
          >
            <div className="flex flex-col gap-0.5">
              <button
                onClick={() => handleMoveUp(cat, idx)}
                className="text-muted-foreground hover:text-foreground"
                title="Subir"
              >
                ▲
              </button>
              <button
                onClick={() => handleMoveDown(cat, idx)}
                className="text-muted-foreground hover:text-foreground"
                title="Bajar"
              >
                ▼
              </button>
            </div>
            <GripVertical className="h-4 w-4 text-muted-foreground" />
            <div className="flex-1">
              <p className="font-medium">{cat.name}</p>
              <p className="text-xs text-muted-foreground">Orden: {cat.order}</p>
            </div>
            <Button variant="ghost" size="icon" onClick={() => handleEdit(cat)}>
              <Pencil className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={() => handleDelete(cat.id)}>
              <Trash2 className="h-4 w-4 text-destructive" />
            </Button>
          </div>
        ))}
        {categories.length === 0 && (
          <p className="text-muted-foreground text-center py-8">
            No hay categorías. Creá la primera.
          </p>
        )}
      </div>
    </div>
  );
}
