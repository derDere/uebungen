<script lang="ts">
  import { onMount } from 'svelte';
  import { templatesApi } from '../api';
  import type { CheckListTemplate, CheckListPointTemplate } from '../types';

  let templates: CheckListTemplate[] = [];
  let pointTemplates: CheckListPointTemplate[] = [];
  let selectedTemplateId: number | null = null;
  let newTemplateName = '';
  let newPointTemplateName = '';
  let newPointTemplateDatatype = 'text';
  let loading = false;
  let error = '';

  $: selectedTemplate = templates.find((t) => t.id === selectedTemplateId);

  async function loadData() {
    try {
      loading = true;
      [templates, pointTemplates] = await Promise.all([
        templatesApi.checklist.list(),
        templatesApi.point.list(),
      ]);
    } catch (e) {
      error = 'Failed to load templates';
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function createTemplate() {
    if (!newTemplateName.trim()) return;

    try {
      const newTemplate = await templatesApi.checklist.create({
        name: newTemplateName,
        status: 'active',
      });
      newTemplateName = '';
      selectedTemplateId = newTemplate.id;
      await loadData();
    } catch (e) {
      error = 'Failed to create template';
      console.error(e);
    }
  }

  async function deleteTemplate(id: number) {
    if (!confirm('Delete this template?')) return;

    try {
      await templatesApi.checklist.delete(id);
      if (selectedTemplateId === id) {
        selectedTemplateId = null;
      }
      await loadData();
    } catch (e) {
      error = 'Failed to delete template';
      console.error(e);
    }
  }

  async function createPointTemplate() {
    if (!newPointTemplateName.trim()) return;

    try {
      await templatesApi.point.create({
        name: newPointTemplateName,
        datatype: newPointTemplateDatatype,
      });
      newPointTemplateName = '';
      newPointTemplateDatatype = 'text';
      await loadData();
    } catch (e) {
      error = 'Failed to create point template';
      console.error(e);
    }
  }

  async function deletePointTemplate(id: number) {
    if (!confirm('Delete this point template?')) return;

    try {
      await templatesApi.point.delete(id);
      await loadData();
    } catch (e) {
      error = 'Failed to delete point template';
      console.error(e);
    }
  }

  async function addPointToTemplate(pointTemplateId: number) {
    if (!selectedTemplateId) return;

    try {
      await templatesApi.checklist.addPointTemplate(
        selectedTemplateId,
        pointTemplateId
      );
      await loadData();
    } catch (e) {
      error = 'Failed to add point to template';
      console.error(e);
    }
  }

  async function removePointFromTemplate(pointTemplateId: number) {
    if (!selectedTemplateId) return;

    try {
      await templatesApi.checklist.removePointTemplate(
        selectedTemplateId,
        pointTemplateId
      );
      await loadData();
    } catch (e) {
      error = 'Failed to remove point from template';
      console.error(e);
    }
  }

  onMount(loadData);
</script>

<div class="template-editor">
  <h2>Templates</h2>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <div class="section">
    <h3>Checklist Templates</h3>
    <div class="create-form">
      <input
        type="text"
        bind:value={newTemplateName}
        placeholder="New template name..."
        on:keydown={(e) => e.key === 'Enter' && createTemplate()}
      />
      <button on:click={createTemplate}>Create Template</button>
    </div>

    <ul class="template-list">
      {#each templates as template (template.id)}
        <li
          class:selected={selectedTemplateId === template.id}
          on:click={() => (selectedTemplateId = template.id)}
        >
          <span>{template.name}</span>
          <button
            class="delete-btn"
            on:click|stopPropagation={() => deleteTemplate(template.id)}
          >
            ×
          </button>
        </li>
      {/each}
    </ul>
  </div>

  {#if selectedTemplate}
    <div class="section">
      <h3>Points in "{selectedTemplate.name}"</h3>
      <ul class="point-list">
        {#each selectedTemplate.point_templates as pt (pt.id)}
          <li>
            <span>{pt.name} <small>({pt.datatype})</small></span>
            <button
              class="remove-btn"
              on:click={() => removePointFromTemplate(pt.id)}
            >
              Remove
            </button>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  <div class="section">
    <h3>Point Templates</h3>
    <div class="create-form">
      <input
        type="text"
        bind:value={newPointTemplateName}
        placeholder="Point template name..."
      />
      <select bind:value={newPointTemplateDatatype}>
        <option value="text">Text</option>
        <option value="number">Number</option>
        <option value="boolean">Boolean</option>
      </select>
      <button on:click={createPointTemplate}>Create Point</button>
    </div>

    <ul class="point-list">
      {#each pointTemplates as pt (pt.id)}
        <li>
          <span>{pt.name} <small>({pt.datatype})</small></span>
          <div class="actions">
            {#if selectedTemplateId}
              <button
                class="add-btn"
                on:click={() => addPointToTemplate(pt.id)}
              >
                Add to Template
              </button>
            {/if}
            <button
              class="delete-btn-small"
              on:click={() => deletePointTemplate(pt.id)}
            >
              ×
            </button>
          </div>
        </li>
      {/each}
    </ul>
  </div>
</div>

<style>
  .template-editor {
    padding: 1rem;
    height: 100%;
    overflow-y: auto;
  }

  h2 {
    margin: 0 0 1.5rem 0;
  }

  h3 {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
  }

  .section {
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #eee;
  }

  .section:last-child {
    border-bottom: none;
  }

  .create-form {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  input,
  select {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .create-form input {
    flex: 1;
  }

  button {
    padding: 0.5rem 1rem;
    background: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    white-space: nowrap;
  }

  button:hover {
    background: #1976D2;
  }

  .template-list,
  .point-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .template-list li,
  .point-list li {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: #f5f5f5;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .template-list li {
    cursor: pointer;
  }

  .template-list li:hover {
    background: #ebebeb;
  }

  .template-list li.selected {
    background: #2196F3;
    color: white;
  }

  .point-list li span {
    flex: 1;
  }

  small {
    color: #666;
    font-size: 0.85em;
  }

  .selected small {
    color: rgba(255, 255, 255, 0.8);
  }

  .actions {
    display: flex;
    gap: 0.5rem;
  }

  .delete-btn,
  .delete-btn-small {
    background: transparent;
    color: #999;
    font-size: 1.5rem;
    padding: 0;
    width: 24px;
    height: 24px;
  }

  .delete-btn:hover,
  .delete-btn-small:hover {
    color: #f44336;
  }

  .selected .delete-btn {
    color: rgba(255, 255, 255, 0.7);
  }

  .selected .delete-btn:hover {
    color: white;
  }

  .remove-btn {
    background: #f44336;
    font-size: 0.85rem;
    padding: 0.4rem 0.7rem;
  }

  .remove-btn:hover {
    background: #d32f2f;
  }

  .add-btn {
    background: #4CAF50;
    font-size: 0.85rem;
    padding: 0.4rem 0.7rem;
  }

  .add-btn:hover {
    background: #45a049;
  }

  .error {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1rem;
  }
</style>
