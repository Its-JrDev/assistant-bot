<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { GraduationCap } from '@lucide/svelte';
	import { goto } from '$app/navigation';

	let username = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	function isValidRole(role: unknown): role is 'directivo' | 'profesor' {
		return role === 'directivo' || role === 'profesor';
	}

	async function handleLogin() {
		error = '';
		loading = true;
		try {
			const tokens = await api.login(username, password);

			const payload = JSON.parse(atob(tokens.access.split('.')[1]));
			const role = payload.role ?? 'profesor';

			auth.login(tokens.access, tokens.refresh, {
				username,
				role: isValidRole(role) ? role : 'profesor',
			});

			goto('/dashboard');
		} catch (e: unknown) {
			const err = e as { details?: { detail?: string }; message?: string };
			error = err.details?.detail ?? err.message ?? 'Error al iniciar sesión';
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-muted/50">
	<Card class="w-full max-w-sm">
		<CardHeader class="space-y-1 text-center">
			<div class="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-primary">
				<GraduationCap class="h-6 w-6 text-primary-foreground" />
			</div>
			<CardTitle class="text-xl">Panel Escolar</CardTitle>
			<CardDescription>Ingresá tus credenciales</CardDescription>
		</CardHeader>
		<CardContent>
			<form onsubmit={(e) => { e.preventDefault(); handleLogin(); }} class="space-y-4">
				{#if error}
					<div class="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>
				{/if}
				<div class="space-y-2">
					<label class="text-sm font-medium leading-none" for="username">Usuario</label>
					<Input id="username" type="text" placeholder="usuario" bind:value={username} required />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium leading-none" for="password">Contraseña</label>
					<Input id="password" type="password" placeholder="••••••" bind:value={password} required />
				</div>
				<Button type="submit" class="w-full" disabled={loading}>
					{loading ? 'Ingresando…' : 'Ingresar'}
				</Button>
			</form>
		</CardContent>
	</Card>
</div>
