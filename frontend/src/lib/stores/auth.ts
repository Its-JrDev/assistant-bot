import { writable } from 'svelte/store';

function createAuthStore() {
	const stored = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
	const { subscribe, set, update } = writable<{ token: string | null; user: { username: string; role: string } | null }>({
		token: stored,
		user: null,
	});

	return {
		subscribe,
		login(token: string, refresh: string, user: { username: string; role: string }) {
			localStorage.setItem('access_token', token);
			localStorage.setItem('refresh_token', refresh);
			set({ token, user });
		},
		logout() {
			localStorage.removeItem('access_token');
			localStorage.removeItem('refresh_token');
			set({ token: null, user: null });
		},
		setUser(user: { username: string; role: string }) {
			update((state) => ({ ...state, user }));
		},
	};
}

export const auth = createAuthStore();

export function isAuthenticated() {
	let val = false;
	auth.subscribe((v) => (val = !!v.token))();
	return val;
}
