export const TOPIC_STATUSES = [
  "radar",
  "inbox",
  "shortlist",
  "selected",
  "produced",
  "archived",
] as const;

export type TopicStatus = (typeof TOPIC_STATUSES)[number];

export type Topic = {
  id: string;
  title: string;
  hook: string;
  angle: string;
  category: string;
  status: TopicStatus;
  platforms: string;
  sourcePlatform: string;
  sourceName: string;
  sourceUrl: string;
  whyNow: string;
  evidence: string;
  shooting: string;
  contentFormat: string;
  risk: string;
  tags: string;
  scorePain: number;
  scoreEvidence: number;
  scorePersona: number;
  scoreRepeatability: number;
  scoreTimeliness: number;
  scoreEase: number;
  scoreTotal: number;
  isPinned: boolean;
  createdAt: string;
  updatedAt: string;
};

export type TopicInput = Omit<Topic, "id" | "createdAt" | "updatedAt"> & {
  id?: string;
  createdAt?: string;
  updatedAt?: string;
};

export const STATUS_META: Record<
  TopicStatus,
  { label: string; short: string; description: string }
> = {
  radar: { label: "今日雷达", short: "雷达", description: "系统当天发现，等待判断" },
  inbox: { label: "候选池", short: "候选", description: "值得保留，尚未进入拍摄" },
  shortlist: { label: "重点观察", short: "重点", description: "高分题，等待最终选择" },
  selected: { label: "已选待拍", short: "待拍", description: "已经确认，进入脚本与拍摄" },
  produced: { label: "已经完成", short: "完成", description: "已制作或已发布" },
  archived: { label: "归档", short: "归档", description: "暂时放弃，保留判断记录" },
};
