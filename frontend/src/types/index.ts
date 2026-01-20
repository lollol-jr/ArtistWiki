export interface Artist {
  id: string
  name: string
  type: 'painter' | 'writer' | 'musician'
  birth_date?: string
  death_date?: string
  nationality?: string
  biography?: string
  mediawiki_page_id?: number
  mediawiki_page_title?: string
  created_at: string
  updated_at: string
}

export interface Work {
  id: string
  artist_id: string
  title: string
  year?: number
  type?: string
  description?: string
  mediawiki_page_id?: number
  mediawiki_page_title?: string
  created_at: string
  updated_at: string
}

export interface AgentJob {
  id: string
  job_type: string
  status: 'pending' | 'running' | 'success' | 'failed'
  target_id?: string
  target_type?: string
  input_data?: any
  output_data?: any
  error_message?: string
  started_at?: string
  completed_at?: string
  created_at: string
}

export interface Relationship {
  id: string
  source_artist_id: string
  target_artist_id: string
  relationship_type: string
  description?: string
  created_at: string
}
