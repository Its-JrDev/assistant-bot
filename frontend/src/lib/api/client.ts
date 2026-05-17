const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api';

type FetchFn = typeof fetch;

interface RequestConfig {
	method?: string;
	body?: unknown;
	params?: Record<string, string>;
	token?: string;
	fetch?: FetchFn;
}

interface ApiError {
	status: number;
	message: string;
	details?: unknown;
}

export class ApiClient {
	private baseUrl: string;

	constructor(baseUrl: string = API_BASE) {
		this.baseUrl = baseUrl.replace(/\/$/, '');
	}

	private getToken(): string | null {
		try {
			return localStorage.getItem('access_token');
		} catch {
			return null;
		}
	}

	private async request<T>(endpoint: string, config: RequestConfig = {}): Promise<T> {
		const { method = 'GET', body, params, token } = config;
		const localFetch = config.fetch ?? fetch;

		const url = new URL(`${this.baseUrl}${endpoint}`);
		if (params) {
			Object.entries(params).forEach(([key, value]) => url.searchParams.set(key, value));
		}

		const headers: Record<string, string> = {
			'Content-Type': 'application/json',
		};

		const authToken = token ?? this.getToken();
		if (authToken) {
			headers['Authorization'] = `Bearer ${authToken}`;
		}

		const response = await localFetch(url.toString(), {
			method,
			headers,
			body: body ? JSON.stringify(body) : undefined,
		});

		if (!response.ok) {
			const error: ApiError = {
				status: response.status,
				message: response.statusText,
			};
			try {
				error.details = await response.json();
			} catch {
				// ignore
			}
			throw error;
		}

		if (response.status === 204) return undefined as T;

		return response.json() as Promise<T>;
	}

	get<T>(endpoint: string, config?: RequestConfig) {
		return this.request<T>(endpoint, { ...config, method: 'GET' });
	}

	post<T>(endpoint: string, body?: unknown, config?: RequestConfig) {
		return this.request<T>(endpoint, { ...config, method: 'POST', body });
	}

	patch<T>(endpoint: string, body?: unknown, config?: RequestConfig) {
		return this.request<T>(endpoint, { ...config, method: 'PATCH', body });
	}

	delete<T>(endpoint: string, config?: RequestConfig) {
		return this.request<T>(endpoint, { ...config, method: 'DELETE' });
	}

	async login(username: string, password: string): Promise<{ access: string; refresh: string }> {
		const result = await this.request<{ access: string; refresh: string }>('/token/', {
			method: 'POST',
			body: { username, password },
			token: undefined,
		});
		localStorage.setItem('access_token', result.access);
		localStorage.setItem('refresh_token', result.refresh);
		return result;
	}

	logout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
	}
}

export const api = new ApiClient();
