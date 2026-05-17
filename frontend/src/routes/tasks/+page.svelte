<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Root as Table, Header, Body, Row, Head, Cell } from '$lib/components/ui/table';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Root as Dialog, Close, Overlay, Content, Header as DialogHeader, Title, Description, Footer } from '$lib/components/ui/dialog';
	import { Plus, Pencil, Trash2, X } from '@lucide/svelte';

	interface Task {
		id: number;
		title: string;
		description?: string;
		due_date: string;
		subject?: string;
		course?: number;
		course_name?: string;
	}

	let tasks = $state<Task[]>([]);
	let loading = $state(true);
	let showDialog = $state(false);
	let editing = $state<Task | null>(null);

	let form = $state({ title: '', description: '', due_date: '', subject: '', course: '' });

	function resetForm() {
		form = { title: '', description: '', due_date: '', subject: '', course: '' };
		editing = null;
	}

	function openCreate() {
		resetForm();
		showDialog = true;
	}

	function openEdit(task: Task) {
		editing = task;
		form = {
			title: task.title,
			description: task.description ?? '',
			due_date: task.due_date.slice(0, 10),
			subject: task.subject ?? '',
			course: task.course?.toString() ?? '',
		};
		showDialog = true;
	}

	async function load() {
		try {
			const res = await api.get<{ results: Task[] }>('/tasks/');
			tasks = res.results ?? [];
		} catch {
			tasks = [];
		} finally {
			loading = false;
		}
	}

	async function save() {
		const body: Record<string, unknown> = {
			title: form.title,
			description: form.description || undefined,
			due_date: form.due_date,
			subject: form.subject || undefined,
			course: form.course ? Number(form.course) : undefined,
		};
		try {
			if (editing) {
				await api.patch(`/tasks/${editing.id}/`, body);
			} else {
				await api.post('/tasks/', body);
			}
			showDialog = false;
			resetForm();
			await load();
		} catch {
			alert('Error al guardar');
		}
	}

	async function remove(id: number) {
		if (!confirm('¿Eliminar tarea?')) return;
		try {
			await api.delete(`/tasks/${id}/`);
			await load();
		} catch {
			alert('Error al eliminar');
		}
	}

	function formatDate(dateStr: string) {
		return new Date(dateStr).toLocaleDateString('es-AR');
	}

	onMount(load);
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold">Tareas</h1>
			<p class="text-sm text-muted-foreground">Gestioná las tareas escolares</p>
		</div>
		<Button onclick={openCreate}>
			<Plus class="mr-2 h-4 w-4" />
			Nueva tarea
		</Button>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Todas las tareas</CardTitle>
		</CardHeader>
		<CardContent>
			{#if loading}
				<p class="text-sm text-muted-foreground">Cargando…</p>
			{:else if tasks.length === 0}
				<p class="text-sm text-muted-foreground">No hay tareas</p>
			{:else}
				<Table>
					<Header>
						<Row>
							<Head>Título</Head>
							<Head>Materia</Head>
							<Head>Fecha límite</Head>
							<Head>Curso</Head>
							<Head class="w-24">Acciones</Head>
						</Row>
					</Header>
					<Body>
						{#each tasks as task}
							<Row>
								<Cell class="font-medium">{task.title}</Cell>
								<Cell>{task.subject ?? '-'}</Cell>
								<Cell>{formatDate(task.due_date)}</Cell>
								<Cell>{task.course_name ?? '-'}</Cell>
								<Cell>
									<div class="flex gap-2">
										<Button variant="ghost" size="icon" onclick={() => openEdit(task)}>
											<Pencil class="h-4 w-4" />
										</Button>
										<Button variant="ghost" size="icon" onclick={() => remove(task.id)}>
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
			<Title>{editing ? 'Editar tarea' : 'Nueva tarea'}</Title>
			<Description>Completá los datos de la tarea</Description>
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
					<label class="text-sm font-medium" for="subject">Materia</label>
					<Input id="subject" bind:value={form.subject} />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="due_date">Fecha límite</label>
					<Input id="due_date" type="date" bind:value={form.due_date} required />
				</div>
			</div>
			<Footer>
				<Button variant="outline" onclick={() => { showDialog = false; resetForm(); }} type="button">Cancelar</Button>
				<Button type="submit">{editing ? 'Guardar cambios' : 'Crear tarea'}</Button>
			</Footer>
		</form>
	</Content>
{/if}
