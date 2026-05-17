<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<td class={cn('p-2 align-middle [&:has([role=checkbox])]:pr-0', className)} {...rest}>
	{@render children?.()}
</td>
