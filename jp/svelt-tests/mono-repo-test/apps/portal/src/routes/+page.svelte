<script lang="ts">
</script>

<div class="portal">
	<h1>Monorepo Demo Portal</h1>
	<p>Welcome to the SvelteKit Monorepo Demo. Choose an app:</p>

	<div class="apps">
		<a href="http://localhost:5171" class="app-card reader">
			<h2>Reader App</h2>
			<p>Reads data from the shared data file using <code>@repo/data-read</code></p>
			<span class="port">Port 5171</span>
		</a>

		<a href="http://localhost:5172" class="app-card writer">
			<h2>Writer App</h2>
			<p>Writes data to the shared data file using <code>@repo/data-write</code></p>
			<span class="port">Port 5172</span>
		</a>
	</div>
</div>

<style>
	.portal {
		max-width: 800px;
		margin: 2rem auto;
		padding: 0 1rem;
		font-family: system-ui, -apple-system, sans-serif;
	}

	h1 {
		text-align: center;
		color: #1a202c;
		font-size: 2rem;
		margin-bottom: 0.5rem;
	}

	p {
		text-align: center;
		color: #718096;
		margin-bottom: 2rem;
	}

	.apps {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
	}

	.app-card {
		display: block;
		padding: 2rem;
		border-radius: 12px;
		text-decoration: none;
		color: inherit;
		transition: transform 0.2s, box-shadow 0.2s;
	}

	.app-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
	}

	.app-card.reader {
		background: #f0f7ff;
		border: 2px solid #4a90d9;
	}

	.app-card.writer {
		background: #f0fff4;
		border: 2px solid #48bb78;
	}

	.app-card h2 {
		margin: 0 0 0.5rem 0;
	}

	.app-card.reader h2 {
		color: #2c5282;
	}

	.app-card.writer h2 {
		color: #276749;
	}

	.app-card p {
		text-align: left;
		color: #4a5568;
		margin: 0 0 1rem 0;
		font-size: 0.9rem;
	}

	.app-card code {
		background: rgba(0, 0, 0, 0.06);
		padding: 0.15rem 0.4rem;
		border-radius: 3px;
		font-size: 0.85rem;
	}

	.port {
		display: inline-block;
		background: rgba(0, 0, 0, 0.08);
		padding: 0.2rem 0.6rem;
		border-radius: 4px;
		font-size: 0.8rem;
		font-family: monospace;
	}
</style>
