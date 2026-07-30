import { useState, useEffect, useCallback } from "react";
import {
  getCategories,
  getAddOns,
  getProduct,
  createProduct,
  updateProduct,
  addAddOnToProduct,
  removeAddOnFromProduct,
  uploadImage,
} from "@menu/api-client";
import type { Category, AddOn, Product, ProductCreate } from "@menu/types";
import { Button, Input } from "@menu/ui";
import { Plus, Trash2, Upload } from "lucide-react";

interface Props {
  product: Product | null;
  onSuccess: () => void;
  onCancel: () => void;
}

export default function ProductForm({ product, onSuccess, onCancel }: Props) {
  const isEditing = !!product;

  const [categories, setCategories] = useState<Category[]>([]);
  const [addons, setAddOns] = useState<AddOn[]>([]);

  const [name, setName] = useState(product?.name ?? "");
  const [description, setDescription] = useState(product?.description ?? "");
  const [basePrice, setBasePrice] = useState(product?.base_price?.toString() ?? "");
  const [categoryId, setCategoryId] = useState(product?.category_id ?? "");
  const [imageUrl, setImageUrl] = useState(product?.image_url ?? "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);

  const [productAddons, setProductAddons] = useState<
    { addon_id: string; price_override: string }[]
  >(
    product?.addons?.map((pa) => ({
      addon_id: pa.addon.id,
      price_override: pa.price_override?.toString() ?? "",
    })) ?? []
  );
  const [selectedAddon, setSelectedAddon] = useState("");
  const [overridePrice, setOverridePrice] = useState("");

  useEffect(() => {
    getCategories().then(setCategories).catch(() => {});
    getAddOns().then(setAddOns).catch(() => {});
  }, []);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const { public_url } = await uploadImage(file);
      setImageUrl(public_url);
    } catch (err) {
      setError("Error al subir imagen");
    } finally {
      setUploading(false);
    }
  };

  const handleAddAddon = () => {
    if (!selectedAddon) return;
    if (productAddons.some((pa) => pa.addon_id === selectedAddon)) {
      alert("Ese adicional ya está asociado");
      return;
    }
    setProductAddons((prev) => [
      ...prev,
      { addon_id: selectedAddon, price_override: overridePrice },
    ]);
    setSelectedAddon("");
    setOverridePrice("");
  };

  const handleRemoveAddon = (addonId: string) => {
    setProductAddons((prev) => prev.filter((pa) => pa.addon_id !== addonId));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = {
        name,
        description,
        base_price: parseFloat(basePrice),
        category_id: categoryId,
        image_url: imageUrl || null,
      };

      let productId: string;
      if (isEditing) {
        await updateProduct(product!.id, data);
        productId = product!.id;
        const currentAddonIds = product!.addons.map((a) => a.addon.id);
        for (const addonId of currentAddonIds) {
          if (!productAddons.some((pa) => pa.addon_id === addonId)) {
            await removeAddOnFromProduct(productId, addonId);
          }
        }
      } else {
        const created = await createProduct(data as ProductCreate);
        productId = created.id;
      }
      for (const pa of productAddons) {
        const isNew =
          !product?.addons?.some((a) => a.addon.id === pa.addon_id);
        if (isNew) {
          await addAddOnToProduct(productId, {
            addon_id: pa.addon_id,
            price_override: pa.price_override ? parseFloat(pa.price_override) : null,
          });
        }
      }
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="text-sm font-medium block mb-1">Nombre</label>
        <Input
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="text-sm font-medium block mb-1">Descripción</label>
        <Input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm font-medium block mb-1">Precio base</label>
          <Input
            type="number"
            step="0.01"
            value={basePrice}
            onChange={(e) => setBasePrice(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="text-sm font-medium block mb-1">Categoría</label>
          <select
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            required
            className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          >
            <option value="">Seleccionar...</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="text-sm font-medium block mb-1">Imagen</label>
        <div className="flex items-center gap-3">
          <label className="cursor-pointer inline-flex items-center gap-2 text-sm bg-secondary hover:bg-secondary/80 rounded-md px-3 py-2 transition-colors">
            <Upload className="h-4 w-4" />
            {uploading ? "Subiendo..." : "Subir imagen"}
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleImageUpload}
              disabled={uploading}
            />
          </label>
          {imageUrl && (
            <img
              src={imageUrl}
              alt="Preview"
              className="h-10 w-10 rounded object-cover"
            />
          )}
        </div>
        {imageUrl && (
          <Input
            className="mt-2"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="URL de imagen"
          />
        )}
      </div>

      <div>
        <label className="text-sm font-medium block mb-2">Adicionales</label>
        <div className="space-y-2 mb-3">
          {productAddons.map((pa) => {
            const addon = addons.find((a) => a.id === pa.addon_id);
            return (
              <div
                key={pa.addon_id}
                className="flex items-center gap-2 p-2 rounded border text-sm"
              >
                <span className="flex-1">{addon?.name ?? pa.addon_id}</span>
                {pa.price_override && (
                  <span className="text-muted-foreground">
                    Precio especial: ${pa.price_override}
                  </span>
                )}
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  onClick={() => handleRemoveAddon(pa.addon_id)}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            );
          })}
        </div>
        <div className="flex gap-2">
          <select
            value={selectedAddon}
            onChange={(e) => setSelectedAddon(e.target.value)}
            className="flex-1 h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          >
            <option value="">Agregar adicional...</option>
            {addons
              .filter(
                (a) => !productAddons.some((pa) => pa.addon_id === a.id)
              )
              .map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name} (${Number(a.default_price).toFixed(2)})
                </option>
              ))}
          </select>
          <Input
            type="number"
            step="0.01"
            placeholder="Precio override"
            value={overridePrice}
            onChange={(e) => setOverridePrice(e.target.value)}
            className="w-36"
          />
          <Button type="button" variant="outline" size="sm" onClick={handleAddAddon}>
            <Plus className="h-3 w-3" />
          </Button>
        </div>
      </div>

      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}

      <div className="flex gap-2 pt-2">
        <Button type="submit" disabled={loading}>
          {loading ? "Guardando..." : isEditing ? "Guardar cambios" : "Crear producto"}
        </Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
      </div>
    </form>
  );
}
