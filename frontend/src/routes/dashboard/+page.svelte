<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Calendar, BookOpen, Clock, GraduationCap } from '@lucide/svelte';

	let stats = $state({
		events: 0,
		tasks: 0,
		courses: 0,
		students: 0,
	});
	let upcomingEvents = $state<Array<{ id: number; title: string; date: string; course_name?: string }>>([]);

	onMount(async () => {
		try {
			const [eventsRes, tasksRes, coursesRes, studentsRes] = await Promise.all([
				api.get<{ count: number }>('/events/'),
				api.get<{ count: number }>('/tasks/'),
				api.get<{ count: number }>('/courses/'),
				api.get<{ count: number }>('/students/'),
			]);
			stats = {
				events: eventsRes.count,
				tasks: tasksRes.count,
				courses: coursesRes.count,
				students: studentsRes.count,
			};

			const events = await api.get<{ results: Array<{ id: number; title: string; date: string; course_name?: string }> }>('/events/', { params: { page_size: '5' } });
			upcomingEvents = (events.results ?? []).sort(
				(a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
			).slice(0, 5);
		} catch {
			// ignore
		}
	});

	function formatDate(dateStr: string) {
		return new Date(dateStr).toLocaleDateString('es-AR', {
			day: 'numeric', month: 'long', year: 'numeric',
		});
	}
</script>

<div class="space-y-6">
	<div>
		<h1 class="text-2xl font-bold">Dashboard</h1>
		<p class="text-sm text-muted-foreground">Resumen del panel escolar</p>
	</div>

	<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
		<Card>
			<CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
				<CardTitle class="text-sm font-medium">Eventos</CardTitle>
				<Calendar class="h-4 w-4 text-muted-foreground" />
			</CardHeader>
			<CardContent>
				<div class="text-2xl font-bold">{stats.events}</div>
			</CardContent>
		</Card>
		<Card>
			<CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
				<CardTitle class="text-sm font-medium">Tareas</CardTitle>
				<BookOpen class="h-4 w-4 text-muted-foreground" />
			</CardHeader>
			<CardContent>
				<div class="text-2xl font-bold">{stats.tasks}</div>
			</CardContent>
		</Card>
		<Card>
			<CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
				<CardTitle class="text-sm font-medium">Cursos</CardTitle>
				<GraduationCap class="h-4 w-4 text-muted-foreground" />
			</CardHeader>
			<CardContent>
				<div class="text-2xl font-bold">{stats.courses}</div>
			</CardContent>
		</Card>
		<Card>
			<CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
				<CardTitle class="text-sm font-medium">Estudiantes</CardTitle>
				<Clock class="h-4 w-4 text-muted-foreground" />
			</CardHeader>
			<CardContent>
				<div class="text-2xl font-bold">{stats.students}</div>
			</CardContent>
		</Card>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Próximos Eventos</CardTitle>
		</CardHeader>
		<CardContent>
			{#if upcomingEvents.length === 0}
				<p class="text-sm text-muted-foreground">No hay eventos próximos</p>
			{:else}
				<ul class="space-y-3">
					{#each upcomingEvents as event}
						<li class="flex items-center justify-between border-b pb-2 last:border-0">
							<div>
								<p class="text-sm font-medium">{event.title}</p>
								{#if event.course_name}
									<p class="text-xs text-muted-foreground">{event.course_name}</p>
								{/if}
							</div>
							<span class="text-xs text-muted-foreground">{formatDate(event.date)}</span>
						</li>
					{/each}
				</ul>
			{/if}
		</CardContent>
	</Card>
</div>
