export type AssignmentField = "room" | "teacher" | "coach";
export type Assignment = Partial<Record<AssignmentField, string>>;
export type Changes = Record<string, Assignment>;

export interface Session {
  id: string;
  date: string;
  class_name: string;
  topic: string;
  start: string;
  end: string;
  format: "online" | "offline";
  room: string;
  teacher: string;
  coach: string;
  room_options: string[];
  teachers: string[];
  coaches: string[];
  published_room?: string;
  update_source?: string;
  online_source?: string;
}

export interface RoomUpdate {
  id: string;
  label: string;
  session: string;
  room: string;
  source: string;
}

export interface Issue {
  sessions: string[];
  field: string;
  message: string;
}

export interface Review {
  rows: Session[];
  updates: RoomUpdate[];
  issues: Issue[];
  impact: (RoomUpdate & {
    old_room: string | null;
    class_name: string;
    date: string;
    start: string;
    end: string;
  }) | null;
  notice: string | null;
  proposal: Changes | null;
  method: "model" | "rules";
}

export interface Draft {
  week: string;
  update: string;
  changes: Changes;
}

export interface Handoff {
  approved: true;
  week: string;
  rows: Session[];
  notice: string | null;
}

export function shortDate(value: string) {
  return value.split("-").reverse().join("/");
}
