export type ProductStatus = "active" | "suspended";

export type LayoutVariant = "list" | "grid" | "carousel";

export interface AppSettings {
  layout: LayoutVariant;
}

export interface Category {
  id: string;
  name: string;
  order: number;
}

export interface AddOn {
  id: string;
  name: string;
  default_price: number;
}

export interface ProductAddOn {
  addon: AddOn;
  price_override: number | null;
}

export interface Product {
  id: string;
  category_id: string;
  name: string;
  description: string;
  base_price: number;
  image_url: string | null;
  status: ProductStatus;
  addons: ProductAddOn[];
}

export interface CategoryCreate {
  name: string;
  order?: number;
}

export interface CategoryUpdate {
  name?: string;
  order?: number;
}

export interface ProductCreate {
  category_id: string;
  name: string;
  description?: string;
  base_price: number;
  image_url?: string | null;
  status?: ProductStatus;
}

export interface ProductUpdate {
  category_id?: string;
  name?: string;
  description?: string;
  base_price?: number;
  image_url?: string | null;
  status?: ProductStatus;
}

export interface AddOnCreate {
  name: string;
  default_price: number;
}

export interface AddOnUpdate {
  name?: string;
  default_price?: number;
}

export interface ProductAddOnCreate {
  addon_id: string;
  price_override?: number | null;
}

export interface PresignRequest {
  filename: string;
  content_type?: string;
}

export interface PresignResponse {
  upload_url: string;
  public_url: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}
