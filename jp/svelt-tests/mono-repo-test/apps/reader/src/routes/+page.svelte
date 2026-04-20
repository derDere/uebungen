<script lang="ts">
	import { DataReader } from '@repo/data-read';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="page">
	<header>
		<h1>Reader App</h1>
		<a href="http://localhost:5170">Back to Portal</a>
	</header>

	<DataReader content={data.content} />

	<footer>
		<p>This app uses <code>@repo/data-read</code> to read from <code>data/data.txt</code></p>
	</footer>
</div>

<style>
	.page {
		max-width: 700px;
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
		color: #2c5282;
		margin: 0;
	}

	header a {
		color: #4a90d9;
		text-decoration: none;
		font-size: 0.9rem;
	}

	header a:hover {
		text-decoration: underline;
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
</style>
