<script lang="ts">
	import '../app.css';
	import { auth } from '$lib/stores/auth';
	import { page } from '$app/stores';
	import { BookOpen, Calendar, Home, LogOut, Users, GraduationCap, Clock, Menu, X } from '@lucide/svelte';

	let { children } = $props();

	let sidebarOpen = $state(false);

	const navItems = [
		{ href: '/dashboard', label: 'Dashboard', icon: Home },
		{ href: '/events', label: 'Eventos', icon: Calendar },
		{ href: '/tasks', label: 'Tareas', icon: BookOpen },
		{ href: '/schedules', label: 'Horarios', icon: Clock },
		{ href: '/grades', label: 'Notas', icon: GraduationCap },
		{ href: '/students', label: 'Estudiantes', icon: Users },
	];

	function handleLogout() {
		auth.logout();
		window.location.href = '/';
	}
</script>

<svelte:head>
	<title>Panel Escolar</title>
</svelte:head>

{#if $auth.token}
	<div class="flex h-screen overflow-hidden bg-background">
		<aside
			class="fixed inset-y-0 left-0 z-50 w-64 border-r bg-card transition-transform duration-200 max-lg:-translate-x-full"
			class:max-lg:translate-x-0={sidebarOpen}
		>
			<div class="flex h-14 items-center border-b px-6">
				<a href="/dashboard" class="flex items-center gap-2 font-semibold">
					<GraduationCap class="h-5 w-5" />
					<span>Panel Escolar</span>
				</a>
				<button class="ml-auto lg:hidden" onclick={() => sidebarOpen = false}>
					<X class="h-5 w-5" />
				</button>
			</div>
			<nav class="flex flex-1 flex-col gap-1 p-4">
				{#each navItems as item}
					<a
						href={item.href}
						class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
						class:bg-accent={$page.url.pathname.startsWith(item.href)}
					>
						<item.icon class="h-4 w-4" />
						{item.label}
					</a>
				{/each}
			</nav>
			<div class="border-t p-4">
				<button
					onclick={handleLogout}
					class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
				>
					<LogOut class="h-4 w-4" />
					Cerrar sesión
				</button>
			</div>
		</aside>

		{#if sidebarOpen}
			<!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
			<div class="fixed inset-0 z-40 bg-black/50 lg:hidden" role="presentation" onclick={() => sidebarOpen = false}></div>
		{/if}

		<div class="flex flex-1 flex-col lg:pl-64">
			<header class="flex h-14 items-center gap-4 border-b bg-card px-6">
				<button class="lg:hidden" onclick={() => sidebarOpen = true}>
					<Menu class="h-5 w-5" />
				</button>
				<div class="flex-1"></div>
			</header>
			<main class="flex-1 overflow-auto p-6">
				{@render children()}
			</main>
		</div>
	</div>
{:else}
	{@render children()}
{/if}
