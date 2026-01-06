<script lang="ts">
  import { onMount } from 'svelte';
  import { toolsApi } from '../api';
  import type { Tool } from '../types';

  export let selectedToolId: number | null = null;
  export let onToolSelect: (toolId: number) => void;

  let tools: Tool[] = [];
  let newToolName = '';
  let loading = false;
  let error = '';

  async function loadTools() {
    try {
      loading = true;
      tools = await toolsApi.list();
    } catch (e) {
      error = 'Failed to load tools';
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function createTool() {
    if (!newToolName.trim()) return;

    try {
      await toolsApi.create({ name: newToolName, status: 'active' });
      newToolName = '';
      await loadTools();
    } catch (e) {
      error = 'Failed to create tool';
      console.error(e);
    }
  }

  async function deleteTool(id: number) {
    if (!confirm('Delete this tool?')) return;

    try {
      await toolsApi.delete(id);
      if (selectedToolId === id) {
        selectedToolId = null;
      }
      await loadTools();
    } catch (e) {
      error = 'Failed to delete tool';
      console.error(e);
    }
  }

  onMount(loadTools);
</script>

<div class="tool-list">
  <h2>Tools</h2>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <div class="create-tool">
    <input
      type="text"
      bind:value={newToolName}
      placeholder="New tool name..."
      on:keydown={(e) => e.key === 'Enter' && createTool()}
    />
    <button on:click={createTool}>Add Tool</button>
  </div>

  {#if loading}
    <div class="loading">Loading...</div>
  {:else}
    <ul class="tools">
      {#each tools as tool (tool.id)}
        <li
          class:selected={selectedToolId === tool.id}
          on:click={() => onToolSelect(tool.id)}
        >
          <span class="tool-name">{tool.name}</span>
          <button
            class="delete-btn"
            on:click|stopPropagation={() => deleteTool(tool.id)}
          >
            ×
          </button>
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .tool-list {
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  h2 {
    margin: 0 0 1rem 0;
    font-size: 1.25rem;
  }

  .create-tool {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .create-tool input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .create-tool button {
    padding: 0.5rem 1rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .create-tool button:hover {
    background: #45a049;
  }

  .tools {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
    overflow-y: auto;
  }

  .tools li {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: #f5f5f5;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
  }

  .tools li:hover {
    background: #ebebeb;
  }

  .tools li.selected {
    background: #2196F3;
    color: white;
  }

  .tool-name {
    flex: 1;
  }

  .delete-btn {
    background: transparent;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #999;
    padding: 0;
    width: 24px;
    height: 24px;
    line-height: 1;
  }

  .delete-btn:hover {
    color: #f44336;
  }

  .selected .delete-btn {
    color: rgba(255, 255, 255, 0.7);
  }

  .selected .delete-btn:hover {
    color: white;
  }

  .error {
    background: #ffebee;
    color: #c62828;
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 1rem;
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #999;
  }
</style>
