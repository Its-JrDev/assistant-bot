<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<div class={cn('rounded-xl border bg-card text-card-foreground shadow', className)} {...rest}>
	{@render children?.()}
</div>
