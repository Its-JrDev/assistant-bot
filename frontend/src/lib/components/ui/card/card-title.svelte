<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<h3 class={cn('font-semibold leading-none tracking-tight', className)} {...rest}>
	{@render children?.()}
</h3>
