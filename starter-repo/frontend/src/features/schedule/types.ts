export type Assignment = { room?: string; teacher?: string; coach?: string[]; resolution_note?: string; meeting_url?: string };
export type Changes = Record<string, Assignment>;

export interface Session {
  id: string;
  session: string;
  group_id: string;
  slot: string;
  room_status: string;
  coach_required: boolean;
  resolution_note: string;
  meeting_url: string;
  extra_rooms: string[];
  key_coaches: string[];
  data_warnings: string[];
  source: string;
  sources: Array<{kind: string; ref: string; value: string}>;
  date: string;
  class_name: string;
  topic: string;
  start: string;
  end: string;
  format: "online" | "offline";
  room: string;
  teacher: string;
  coach: string[];
  room_options: string[];
  teachers: string[];
  coaches: string[];
  published_room?: string | null;
  update_source?: string;
  online_source?: string;
}

export interface RoomUpdate {
  id: string;
  label: string;
  session: string;
  room: string;
  source: string;
  confirmed: boolean;
}

export interface Issue {
  sessions: string[];
  field: string;
  message: string;
  severity?: string;
  source?: string;
}

export interface Review {
  rows: Session[];
  updates: RoomUpdate[];
  issues: Issue[];
  impact: (RoomUpdate & {
    old_room: string | null;
    baseline_room: string;
    baseline_kind: string;
    class_name: string;
    date: string;
    start: string;
    end: string;
  }) | null;
  notice: string | null;
  proposal: Changes | null;
  method: "model" | "rules";
  explanation: string;
  questions: string[];
  ai_error: string | null;
  usage: {model: string; tokens_in: number; tokens_out: number} | null;
  saved_at?: string;
}

export interface Draft {
  week: string;
  update: string;
  changes: Changes;
}

export interface Handoff {
  approved: true;
  approved_at: string;
  week: string;
  rows: Session[];
  notice: string | null;
}

export function shortDate(value: string) {
  return value.split("-").reverse().join("/");
}

export interface AIStatus { provider: string; model: string; ready: boolean; message: string }
export interface DatasetMetadata { course: string; fingerprint: string; sessions: number; registrations: number; coach_assignments: number; requests: number; date_start: string; date_end: string; notes: string[]; files: Array<{name: string; sha256: string; sheets: string[]}> }
export interface SourceData {metadata: DatasetMetadata; requests: Array<{id: string; name: string; from: string; to: string; reason: string; status: string; note: string; source: string}>; workload: Array<{name: string; key: string; lab: string; total: string; source: string}>}
export interface AssistantReply {answer: string; references: string[]; usage: {model: string; tokens_in: number; tokens_out: number}}
