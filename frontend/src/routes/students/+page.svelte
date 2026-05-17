<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Root as Table, Header, Body, Row, Head, Cell } from '$lib/components/ui/table';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Root as Dialog, Close, Overlay, Content, Header as DialogHeader, Title, Description, Footer } from '$lib/components/ui/dialog';
	import { Plus, Pencil, Trash2, X, Search } from '@lucide/svelte';

	interface Student {
		id: number;
		dni: string;
		full_name: string;
		email?: string;
		course?: number;
		course_name?: string;
		telegram_id?: string;
	}

	let students = $state<Student[]>([]);
	let loading = $state(true);
	let showDialog = $state(false);
	let editing = $state<Student | null>(null);
	let searchQuery = $state('');

	let form = $state({ dni: '', full_name: '', email: '', course: '', pin: '' });

	function resetForm() {
		form = { dni: '', full_name: '', email: '', course: '', pin: '' };
		editing = null;
	}

	function openCreate() {
		resetForm();
		showDialog = true;
	}

	function openEdit(student: Student) {
		editing = student;
		form = {
			dni: student.dni,
			full_name: student.full_name,
			email: student.email ?? '',
			course: student.course?.toString() ?? '',
			pin: '',
		};
		showDialog = true;
	}

	async function load() {
		try {
			const params: Record<string, string> = {};
			if (searchQuery) params.search = searchQuery;
			const res = await api.get<{ results: Student[] }>('/students/', { params });
			students = res.results ?? [];
		} catch {
			students = [];
		} finally {
			loading = false;
		}
	}

	async function save() {
		const body: Record<string, unknown> = {
			dni: form.dni,
			full_name: form.full_name,
			email: form.email || undefined,
			course: form.course ? Number(form.course) : undefined,
		};
		if (form.pin) body.pin = form.pin;
		try {
			if (editing) {
				await api.patch(`/students/${editing.id}/`, body);
			} else {
				await api.post('/students/', body);
			}
			showDialog = false;
			resetForm();
			await load();
		} catch {
			alert('Error al guardar');
		}
	}

	async function remove(id: number) {
		if (!confirm('¿Eliminar estudiante?')) return;
		try {
			await api.delete(`/students/${id}/`);
			await load();
		} catch {
			alert('Error al eliminar');
		}
	}

	function handleSearch() {
		loading = true;
		load();
	}

	onMount(load);
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold">Estudiantes</h1>
			<p class="text-sm text-muted-foreground">Gestioná los estudiantes</p>
		</div>
		<Button onclick={openCreate}>
			<Plus class="mr-2 h-4 w-4" />
			Nuevo estudiante
		</Button>
	</div>

	<div class="flex items-center gap-2">
		<div class="relative flex-1 max-w-sm">
			<Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
			<Input
				class="pl-9"
				placeholder="Buscar por nombre o DNI…"
				bind:value={searchQuery}
				onkeydown={(e: KeyboardEvent) => { if (e.key === 'Enter') handleSearch(); }}
			/>
		</div>
		<Button variant="secondary" onclick={handleSearch}>Buscar</Button>
	</div>

	<Card>
		<CardHeader>
			<CardTitle>Todos los estudiantes</CardTitle>
		</CardHeader>
		<CardContent>
			{#if loading}
				<p class="text-sm text-muted-foreground">Cargando…</p>
			{:else if students.length === 0}
				<p class="text-sm text-muted-foreground">No hay estudiantes</p>
			{:else}
				<Table>
					<Header>
						<Row>
							<Head>Nombre</Head>
							<Head>DNI</Head>
							<Head>Email</Head>
							<Head>Curso</Head>
							<Head>Telegram ID</Head>
							<Head class="w-24">Acciones</Head>
						</Row>
					</Header>
					<Body>
						{#each students as student}
							<Row>
								<Cell class="font-medium">{student.full_name}</Cell>
								<Cell>{student.dni}</Cell>
								<Cell>{student.email ?? '-'}</Cell>
								<Cell>{student.course_name ?? '-'}</Cell>
								<Cell>{student.telegram_id ?? '-'}</Cell>
								<Cell>
									<div class="flex gap-2">
										<Button variant="ghost" size="icon" onclick={() => openEdit(student)}>
											<Pencil class="h-4 w-4" />
										</Button>
										<Button variant="ghost" size="icon" onclick={() => remove(student.id)}>
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
			<Title>{editing ? 'Editar estudiante' : 'Nuevo estudiante'}</Title>
			<Description>Completá los datos del estudiante</Description>
		</DialogHeader>
		<form onsubmit={(e) => { e.preventDefault(); save(); }} class="space-y-4">
			<div class="grid grid-cols-2 gap-4">
				<div class="space-y-2">
					<label class="text-sm font-medium" for="fn">Nombre completo</label>
					<Input id="fn" bind:value={form.full_name} required />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="dni">DNI</label>
					<Input id="dni" bind:value={form.dni} required />
				</div>
			</div>
			<div class="grid grid-cols-2 gap-4">
				<div class="space-y-2">
					<label class="text-sm font-medium" for="email">Email</label>
					<Input id="email" type="email" bind:value={form.email} />
				</div>
				<div class="space-y-2">
					<label class="text-sm font-medium" for="course">ID Curso</label>
					<Input id="course" type="number" bind:value={form.course} />
				</div>
			</div>
			<div class="space-y-2">
				<label class="text-sm font-medium" for="pin">PIN</label>
				<Input id="pin" type="password" bind:value={form.pin} placeholder={editing ? 'Dejar vacío para no cambiar' : 'PIN del estudiante'} />
			</div>
			<Footer>
				<Button variant="outline" onclick={() => { showDialog = false; resetForm(); }} type="button">Cancelar</Button>
				<Button type="submit">{editing ? 'Guardar cambios' : 'Crear estudiante'}</Button>
			</Footer>
		</form>
	</Content>
{/if}
