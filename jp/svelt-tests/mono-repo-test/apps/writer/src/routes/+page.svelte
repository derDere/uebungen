<script lang="ts">
	import { DataReader } from '@repo/data-read';
	import { DataWriter } from '@repo/data-write';
	import type { PageData } from './$types';

	let { data, form }: { data: PageData; form: { success: boolean } | null } = $props();
</script>

<div class="page">
	<header>
		<h1>Writer App</h1>
		<a href="http://localhost:5170">Back to Portal</a>
	</header>

	{#if form?.success}
		<div class="success-banner">Data saved successfully!</div>
	{/if}

	<div class="panels">
		<DataWriter currentContent={data.content} />
		<DataReader content={data.content} />
	</div>

	<footer>
		<p>
			This app uses <code>@repo/data-write</code> to write and <code>@repo/data-read</code> to preview
			<code>data/data.txt</code>
		</p>
	</footer>
</div>

<style>
	.page {
		max-width: 900px;
		margin: 2rem auto;
		padding: 0 1rem;
		font-family: system-ui, -apple-system, sans-serif;
	}

	header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	h1 {
		color: #276749;
		margin: 0;
	}

	header a {
		color: #48bb78;
		text-decoration: none;
		font-size: 0.9rem;
	}

	header a:hover {
		text-decoration: underline;
	}

	.success-banner {
		background: #c6f6d5;
		color: #276749;
		padding: 0.75rem 1rem;
		border-radius: 6px;
		margin-bottom: 1.5rem;
		font-weight: 500;
	}

	.panels {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		align-items: start;
	}

	footer {
		margin-top: 2rem;
		padding-top: 1rem;
		border-top: 1px solid #e2e8f0;
		color: #a0aec0;
		font-size: 0.85rem;
	}

	code {
		background: #edf2f7;
		padding: 0.1rem 0.3rem;
		border-radius: 3px;
		font-size: 0.85rem;
	}

	@media (max-width: 768px) {
		.panels {
			grid-template-columns: 1fr;
		}
	}
</style>
