<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<p class={cn('text-sm text-muted-foreground', className)} {...rest}>
	{@render children?.()}
</p>
