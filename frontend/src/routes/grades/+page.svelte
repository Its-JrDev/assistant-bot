<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Root as Table, Header, Body, Row, Head, Cell } from '$lib/components/ui/table';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Root as Dialog, Close, Overlay, Content, Header as DialogHeader, Title, Description, Footer } from '$lib/components/ui/dialog';
	import { Plus, Pencil, Trash2, X } from '@lucide/svelte';

	interface Grade {
		id: number;
		student?: number;
		student_name?: string;
		subject?: string;
		grade: number;
		period?: string;
		date?: string;
	}

	let grades = $state<Grade[]>([]);
	let loading = $state(true);
	let showDialog = $state(false);
	let editing = $state<Grade | null>(null);

	let form = $state({ student: '', subject: '', grade: '', period: '', date: '' });

	function resetForm() {
		form = { student: '', subject: '', grade: '', period: '', date: '' };
		editing = null;
	}

	function openCreate() {
		resetForm();
		showDialog = true;
	}

	function openEdit(grade: Grade) {
		editing = grade;
		form = {
			student: grade.student?.toString() ?? '',
			subject: grade.subject ?? '',
			grade: grade.grade.toString(),
			period: grade.period ?? '',
			date: grade.date ? grade.date.slice(0, 10) : '',
		};
		showDialog = true;
	}

	async function load() {
		try {
			const res = await api.get<{ results: Grade[] }>('/grades/');
			grades = res.results ?? [];
		} catch {
			grades = [];
		} finally {
			loading = false;
		}
	}

	async function save() {
		const body: Record<string, unknown> = {
			student: form.student ? Number(form.student) : undefined,
			subject: form.subject || undefined,
			grade: form.grade ? Number(form.grade) : undefined,
			period: form.period || undefined,
			date: form.date || undefined,
		};
		try {
			if (editing) {
				await api.patch(`/grades/${editing.id}/`, body);
			} else {
				await api.post('/grades/', body);
			}
			showDialog = false;
			resetForm();
			await load();
		} catch {
			alert('Error al guardar');
		}
	}

	async function remove(id: number) {
		if (!confirm('¿Eliminar nota?')) return;
		try {
			await api.delete(`/grades/${id}/`);
			await load();
		} catch {
			alert('Error al eliminar');
		}
	}

	function formatDate(dateStr?: string) {
		if (!dateStr) return '-';
		return new Date(dateStr).toLocaleDateString('es-AR');
	}

	onMount(load);
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold">Notas</h1>
			<p class="text-sm text-muted-foreground">Gestioná las notas de los estudiantes</p>
		</div>
		<Button onclick={openCreate}>
			<Plus class="mr-2 h-4 w-4" />
			Nueva nota
		</Button>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Todas las notas</CardTitle>
		</CardHeader>
		<CardContent>
			{#if loading}
				<p class="text-sm text-muted-foreground">Cargando…</p>
			{:else if grades.length === 0}
				<p class="text-sm text-muted-foreground">No hay notas</p>
			{:else}
				<Table>
					<Header>
						<Row>
							<Head>Estudiante</Head>
							<Head>Materia</Head>
							<Head>Nota</Head>
							<Head>Período</Head>
							<Head>Fecha</Head>
							<Head class="w-24">Acciones</Head>
						</Row>
					</Header>
					<Body>
						{#each grades as grade}
							<Row>
								<Cell class="font-medium">{grade.student_name ?? '-'}</Cell>
								<Cell>{grade.subject ?? '-'}</Cell>
								<Cell>{grade.grade}</Cell>
								<Cell>{grade.period ?? '-'}</Cell>
								<Cell>{formatDate(grade.date)}</Cell>
								<Cell>
									<div class="flex gap-2">
										<Button variant="ghost" size="icon" onclick={() => openEdit(grade)}>
											<Pencil class="h-4 w-4" />
										</Button>
										<Button variant="ghost" size="icon" onclick={() => remove(grade.id)}>
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
			<Title>{editing ? 'Editar nota' : 'Nueva nota'}</Title>
			<Description>Completá los datos de la nota</Description>
		</DialogHeader>
		<form onsubmit={(e) => { e.preventDefault(); save(); }} class="space-y-4">
			<div class="grid grid-cols-2 gap-4">
				<div class="space-y-2">
					<label class="text-sm font-medium" for="student">ID Estudiante</label>
					<Input id="student" type="number" bind:value={form.student} />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="subject">Materia</label>
					<Input id="subject" bind:value={form.subject} />
				</div>
			</div>
			<div class="grid grid-cols-2 gap-4">
				<div class="space-y-2">
					<label class="text-sm font-medium" for="grade">Nota</label>
					<Input id="grade" type="number" min="1" max="10" step="0.5" bind:value={form.grade} required />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="period">Período</label>
					<Input id="period" bind:value={form.period} placeholder="1er trimestre" />
				</div>
			</div>
			<div class="space-y-2">
				<label class="text-sm font-medium" for="date">Fecha</label>
				<Input id="date" type="date" bind:value={form.date} />
			</div>
			<Footer>
				<Button variant="outline" onclick={() => { showDialog = false; resetForm(); }} type="button">Cancelar</Button>
				<Button type="submit">{editing ? 'Guardar cambios' : 'Crear nota'}</Button>
			</Footer>
		</form>
	</Content>
{/if}
