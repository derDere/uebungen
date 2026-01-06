<script lang="ts">
  import { search } from '../api';
  import type { SearchResults } from '../types';

  let query = '';
  let results: SearchResults | null = null;
  let searching = false;
  let debounceTimer: number;

  async function performSearch() {
    if (!query.trim()) {
      results = null;
      return;
    }

    try {
      searching = true;
      results = await search(query);
    } catch (e) {
      console.error('Search failed:', e);
    } finally {
      searching = false;
    }
  }

  function debounceSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(performSearch, 300);
  }

  $: if (query !== undefined) {
    debounceSearch();
  }
</script>

<div class="search-filter">
  <input
    type="search"
    bind:value={query}
    placeholder="Search tools, checklists, points..."
    class="search-input"
  />

  {#if searching}
    <div class="searching">Searching...</div>
  {/if}

  {#if results && query.trim()}
    <div class="results">
      {#if results.tools.length > 0}
        <div class="result-group">
          <h4>Tools ({results.tools.length})</h4>
          <ul>
            {#each results.tools as tool (tool.id)}
              <li>{tool.name}</li>
            {/each}
          </ul>
        </div>
      {/if}

      {#if results.checklists.length > 0}
        <div class="result-group">
          <h4>Checklists ({results.checklists.length})</h4>
          <ul>
            {#each results.checklists as checklist (checklist.id)}
              <li>{checklist.name}</li>
            {/each}
          </ul>
        </div>
      {/if}

      {#if results.points.length > 0}
        <div class="result-group">
          <h4>Points ({results.points.length})</h4>
          <ul>
            {#each results.points as point (point.id)}
              <li>
                {point.name}
                {#if point.is_checked}✓{/if}
              </li>
            {/each}
          </ul>
        </div>
      {/if}

      {#if results.tools.length === 0 && results.checklists.length === 0 && results.points.length === 0}
        <div class="no-results">No results found</div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .search-filter {
    position: relative;
  }

  .search-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  .searching {
    padding: 0.5rem;
    text-align: center;
    color: #666;
    font-size: 0.9rem;
  }

  .results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin-top: 0.5rem;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-height: 400px;
    overflow-y: auto;
    z-index: 100;
  }

  .result-group {
    padding: 0.75rem;
    border-bottom: 1px solid #eee;
  }

  .result-group:last-child {
    border-bottom: none;
  }

  .result-group h4 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    color: #666;
    text-transform: uppercase;
  }

  .result-group ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .result-group li {
    padding: 0.4rem 0;
    font-size: 0.95rem;
  }

  .no-results {
    padding: 1.5rem;
    text-align: center;
    color: #999;
  }
</style>
