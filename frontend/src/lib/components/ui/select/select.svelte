<script lang="ts">
	import { cn } from '$lib/utils.js';
	import { ChevronDown } from '@lucide/svelte';

	let { ref = $bindable(null), class: className, children, ...rest }: {
		ref?: HTMLSelectElement | null;
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<div class="relative">
	<select
		bind:this={ref}
		class={cn(
			'flex h-9 w-full appearance-none rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50',
			className,
		)}
		{...rest}
	>
		{@render children?.()}
	</select>
	<ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 opacity-50 pointer-events-none" />
</div>
