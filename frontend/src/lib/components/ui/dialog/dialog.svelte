<script lang="ts">
	let { open = $bindable(false), children }: {
		open?: boolean;
		children?: import('svelte').Snippet;
	} = $props();
</script>

{#key open}
	{@render children?.()}
{/key}
