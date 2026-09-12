import { atom } from 'nanostores';

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

export const $user = atom<User | null>(null);
export const $isAuthenticated = atom<boolean>(false);

export function setUser(user: User | null) {
  $user.set(user);
  $isAuthenticated.set(!!user);
}

export function logout() {
  document.cookie = 'token=; Path=/; Max-Age=0';
  $user.set(null);
  $isAuthenticated.set(false);
  window.location.href = '/login';
}
