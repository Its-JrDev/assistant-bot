<script lang="ts">
	import { cn } from '$lib/utils.js';

	let { class: className, ...rest }: {
		class?: string;
	} & Record<string, unknown> = $props();
</script>

<div class={cn('fixed inset-0 z-50 bg-black/80', className)} role="presentation" {...rest}></div>
