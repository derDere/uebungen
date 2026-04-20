<script lang="ts">
	interface Props {
		content: string;
	}

	let { content }: Props = $props();
</script>

<div class="data-reader">
	<h2>Data Reader</h2>
	<div class="content-box">
		{#if content}
			<pre>{content}</pre>
		{:else}
			<p class="empty">No data available.</p>
		{/if}
	</div>
</div>

<style>
	.data-reader {
		border: 2px solid #4a90d9;
		border-radius: 8px;
		padding: 1.5rem;
		background: #f0f7ff;
		max-width: 600px;
	}

	h2 {
		margin: 0 0 1rem 0;
		color: #2c5282;
	}

	.content-box {
		background: white;
		border: 1px solid #bee3f8;
		border-radius: 4px;
		padding: 1rem;
	}

	pre {
		margin: 0;
		white-space: pre-wrap;
		word-break: break-word;
		font-family: 'Fira Code', 'Consolas', monospace;
	}

	.empty {
		color: #a0aec0;
		font-style: italic;
		margin: 0;
	}
</style>
