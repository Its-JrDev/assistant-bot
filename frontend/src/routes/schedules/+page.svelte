<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Root as Table, Header, Body, Row, Head, Cell } from '$lib/components/ui/table';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Root as Dialog, Close, Overlay, Content, Header as DialogHeader, Title, Description, Footer } from '$lib/components/ui/dialog';
	import { Plus, Pencil, Trash2, X } from '@lucide/svelte';

	interface Schedule {
		id: number;
		day: string;
		start_time: string;
		end_time: string;
		subject?: string;
		course?: number;
		course_name?: string;
	}

	const DAYS = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES'];

	let schedules = $state<Schedule[]>([]);
	let loading = $state(true);
	let showDialog = $state(false);
	let editing = $state<Schedule | null>(null);

	let form = $state({ day: 'LUNES', start_time: '', end_time: '', subject: '', course: '' });

	function resetForm() {
		form = { day: 'LUNES', start_time: '', end_time: '', subject: '', course: '' };
		editing = null;
	}

	function openCreate() {
		resetForm();
		showDialog = true;
	}

	function openEdit(schedule: Schedule) {
		editing = schedule;
		form = {
			day: schedule.day,
			start_time: schedule.start_time,
			end_time: schedule.end_time,
			subject: schedule.subject ?? '',
			course: schedule.course?.toString() ?? '',
		};
		showDialog = true;
	}

	async function load() {
		try {
			const res = await api.get<{ results: Schedule[] }>('/schedules/');
			schedules = res.results ?? [];
		} catch {
			schedules = [];
		} finally {
			loading = false;
		}
	}

	async function save() {
		const body: Record<string, unknown> = {
			day: form.day,
			start_time: form.start_time,
			end_time: form.end_time,
			subject: form.subject || undefined,
			course: form.course ? Number(form.course) : undefined,
		};
		try {
			if (editing) {
				await api.patch(`/schedules/${editing.id}/`, body);
			} else {
				await api.post('/schedules/', body);
			}
			showDialog = false;
			resetForm();
			await load();
		} catch {
			alert('Error al guardar');
		}
	}

	async function remove(id: number) {
		if (!confirm('¿Eliminar horario?')) return;
		try {
			await api.delete(`/schedules/${id}/`);
			await load();
		} catch {
			alert('Error al eliminar');
		}
	}

	const dayLabels: Record<string, string> = {
		LUNES: 'Lunes', MARTES: 'Martes', MIERCOLES: 'Miércoles',
		JUEVES: 'Jueves', VIERNES: 'Viernes',
	};

	const sortedSchedules = $derived(
		[...schedules].sort((a, b) => {
			const dayDiff = DAYS.indexOf(a.day) - DAYS.indexOf(b.day);
			if (dayDiff !== 0) return dayDiff;
			return a.start_time.localeCompare(b.start_time);
		})
	);

	onMount(load);
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold">Horarios</h1>
			<p class="text-sm text-muted-foreground">Gestioná los horarios por curso</p>
		</div>
		<Button onclick={openCreate}>
			<Plus class="mr-2 h-4 w-4" />
			Nuevo horario
		</Button>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Todos los horarios</CardTitle>
		</CardHeader>
		<CardContent>
			{#if loading}
				<p class="text-sm text-muted-foreground">Cargando…</p>
			{:else if sortedSchedules.length === 0}
				<p class="text-sm text-muted-foreground">No hay horarios</p>
			{:else}
				<Table>
					<Header>
						<Row>
							<Head>Día</Head>
							<Head>Inicio</Head>
							<Head>Fin</Head>
							<Head>Materia</Head>
							<Head>Curso</Head>
							<Head class="w-24">Acciones</Head>
						</Row>
					</Header>
					<Body>
						{#each sortedSchedules as schedule}
							<Row>
								<Cell class="font-medium">{dayLabels[schedule.day] ?? schedule.day}</Cell>
								<Cell>{schedule.start_time}</Cell>
								<Cell>{schedule.end_time}</Cell>
								<Cell>{schedule.subject ?? '-'}</Cell>
								<Cell>{schedule.course_name ?? '-'}</Cell>
								<Cell>
									<div class="flex gap-2">
										<Button variant="ghost" size="icon" onclick={() => openEdit(schedule)}>
											<Pencil class="h-4 w-4" />
										</Button>
										<Button variant="ghost" size="icon" onclick={() => remove(schedule.id)}>
											<Trash2 class="h-4 w-4" />
										</Button>
									</div>
								</Cell>
							</Row>
						{/each}
					</Body>
				</Table>
			{/if}
		</CardContent>
	</Card>
</div>

{#if showDialog}
	<Overlay />
	<Content>
		<Close onclick={() => { showDialog = false; resetForm(); }}>
			<X class="h-4 w-4" />
		</Close>
		<DialogHeader>
			<Title>{editing ? 'Editar horario' : 'Nuevo horario'}</Title>
			<Description>Completá los datos del horario</Description>
		</DialogHeader>
		<form onsubmit={(e) => { e.preventDefault(); save(); }} class="space-y-4">
			<div class="space-y-2">
				<label class="text-sm font-medium" for="day">Día</label>
				<select id="day" bind:value={form.day} class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm">
					{#each DAYS as d}
						<option value={d}>{dayLabels[d]}</option>
					{/each}
				</select>
			</div>
			<div class="grid grid-cols-2 gap-4">
				<div class="space-y-2">
					<label class="text-sm font-medium" for="start">Inicio</label>
					<Input id="start" type="time" bind:value={form.start_time} required />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="end">Fin</label>
					<Input id="end" type="time" bind:value={form.end_time} required />
				</div>
			</div>
			<div class="space-y-2">
				<label class="text-sm font-medium" for="subject">Materia</label>
				<Input id="subject" bind:value={form.subject} />
			</div>
			<Footer>
				<Button variant="outline" onclick={() => { showDialog = false; resetForm(); }} type="button">Cancelar</Button>
				<Button type="submit">{editing ? 'Guardar cambios' : 'Crear horario'}</Button>
			</Footer>
		</form>
	</Content>
{/if}
