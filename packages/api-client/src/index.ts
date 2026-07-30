import type {
  Category,
  CategoryCreate,
  CategoryUpdate,
  Product,
  ProductCreate,
  ProductUpdate,
  AddOn,
  AddOnCreate,
  AddOnUpdate,
  ProductAddOn,
  ProductAddOnCreate,
  PresignRequest,
  PresignResponse,
  TokenResponse,
  LoginRequest,
} from "@menu/types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function getToken(): string | null {
  return localStorage.getItem("access_token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...((options.headers as Record<string, string>) ?? {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (options.body && typeof options.body === "string") {
    headers["Content-Type"] = headers["Content-Type"] ?? "application/json";
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(
      (detail as { detail?: string }).detail ?? `Error ${res.status}`
    );
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// Categories
export function getCategories(): Promise<Category[]> {
  return request<Category[]>("/categories");
}

export function createCategory(data: CategoryCreate): Promise<Category> {
  return request<Category>("/categories", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateCategory(
  id: string,
  data: CategoryUpdate
): Promise<Category> {
  return request<Category>(`/categories/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteCategory(id: string): Promise<void> {
  return request<void>(`/categories/${id}`, { method: "DELETE" });
}

// Products
export function getProducts(params?: {
  category_id?: string;
  status?: string;
}): Promise<Product[]> {
  const search = new URLSearchParams();
  if (params?.category_id) search.set("category_id", params.category_id);
  if (params?.status) search.set("status", params.status);
  const qs = search.toString();
  return request<Product[]>(`/products${qs ? `?${qs}` : ""}`);
}

export function getProduct(id: string): Promise<Product> {
  return request<Product>(`/products/${id}`);
}

export function createProduct(data: ProductCreate): Promise<Product> {
  return request<Product>("/products", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateProduct(
  id: string,
  data: ProductUpdate
): Promise<Product> {
  return request<Product>(`/products/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteProduct(id: string): Promise<void> {
  return request<void>(`/products/${id}`, { method: "DELETE" });
}

// AddOns
export function getAddOns(): Promise<AddOn[]> {
  return request<AddOn[]>("/addons");
}

export function createAddOn(data: AddOnCreate): Promise<AddOn> {
  return request<AddOn>("/addons", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateAddOn(
  id: string,
  data: AddOnUpdate
): Promise<AddOn> {
  return request<AddOn>(`/addons/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteAddOn(id: string): Promise<void> {
  return request<void>(`/addons/${id}`, { method: "DELETE" });
}

// Product-AddOn associations
export function addAddOnToProduct(
  productId: string,
  data: ProductAddOnCreate
): Promise<ProductAddOn> {
  return request<ProductAddOn>(`/products/${productId}/addons`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function removeAddOnFromProduct(
  productId: string,
  addonId: string
): Promise<void> {
  return request<void>(`/products/${productId}/addons/${addonId}`, {
    method: "DELETE",
  });
}

// Uploads
export function presignUpload(data: PresignRequest): Promise<PresignResponse> {
  return request<PresignResponse>("/uploads/presign", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function uploadImage(file: File): Promise<PresignResponse> {
  const token = getToken();
  const headers: Record<string, string> = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/uploads/local`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(
      (detail as { detail?: string }).detail ?? `Error ${res.status}`
    );
  }

  return res.json();
}

// Auth
export function login(data: LoginRequest): Promise<TokenResponse> {
  return request<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
