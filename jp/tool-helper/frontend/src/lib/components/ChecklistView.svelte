<script lang="ts">
  import { checklistsApi, templatesApi } from '../api';
  import type { CheckList, CheckListTemplate, CheckListPoint } from '../types';

  export let toolId: number;

  let checklists: CheckList[] = [];
  let templates: CheckListTemplate[] = [];
  let newChecklistName = '';
  let selectedTemplateId: number | null = null;
  let newPointName = '';
  let addingPointToChecklistId: number | null = null;
  let loading = false;
  let error = '';

  $: if (toolId) {
    loadData();
  }

  async function loadData() {
    try {
      loading = true;
      [checklists, templates] = await Promise.all([
        checklistsApi.list(toolId),
        templatesApi.checklist.list(),
      ]);
    } catch (e) {
      error = 'Failed to load data';
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function createChecklist() {
    if (!newChecklistName.trim()) return;

    try {
      await checklistsApi.create({
        name: newChecklistName,
        tool_id: toolId,
        status: 'active',
      });
      newChecklistName = '';
      await loadData();
    } catch (e) {
      error = 'Failed to create checklist';
      console.error(e);
    }
  }

  async function createFromTemplate() {
    if (!selectedTemplateId) return;

    try {
      await checklistsApi.createFromTemplate(selectedTemplateId, toolId);
      await loadData();
    } catch (e) {
      error = 'Failed to create checklist from template';
      console.error(e);
    }
  }

  async function deleteChecklist(id: number) {
    if (!confirm('Delete this checklist?')) return;

    try {
      await checklistsApi.delete(id);
      await loadData();
    } catch (e) {
      error = 'Failed to delete checklist';
      console.error(e);
    }
  }

  async function togglePoint(checklistId: number, pointId: number) {
    try {
      await checklistsApi.togglePoint(checklistId, pointId);
      await loadData();
    } catch (e) {
      error = 'Failed to toggle point';
      console.error(e);
    }
  }

  async function addPoint(checklistId: number) {
    if (!newPointName.trim()) return;

    try {
      await checklistsApi.addPoint(checklistId, {
        name: newPointName,
        status: 'active',
        is_checked: false,
      });
      newPointName = '';
      addingPointToChecklistId = null;
      await loadData();
    } catch (e) {
      error = 'Failed to add point';
      console.error(e);
    }
  }

  function getSortedPoints(points: CheckListPoint[]): CheckListPoint[] {
    return [...points].sort((a, b) => a.name.localeCompare(b.name));
  }
</script>

<div class="checklist-view">
  {#if error}
    <div class="error">{error}</div>
  {/if}

  <div class="create-section">
    <h3>Create New Checklist</h3>
    <div class="create-form">
      <input
        type="text"
        bind:value={newChecklistName}
        placeholder="Checklist name..."
        on:keydown={(e) => e.key === 'Enter' && createChecklist()}
      />
      <button on:click={createChecklist}>Create</button>
    </div>

    <div class="template-section">
      <select bind:value={selectedTemplateId}>
        <option value={null}>Select template...</option>
        {#each templates as template (template.id)}
          <option value={template.id}>{template.name}</option>
        {/each}
      </select>
      <button on:click={createFromTemplate} disabled={!selectedTemplateId}>
        Create from Template
      </button>
    </div>
  </div>

  {#if loading}
    <div class="loading">Loading...</div>
  {:else}
    <div class="checklists">
      {#each checklists as checklist (checklist.id)}
        <div class="checklist">
          <div class="checklist-header">
            <h4>{checklist.name}</h4>
            <button
              class="delete-btn"
              on:click={() => deleteChecklist(checklist.id)}
            >
              Delete
            </button>
          </div>

          <ul class="points">
            {#each getSortedPoints(checklist.points) as point (point.id)}
              <li class="point">
                <label>
                  <input
                    type="checkbox"
                    checked={point.is_checked}
                    on:change={() => togglePoint(checklist.id, point.id)}
                  />
                  <span class:checked={point.is_checked}>{point.name}</span>
                </label>
              </li>
            {/each}
          </ul>

          {#if addingPointToChecklistId === checklist.id}
            <div class="add-point">
              <input
                type="text"
                bind:value={newPointName}
                placeholder="New point name..."
                on:keydown={(e) => e.key === 'Enter' && addPoint(checklist.id)}
                autofocus
              />
              <button on:click={() => addPoint(checklist.id)}>Add</button>
              <button on:click={() => (addingPointToChecklistId = null)}>
                Cancel
              </button>
            </div>
          {:else}
            <button
              class="add-point-btn"
              on:click={() => (addingPointToChecklistId = checklist.id)}
            >
              + Add Point
            </button>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .checklist-view {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }

  .create-section {
    background: #f9f9f9;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
  }

  .create-section h3 {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
  }

  .create-form,
  .template-section {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
  }

  .template-section {
    margin-bottom: 0;
  }

  input,
  select {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  button {
    padding: 0.5rem 1rem;
    background: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background: #1976D2;
  }

  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .checklists {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .checklist {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
  }

  .checklist-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #eee;
  }

  .checklist-header h4 {
    margin: 0;
    font-size: 1.1rem;
  }

  .delete-btn {
    background: #f44336;
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }

  .delete-btn:hover {
    background: #d32f2f;
  }

  .points {
    list-style: none;
    padding: 0;
    margin: 0 0 1rem 0;
  }

  .point {
    padding: 0.5rem 0;
  }

  .point label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
  }

  .point input[type='checkbox'] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    flex-shrink: 0;
  }

  .point span {
    flex: 1;
  }

  .point span.checked {
    text-decoration: line-through;
    color: #999;
  }

  .add-point {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
  }

  .add-point-btn {
    background: #4CAF50;
    width: 100%;
    margin-top: 0.5rem;
  }

  .add-point-btn:hover {
    background: #45a049;
  }

  .error {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1rem;
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #999;
  }
</style>
