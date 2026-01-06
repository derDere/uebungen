export interface Tool {
  id: number;
  name: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ToolWithChecklists extends Tool {
  checklists: CheckList[];
}

export interface CheckListPointTemplate {
  id: number;
  name: string;
  datatype: string;
  created_at: string;
  updated_at: string;
}

export interface CheckListTemplate {
  id: number;
  name: string;
  status: string;
  created_at: string;
  updated_at: string;
  point_templates: CheckListPointTemplate[];
}

export interface CheckListPoint {
  id: number;
  name: string;
  status: string;
  is_checked: boolean;
  check_list_point_template_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface CheckList {
  id: number;
  name: string;
  status: string;
  tool_id: number;
  check_list_template_id: number | null;
  created_at: string;
  updated_at: string;
  points: CheckListPoint[];
}

export interface ToolCreate {
  name: string;
  status?: string;
}

export interface CheckListCreate {
  name: string;
  tool_id: number;
  status?: string;
  check_list_template_id?: number | null;
}

export interface CheckListPointCreate {
  name: string;
  status?: string;
  is_checked?: boolean;
  check_list_point_template_id?: number | null;
}

export interface CheckListTemplateCreate {
  name: string;
  status?: string;
}

export interface CheckListPointTemplateCreate {
  name: string;
  datatype?: string;
}

export interface SearchResults {
  tools: Tool[];
  checklists: CheckList[];
  points: CheckListPoint[];
}
