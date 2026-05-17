<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
	} & Record<string, unknown> = $props();
</script>

<div class={cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)} {...rest}>
	{@render children?.()}
</div>
