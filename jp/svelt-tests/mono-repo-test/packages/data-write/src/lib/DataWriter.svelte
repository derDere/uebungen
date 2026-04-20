<script lang="ts">
	interface Props {
		currentContent?: string;
	}

	let { currentContent = '' }: Props = $props();
</script>

<div class="data-writer">
	<h2>Data Writer</h2>
	<form method="POST" action="?/write">
		<textarea name="content" value={currentContent} rows="6" placeholder="Enter text to save..."></textarea>
		<button type="submit">Save Data</button>
	</form>
</div>

<style>
	.data-writer {
		border: 2px solid #48bb78;
		border-radius: 8px;
		padding: 1.5rem;
		background: #f0fff4;
		max-width: 600px;
	}

	h2 {
		margin: 0 0 1rem 0;
		color: #276749;
	}

	textarea {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #c6f6d5;
		border-radius: 4px;
		font-family: 'Fira Code', 'Consolas', monospace;
		font-size: 0.9rem;
		resize: vertical;
		box-sizing: border-box;
	}

	textarea:focus {
		outline: none;
		border-color: #48bb78;
		box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.2);
	}

	button {
		margin-top: 0.75rem;
		padding: 0.5rem 1.5rem;
		background: #48bb78;
		color: white;
		border: none;
		border-radius: 4px;
		font-size: 1rem;
		cursor: pointer;
		transition: background 0.2s;
	}

	button:hover {
		background: #38a169;
	}
</style>
