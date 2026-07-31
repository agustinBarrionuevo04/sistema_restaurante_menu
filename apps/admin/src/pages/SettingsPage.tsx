import { useState, useEffect, useCallback } from "react";
import { getSettings, updateSettings } from "@menu/api-client";
import type { LayoutVariant } from "@menu/types";
import { Button, Card, CardHeader, CardTitle, CardContent } from "@menu/ui";

const layoutOptions: { value: LayoutVariant; label: string; desc: string }[] = [
  { value: "grid", label: "Grilla", desc: "Tarjetas en 2 columnas con foto arriba" },
  { value: "list", label: "Lista", desc: "Filas con foto a la izquierda" },
  { value: "carousel", label: "Carrusel", desc: "Deslizamiento horizontal por categoría" },
];

export default function SettingsPage() {
  const [layout, setLayout] = useState<LayoutVariant>("grid");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const fetchSettings = useCallback(async () => {
    try {
      const settings = await getSettings();
      setLayout(settings.layout);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Error al cargar configuración");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const handleSave = async () => {
    setSaving(true);
    setMessage("");
    try {
      await updateSettings({ layout });
      setMessage("Configuración guardada.");
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Error al guardar");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-muted-foreground">Cargando...</p>;
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Configuración</h2>

      <Card className="max-w-xl">
        <CardHeader>
          <CardTitle className="text-lg">Diseño de la carta</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground mb-4">
            Elegí cómo se muestra la carta pública a tus clientes.
          </p>
          <div className="flex flex-col gap-2">
            {layoutOptions.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setLayout(opt.value)}
                className={`flex items-start gap-3 rounded-lg border p-4 text-left transition-colors ${
                  layout === opt.value
                    ? "border-primary bg-primary/5"
                    : "border-border hover:bg-muted"
                }`}
              >
                <input
                  type="radio"
                  name="layout"
                  checked={layout === opt.value}
                  onChange={() => setLayout(opt.value)}
                  className="mt-0.5 accent-[hsl(var(--primary))]"
                />
                <span>
                  <span className="block font-medium">{opt.label}</span>
                  <span className="block text-sm text-muted-foreground">
                    {opt.desc}
                  </span>
                </span>
              </button>
            ))}
          </div>

          {message && <p className="text-sm text-muted-foreground mt-4">{message}</p>}

          <div className="mt-5">
            <Button onClick={handleSave} disabled={saving}>
              {saving ? "Guardando..." : "Guardar"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
