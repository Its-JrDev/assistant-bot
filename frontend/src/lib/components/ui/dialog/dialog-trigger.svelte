<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, children, onclick, ...rest }: {
		class?: string;
		children?: import('svelte').Snippet;
		onclick?: (e: MouseEvent) => void;
	} & Record<string, unknown> = $props();
</script>

<button class={cn('', className)} {onclick} {...rest}>
	{@render children?.()}
</button>
