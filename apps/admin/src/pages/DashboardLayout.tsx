import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { Button } from "@menu/ui";
import { LayoutGrid, Package, PlusCircle, Settings, LogOut } from "lucide-react";

const navItems = [
  { to: "/categories", label: "Categorías", icon: LayoutGrid },
  { to: "/products", label: "Productos", icon: Package },
  { to: "/addons", label: "Adicionales", icon: PlusCircle },
  { to: "/settings", label: "Configuración", icon: Settings },
];

export default function DashboardLayout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex">
      <aside className="w-60 border-r bg-muted/10 p-4 flex flex-col">
        <h1 className="text-lg font-bold mb-6 px-3">Carta Digital</h1>
        <nav className="flex-1 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors ${
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted"
                }`
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
        <Button variant="ghost" className="justify-start" onClick={handleLogout}>
          <LogOut className="h-4 w-4 mr-2" />
          Salir
        </Button>
      </aside>
      <main className="flex-1 p-6 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
