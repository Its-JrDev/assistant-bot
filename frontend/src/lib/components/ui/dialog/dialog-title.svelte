<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<h2 class={cn('text-lg font-semibold leading-none tracking-tight', className)} {...rest}>
	{@render children?.()}
</h2>
