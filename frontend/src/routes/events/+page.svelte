<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Root as Table, Header, Body, Row, Head, Cell } from '$lib/components/ui/table';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Root as Dialog, Trigger, Close, Portal, Overlay, Content, Header as DialogHeader, Title, Description, Footer } from '$lib/components/ui/dialog';
	import { Plus, Pencil, Trash2, X } from '@lucide/svelte';

	interface Event {
		id: number;
		title: string;
		description?: string;
		date: string;
		time?: string;
		location?: string;
		course?: number;
		course_name?: string;
	}

	let events = $state<Event[]>([]);
	let loading = $state(true);
	let showDialog = $state(false);
	let editing = $state<Event | null>(null);

	let form = $state({ title: '', description: '', date: '', time: '', location: '', course: '' });

	function resetForm() {
		form = { title: '', description: '', date: '', time: '', location: '', course: '' };
		editing = null;
	}

	function openCreate() {
		resetForm();
		showDialog = true;
	}

	function openEdit(event: Event) {
		editing = event;
		form = {
			title: event.title,
			description: event.description ?? '',
			date: event.date.slice(0, 10),
			time: event.time ?? '',
			location: event.location ?? '',
			course: event.course?.toString() ?? '',
		};
		showDialog = true;
	}

	async function loadEvents() {
		try {
			const res = await api.get<{ results: Event[] }>('/events/');
			events = res.results ?? [];
		} catch {
			events = [];
		} finally {
			loading = false;
		}
	}

	async function save() {
		const body: Record<string, unknown> = {
			title: form.title,
			description: form.description || undefined,
			date: form.date,
			time: form.time || undefined,
			location: form.location || undefined,
			course: form.course ? Number(form.course) : undefined,
		};

		try {
			if (editing) {
				await api.patch(`/events/${editing.id}/`, body);
			} else {
				await api.post('/events/', body);
			}
			showDialog = false;
			resetForm();
			await loadEvents();
		} catch (e) {
			alert('Error al guardar');
		}
	}

	async function remove(id: number) {
		if (!confirm('¿Eliminar evento?')) return;
		try {
			await api.delete(`/events/${id}/`);
			await loadEvents();
		} catch {
			alert('Error al eliminar');
		}
	}

	function formatDate(dateStr: string) {
		return new Date(dateStr).toLocaleDateString('es-AR');
	}

	onMount(loadEvents);
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold">Eventos</h1>
			<p class="text-sm text-muted-foreground">Gestioná los eventos escolares</p>
		</div>
		<Button onclick={openCreate}>
			<Plus class="mr-2 h-4 w-4" />
			Nuevo evento
		</Button>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Todos los eventos</CardTitle>
		</CardHeader>
		<CardContent>
			{#if loading}
				<p class="text-sm text-muted-foreground">Cargando…</p>
			{:else if events.length === 0}
				<p class="text-sm text-muted-foreground">No hay eventos</p>
			{:else}
				<Table>
					<Header>
						<Row>
							<Head>Título</Head>
							<Head>Fecha</Head>
							<Head>Curso</Head>
							<Head class="w-24">Acciones</Head>
						</Row>
					</Header>
					<Body>
						{#each events as event}
							<Row>
								<Cell class="font-medium">{event.title}</Cell>
								<Cell>{formatDate(event.date)}</Cell>
								<Cell>{event.course_name ?? '-'}</Cell>
								<Cell>
									<div class="flex gap-2">
										<Button variant="ghost" size="icon" onclick={() => openEdit(event)}>
											<Pencil class="h-4 w-4" />
										</Button>
										<Button variant="ghost" size="icon" onclick={() => remove(event.id)}>
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
			<Title>{editing ? 'Editar evento' : 'Nuevo evento'}</Title>
			<Description>Completá los datos del evento</Description>
		</DialogHeader>
		<form onsubmit={(e) => { e.preventDefault(); save(); }} class="space-y-4">
			<div class="space-y-2">
				<label class="text-sm font-medium" for="title">Título</label>
				<Input id="title" bind:value={form.title} required />
			</div>
			<div class="space-y-2">
				<label class="text-sm font-medium" for="desc">Descripción</label>
				<Input id="desc" bind:value={form.description} />
			</div>
			<div class="grid grid-cols-2 gap-4">
				<div class="space-y-2">
					<label class="text-sm font-medium" for="date">Fecha</label>
					<Input id="date" type="date" bind:value={form.date} required />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="time">Hora</label>
					<Input id="time" type="time" bind:value={form.time} />
				</div>
			</div>
			<div class="space-y-2">
				<label class="text-sm font-medium" for="loc">Ubicación</label>
				<Input id="loc" bind:value={form.location} placeholder="Salón, aula…" />
			</div>
			<Footer>
				<Button variant="outline" onclick={() => { showDialog = false; resetForm(); }} type="button">Cancelar</Button>
				<Button type="submit">{editing ? 'Guardar cambios' : 'Crear evento'}</Button>
			</Footer>
		</form>
	</Content>
{/if}
