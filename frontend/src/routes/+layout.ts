import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';

export const prerender = true;
export const ssr = false;
export const trailingSlash = 'always';

export const load: LayoutLoad = async ({ url }) => {
	const publicPaths = ['/'];
	const isPublic = publicPaths.includes(url.pathname);

	if (browser && !isPublic) {
		const token = localStorage.getItem('access_token');
		if (!token) {
			throw redirect(307, '/');
		}
	}

	return {};
};
