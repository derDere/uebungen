<script lang="ts">
  import ToolList from './lib/components/ToolList.svelte';
  import ChecklistView from './lib/components/ChecklistView.svelte';
  import TemplateEditor from './lib/components/TemplateEditor.svelte';
  import SearchFilter from './lib/components/SearchFilter.svelte';
  import ExportPanel from './lib/components/ExportPanel.svelte';

  let selectedToolId: number | null = null;
  let showTemplates = false;

  function handleToolSelect(toolId: number) {
    selectedToolId = toolId;
    showTemplates = false;
  }

  function toggleTemplates() {
    showTemplates = !showTemplates;
    if (showTemplates) {
      selectedToolId = null;
    }
  }
</script>

<main>
  <header>
    <h1>Tool Helper</h1>
    <div class="header-actions">
      <SearchFilter />
      <ExportPanel />
    </div>
  </header>

  <div class="container">
    <aside class="sidebar">
      <ToolList
        {selectedToolId}
        onToolSelect={handleToolSelect}
      />

      <div class="template-toggle">
        <button on:click={toggleTemplates} class:active={showTemplates}>
          {showTemplates ? 'Hide' : 'Show'} Templates
        </button>
      </div>
    </aside>

    <section class="main-content">
      {#if showTemplates}
        <TemplateEditor />
      {:else if selectedToolId !== null}
        <ChecklistView toolId={selectedToolId} />
      {:else}
        <div class="welcome">
          <h2>Welcome to Tool Helper</h2>
          <p>Select a tool from the sidebar to view and manage checklists.</p>
          <p>Or click "Show Templates" to create and edit templates.</p>
        </div>
      {/if}
    </section>
  </div>
</main>

<style>
  main {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    background: #1976D2;
    color: white;
    padding: 1rem 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h1 {
    margin: 0 0 1rem 0;
    font-size: 1.75rem;
  }

  .header-actions {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  .header-actions :global(.search-filter) {
    flex: 1;
    max-width: 500px;
  }

  .container {
    flex: 1;
    display: flex;
    overflow: hidden;
  }

  .sidebar {
    width: 300px;
    background: #f5f5f5;
    border-right: 1px solid #ddd;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }

  .template-toggle {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #ddd;
  }

  .template-toggle button {
    width: 100%;
    padding: 0.75rem;
    background: white;
    color: #1976D2;
    border: 2px solid #1976D2;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }

  .template-toggle button:hover {
    background: #f0f7ff;
  }

  .template-toggle button.active {
    background: #1976D2;
    color: white;
  }

  .main-content {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
    background: white;
  }

  .welcome {
    text-align: center;
    padding: 4rem 2rem;
    color: #666;
  }

  .welcome h2 {
    color: #333;
    margin-bottom: 1rem;
  }

  .welcome p {
    margin: 0.5rem 0;
  }
</style>
