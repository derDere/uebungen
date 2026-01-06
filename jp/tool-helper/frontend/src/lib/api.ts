import type {
  Tool,
  ToolWithChecklists,
  ToolCreate,
  CheckList,
  CheckListCreate,
  CheckListPoint,
  CheckListPointCreate,
  CheckListTemplate,
  CheckListTemplateCreate,
  CheckListPointTemplate,
  CheckListPointTemplateCreate,
  SearchResults,
} from './types';

const API_BASE = '/api';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

// Tools API
export const toolsApi = {
  async list(): Promise<Tool[]> {
    return fetchJson<Tool[]>('/tools/');
  },

  async get(id: number): Promise<ToolWithChecklists> {
    return fetchJson<ToolWithChecklists>(`/tools/${id}`);
  },

  async create(data: ToolCreate): Promise<Tool> {
    return fetchJson<Tool>('/tools/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async update(id: number, data: Partial<ToolCreate>): Promise<Tool> {
    return fetchJson<Tool>(`/tools/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async delete(id: number): Promise<void> {
    await fetch(`${API_BASE}/tools/${id}`, { method: 'DELETE' });
  },
};

// Checklists API
export const checklistsApi = {
  async list(toolId?: number): Promise<CheckList[]> {
    const url = toolId ? `/checklists/?tool_id=${toolId}` : '/checklists/';
    return fetchJson<CheckList[]>(url);
  },

  async get(id: number): Promise<CheckList> {
    return fetchJson<CheckList>(`/checklists/${id}`);
  },

  async create(data: CheckListCreate): Promise<CheckList> {
    return fetchJson<CheckList>('/checklists/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async createFromTemplate(
    templateId: number,
    toolId: number,
    name?: string
  ): Promise<CheckList> {
    return fetchJson<CheckList>(`/checklists/from-template/${templateId}`, {
      method: 'POST',
      body: JSON.stringify({ tool_id: toolId, name }),
    });
  },

  async update(id: number, data: Partial<CheckListCreate>): Promise<CheckList> {
    return fetchJson<CheckList>(`/checklists/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async delete(id: number): Promise<void> {
    await fetch(`${API_BASE}/checklists/${id}`, { method: 'DELETE' });
  },

  async togglePoint(checklistId: number, pointId: number): Promise<CheckListPoint> {
    return fetchJson<CheckListPoint>(
      `/checklists/${checklistId}/points/${pointId}/toggle`,
      { method: 'PATCH' }
    );
  },

  async addPoint(checklistId: number, data: CheckListPointCreate): Promise<CheckList> {
    return fetchJson<CheckList>(`/checklists/${checklistId}/points`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async removePoint(checklistId: number, pointId: number): Promise<void> {
    await fetch(`${API_BASE}/checklists/${checklistId}/points/${pointId}`, {
      method: 'DELETE',
    });
  },
};

// Templates API
export const templatesApi = {
  checklist: {
    async list(): Promise<CheckListTemplate[]> {
      return fetchJson<CheckListTemplate[]>('/templates/checklist');
    },

    async get(id: number): Promise<CheckListTemplate> {
      return fetchJson<CheckListTemplate>(`/templates/checklist/${id}`);
    },

    async create(data: CheckListTemplateCreate): Promise<CheckListTemplate> {
      return fetchJson<CheckListTemplate>('/templates/checklist', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    },

    async update(
      id: number,
      data: Partial<CheckListTemplateCreate>
    ): Promise<CheckListTemplate> {
      return fetchJson<CheckListTemplate>(`/templates/checklist/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      });
    },

    async delete(id: number): Promise<void> {
      await fetch(`${API_BASE}/templates/checklist/${id}`, { method: 'DELETE' });
    },

    async addPointTemplate(
      templateId: number,
      pointTemplateId: number
    ): Promise<CheckListTemplate> {
      return fetchJson<CheckListTemplate>(
        `/templates/checklist/${templateId}/points/${pointTemplateId}`,
        { method: 'POST' }
      );
    },

    async removePointTemplate(
      templateId: number,
      pointTemplateId: number
    ): Promise<void> {
      await fetch(
        `${API_BASE}/templates/checklist/${templateId}/points/${pointTemplateId}`,
        { method: 'DELETE' }
      );
    },
  },

  point: {
    async list(): Promise<CheckListPointTemplate[]> {
      return fetchJson<CheckListPointTemplate[]>('/templates/point');
    },

    async get(id: number): Promise<CheckListPointTemplate> {
      return fetchJson<CheckListPointTemplate>(`/templates/point/${id}`);
    },

    async create(data: CheckListPointTemplateCreate): Promise<CheckListPointTemplate> {
      return fetchJson<CheckListPointTemplate>('/templates/point', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    },

    async update(
      id: number,
      data: Partial<CheckListPointTemplateCreate>
    ): Promise<CheckListPointTemplate> {
      return fetchJson<CheckListPointTemplate>(`/templates/point/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      });
    },

    async delete(id: number): Promise<void> {
      await fetch(`${API_BASE}/templates/point/${id}`, { method: 'DELETE' });
    },
  },
};

// Search API
export async function search(query: string): Promise<SearchResults> {
  return fetchJson<SearchResults>(`/checklists/search/${encodeURIComponent(query)}`);
}

// Export API
export const exportApi = {
  async json(): Promise<string> {
    const response = await fetch(`${API_BASE}/export/json`);
    return response.text();
  },

  async yaml(): Promise<string> {
    const response = await fetch(`${API_BASE}/export/yaml`);
    return response.text();
  },

  async csv(): Promise<string> {
    const response = await fetch(`${API_BASE}/export/csv`);
    return response.text();
  },

  async markdown(): Promise<string> {
    const response = await fetch(`${API_BASE}/export/markdown`);
    return response.text();
  },
};
