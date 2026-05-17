<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<th class={cn('h-10 px-2 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0', className)} {...rest}>
	{@render children?.()}
</th>
