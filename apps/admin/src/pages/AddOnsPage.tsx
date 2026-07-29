import { useState, useEffect, useCallback } from "react";
import {
  getAddOns,
  createAddOn,
  updateAddOn,
  deleteAddOn,
} from "@menu/api-client";
import type { AddOn } from "@menu/types";
import { Button, Input, Card, CardHeader, CardTitle, CardContent } from "@menu/ui";
import { Plus, Pencil, Trash2 } from "lucide-react";

export default function AddOnsPage() {
  const [addons, setAddOns] = useState<AddOn[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<AddOn | null>(null);
  const [name, setName] = useState("");
  const [defaultPrice, setDefaultPrice] = useState("");

  const fetchAddOns = useCallback(async () => {
    try {
      const data = await getAddOns();
      setAddOns(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar adicionales");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAddOns();
  }, [fetchAddOns]);

  const resetForm = () => {
    setShowForm(false);
    setEditing(null);
    setName("");
    setDefaultPrice("");
    setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const data = { name, default_price: parseFloat(defaultPrice) };
      if (editing) {
        await updateAddOn(editing.id, data);
      } else {
        await createAddOn(data);
      }
      resetForm();
      fetchAddOns();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar");
    }
  };

  const handleEdit = (addon: AddOn) => {
    setEditing(addon);
    setName(addon.name);
    setDefaultPrice(addon.default_price.toString());
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("¿Eliminar este adicional?")) return;
    try {
      await deleteAddOn(id);
      fetchAddOns();
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
        <h2 className="text-2xl font-bold">Adicionales</h2>
        <Button
          onClick={() => {
            resetForm();
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
              {editing ? "Editar adicional" : "Nuevo adicional"}
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
                  placeholder="Ej: Extra queso"
                />
              </div>
              <div>
                <label className="text-sm font-medium block mb-1">
                  Precio por defecto
                </label>
                <Input
                  type="number"
                  step="0.01"
                  value={defaultPrice}
                  onChange={(e) => setDefaultPrice(e.target.value)}
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
        {addons.map((addon) => (
          <div
            key={addon.id}
            className="flex items-center gap-3 p-3 rounded-lg border bg-card"
          >
            <div className="flex-1">
              <p className="font-medium">{addon.name}</p>
              <p className="text-sm text-muted-foreground">
                ${Number(addon.default_price).toFixed(2)}
              </p>
            </div>
            <Button variant="ghost" size="icon" onClick={() => handleEdit(addon)}>
              <Pencil className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={() => handleDelete(addon.id)}>
              <Trash2 className="h-4 w-4 text-destructive" />
            </Button>
          </div>
        ))}
        {addons.length === 0 && (
          <p className="text-muted-foreground text-center py-8">
            No hay adicionales. Creá el primero.
          </p>
        )}
      </div>
    </div>
  );
}
