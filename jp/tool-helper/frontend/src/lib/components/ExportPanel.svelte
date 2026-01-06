<script lang="ts">
  import { exportApi } from '../api';

  let exporting = false;
  let error = '';

  async function exportData(format: 'json' | 'yaml' | 'csv' | 'markdown') {
    try {
      exporting = true;
      error = '';

      let data: string;
      let filename: string;
      let mimeType: string;

      switch (format) {
        case 'json':
          data = await exportApi.json();
          filename = 'tool-helper-export.json';
          mimeType = 'application/json';
          break;
        case 'yaml':
          data = await exportApi.yaml();
          filename = 'tool-helper-export.yaml';
          mimeType = 'text/yaml';
          break;
        case 'csv':
          data = await exportApi.csv();
          filename = 'tool-helper-export.csv';
          mimeType = 'text/csv';
          break;
        case 'markdown':
          data = await exportApi.markdown();
          filename = 'tool-helper-export.md';
          mimeType = 'text/markdown';
          break;
      }

      const blob = new Blob([data], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      error = `Failed to export as ${format.toUpperCase()}`;
      console.error(e);
    } finally {
      exporting = false;
    }
  }
</script>

<div class="export-panel">
  <h3>Export Data</h3>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <div class="export-buttons">
    <button on:click={() => exportData('json')} disabled={exporting}>
      Export JSON
    </button>
    <button on:click={() => exportData('yaml')} disabled={exporting}>
      Export YAML
    </button>
    <button on:click={() => exportData('csv')} disabled={exporting}>
      Export CSV
    </button>
    <button on:click={() => exportData('markdown')} disabled={exporting}>
      Export Markdown
    </button>
  </div>

  {#if exporting}
    <div class="exporting">Exporting...</div>
  {/if}
</div>

<style>
  .export-panel {
    padding: 1rem;
  }

  h3 {
    margin: 0 0 1rem 0;
    font-size: 1rem;
  }

  .export-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  button {
    padding: 0.6rem 1rem;
    background: #673AB7;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  button:hover {
    background: #5E35B1;
  }

  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .exporting {
    margin-top: 0.75rem;
    color: #666;
    font-size: 0.9rem;
  }

  .error {
    background: #ffebee;
    color: #c62828;
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }
</style>
