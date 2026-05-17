<script lang="ts">
	import { cn } from '$lib/utils.js';
	import { X } from '@lucide/svelte';

	let { class: className, onclick, ...rest }: {
		class?: string;
		onclick?: (e: MouseEvent) => void;
	} & Record<string, unknown> = $props();
</script>

<button class={cn('absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none', className)} {onclick} {...rest}>
	<X class="h-4 w-4" />
</button>
