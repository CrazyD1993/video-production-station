import { env } from "cloudflare:workers";
import type { Topic, TopicInput, TopicStatus } from "../lib/topic-types";

type TopicRow = {
  id: string;
  title: string;
  hook: string;
  angle: string;
  category: string;
  status: TopicStatus;
  platforms: string;
  source_platform: string;
  source_name: string;
  source_url: string;
  why_now: string;
  evidence: string;
  shooting: string;
  content_format: string;
  risk: string;
  tags: string;
  score_pain: number;
  score_evidence: number;
  score_persona: number;
  score_repeatability: number;
  score_timeliness: number;
  score_ease: number;
  score_total: number;
  is_pinned: number;
  created_at: string;
  updated_at: string;
};

const now = "2026-07-30T09:00:00+08:00";

const seedTopics: TopicInput[] = [
  {
    id: "seed-ai-tools-less-output",
    title: "为什么 AI 工具越多，你反而越做不出东西？",
    hook: "现在有一个很奇怪的现象：AI 工具越多，很多人的作品反而越少。",
    angle: "不是工具不够强，而是每次迁移工作流都在重新支付时间成本。",
    category: "商业解释",
    status: "radar",
    platforms: "抖音 / 小红书 / X",
    sourcePlatform: "YouTube / X",
    sourceName: "Kyla Scanlon 内容结构启发",
    sourceUrl: "https://www.youtube.com/@KylaScanlon",
    whyNow: "AI 产品迭代加速，用户普遍陷入追工具与不交付的矛盾。",
    evidence: "用自己的工具试用记录、项目切换次数和最终交付数量做前后对比。",
    shooting: "固定机位口播；中段插入三个工具界面和一个未完成项目文件夹。",
    contentFormat: "60 秒商业解释",
    risk: "不能停在情绪观点，必须给出一个可执行的取舍标准。",
    tags: "工具焦虑,工作流,反常识",
    scorePain: 23,
    scoreEvidence: 22,
    scorePersona: 19,
    scoreRepeatability: 14,
    scoreTimeliness: 9,
    scoreEase: 5,
    scoreTotal: 92,
    isPinned: true,
  },
  {
    id: "seed-not-director-ai-video",
    title: "我不是导演，却用 AI 做完了一条 40 秒视频",
    hook: "我原来以为 AI 做视频最难的是生成画面，做完以后才发现，最贵的是判断什么能发。",
    angle: "用真实项目讲一个普通女性如何成为 AI 内容实验者。",
    category: "真实项目",
    status: "shortlist",
    platforms: "全平台",
    sourcePlatform: "YouTube",
    sourceName: "ami.moment 人物叙事结构",
    sourceUrl: "https://www.youtube.com/watch?v=4-89v26eTLw",
    whyNow: "这是账号的起源故事，能一次建立人设、专业度和真实感。",
    evidence: "展示脚本、分镜、失败镜头、成片和真实工时。",
    shooting: "真人开头与结尾；中段用项目文件、失败版本和成片对比。",
    contentFormat: "75 秒人物实验",
    risk: "不能做成流程汇报，要讲清楚一次判断如何改变结果。",
    tags: "起源故事,AI视频,女性IP",
    scorePain: 21,
    scoreEvidence: 25,
    scorePersona: 20,
    scoreRepeatability: 14,
    scoreTimeliness: 8,
    scoreEase: 4,
    scoreTotal: 92,
    isPinned: true,
  },
  {
    id: "seed-ai-editing-mistakes",
    title: "我怎么用 AI 剪完一条口播？包括它剪错的地方",
    hook: "AI 的确替我做掉了大部分体力活，但有三个地方不亲自检查，成片一定会翻车。",
    angle: "先展示节省，再展示错误，建立不替工具站台的可信判断。",
    category: "真实项目",
    status: "shortlist",
    platforms: "抖音 / 小红书 / YouTube",
    sourcePlatform: "YouTube",
    sourceName: "Softgirlnocode 工作流结构",
    sourceUrl: "https://www.youtube.com/watch?v=twaDQ0uwJak",
    whyNow: "AI 剪辑承诺很多，但真实错误和验收标准仍是内容空位。",
    evidence: "同一段素材的人工版、AI 初稿和最终修正版。",
    shooting: "真人交代问题；70% 录屏；错误处停帧并标出原因。",
    contentFormat: "实操拆解",
    risk: "避免做成软件操作说明，重点是验收判断。",
    tags: "AI剪辑,翻车,验收",
    scorePain: 24,
    scoreEvidence: 25,
    scorePersona: 18,
    scoreRepeatability: 15,
    scoreTimeliness: 8,
    scoreEase: 4,
    scoreTotal: 94,
    isPinned: true,
  },
  {
    id: "seed-ai-one-click-time",
    title: "AI 一键成片真能省时间吗？我记下了完整工时",
    hook: "宣传里是一键成片，我实际按下这个按钮以后，又工作了三个小时。",
    angle: "用时间账单拆穿模糊的效率叙事。",
    category: "真实项目",
    status: "inbox",
    platforms: "抖音 / 小红书",
    sourcePlatform: "自主策划",
    sourceName: "视频制作站真实流程",
    sourceUrl: "",
    whyNow: "所有 AI 产品都在卖省时间，但很少有人计算返工和审核成本。",
    evidence: "完整计时表：输入、等待、挑选、返工、配音、字幕、审核。",
    shooting: "真人口播 + 计时器 + 工时账单卡片；无需额外 B-roll。",
    contentFormat: "数据实测",
    risk: "必须使用真实计时，不能为了冲突夸大。",
    tags: "效率,工时,一键成片",
    scorePain: 24,
    scoreEvidence: 24,
    scorePersona: 18,
    scoreRepeatability: 14,
    scoreTimeliness: 8,
    scoreEase: 5,
    scoreTotal: 93,
    isPinned: false,
  },
  {
    id: "seed-codex-not-coding",
    title: "我不是程序员，Codex 对我最有用的却不是写代码",
    hook: "一个写代码的 AI，为什么最后成了我的内容制片人？",
    angle: "把技术产品翻译成普通创作者可理解的内容协作系统。",
    category: "工作流",
    status: "radar",
    platforms: "小红书 / YouTube / X",
    sourcePlatform: "小红书",
    sourceName: "阿侠就是财女命",
    sourceUrl: "https://www.xiaohongshu.com/explore/6a57824a0000000011019f68",
    whyNow: "非程序员使用 Codex 的真实场景正在增加，但内容仍被安装教程占据。",
    evidence: "展示选题库、项目文档、脚本迭代和版本记录。",
    shooting: "桌面录屏为主；真人只负责提出误解和给最终判断。",
    contentFormat: "场景解释",
    risk: "不要讲产品功能清单，要集中在一个交付闭环。",
    tags: "Codex,非程序员,内容协作",
    scorePain: 21,
    scoreEvidence: 25,
    scorePersona: 20,
    scoreRepeatability: 13,
    scoreTimeliness: 9,
    scoreEase: 5,
    scoreTotal: 93,
    isPinned: true,
  },
  {
    id: "seed-validation-most-expensive",
    title: "为什么 AI 时代最贵的不是生成，而是验收？",
    hook: "生成一段视频只要一分钟，判断它能不能发，我却用了半天。",
    angle: "把 AI 商业价值从生成速度转向判断、责任和验收。",
    category: "商业解释",
    status: "radar",
    platforms: "全平台",
    sourcePlatform: "自主策划",
    sourceName: "视频制作站审片经验",
    sourceUrl: "",
    whyNow: "模型能力趋同后，选择和验收会成为普通人真正的竞争力。",
    evidence: "同一镜头三个候选、导演审核意见和最终选择。",
    shooting: "真人近景 + 三张候选画面；用一个具体错误完成解释。",
    contentFormat: "60 秒观点",
    risk: "概念容易抽象，必须从一个肉眼可见的错误开始。",
    tags: "验收,判断力,AI商业",
    scorePain: 22,
    scoreEvidence: 24,
    scorePersona: 20,
    scoreRepeatability: 14,
    scoreTimeliness: 9,
    scoreEase: 5,
    scoreTotal: 94,
    isPinned: true,
  },
  {
    id: "seed-model-routing",
    title: "Seedance、Veo、程序动画，什么镜头该交给谁？",
    hook: "不是最贵的模型做得最好，而是不同镜头根本不该交给同一种工具。",
    angle: "建立“镜头分工”而不是“模型排行”的决策框架。",
    category: "方法系统",
    status: "inbox",
    platforms: "小红书 / YouTube",
    sourcePlatform: "自主策划",
    sourceName: "视频制作站混合生产经验",
    sourceUrl: "",
    whyNow: "AI 视频模型越来越多，普通人真正需要的是选择规则。",
    evidence: "相同需求由三种方法生成的效果、成本、时间和可控性。",
    shooting: "三栏画面对比；真人负责每一轮裁决。",
    contentFormat: "对比实验",
    risk: "避免变成模型参数横评，要围绕具体镜头任务。",
    tags: "AI视频,模型选择,导演",
    scorePain: 20,
    scoreEvidence: 24,
    scorePersona: 19,
    scoreRepeatability: 15,
    scoreTimeliness: 9,
    scoreEase: 3,
    scoreTotal: 90,
    isPinned: false,
  },
  {
    id: "seed-ai-topic-week",
    title: "我把一周选题交给 AI，结果删掉了一半",
    hook: "AI 一分钟给了我 50 个选题，我最后只留下 6 个。",
    angle: "展示选题不是生成标题，而是做取舍。",
    category: "工作流",
    status: "inbox",
    platforms: "抖音 / 小红书",
    sourcePlatform: "自主策划",
    sourceName: "私人选题中枢实验",
    sourceUrl: "",
    whyNow: "AI 批量选题已经普及，但大量内容同质、缺证据、不可拍。",
    evidence: "展示原始 50 题、淘汰规则、评分过程和最终 6 题。",
    shooting: "真人开场；屏幕录制评分；用红色淘汰印章形成节奏。",
    contentFormat: "工作流揭秘",
    risk: "不能只展示效率，要让观众学会至少一个否决标准。",
    tags: "选题,AI工作流,内容运营",
    scorePain: 23,
    scoreEvidence: 24,
    scorePersona: 19,
    scoreRepeatability: 15,
    scoreTimeliness: 8,
    scoreEase: 5,
    scoreTotal: 94,
    isPinned: false,
  },
  {
    id: "seed-three-ai-editors",
    title: "三款 AI 剪辑实测：谁省时间，谁只是换一种加班",
    hook: "三个工具都说能省时间，其中一个只是把剪辑变成了提示词加班。",
    angle: "以真实任务、总工时和返工次数为唯一评价标准。",
    category: "真实项目",
    status: "inbox",
    platforms: "小红书 / YouTube",
    sourcePlatform: "YouTube",
    sourceName: "Softgirlnocode 选题结构启发",
    sourceUrl: "https://www.youtube.com/@Softgirlnocode",
    whyNow: "工具横评很多，但以完整交付成本为标准的测试很少。",
    evidence: "统一素材、统一交付标准、总耗时、人工接管次数。",
    shooting: "固定机位开场；大部分为录屏和结果对比。",
    contentFormat: "横向实测",
    risk: "制作成本较高，先明确测试合同再开始。",
    tags: "AI剪辑,横评,加班",
    scorePain: 24,
    scoreEvidence: 25,
    scorePersona: 17,
    scoreRepeatability: 14,
    scoreTimeliness: 8,
    scoreEase: 2,
    scoreTotal: 90,
    isPinned: false,
  },
  {
    id: "seed-one-person-company",
    title: "“一人公司”为什么突然火了？一分钟讲懂",
    hook: "一人公司不是一个人干十个人的活，而是一个人决定哪些活根本不该干。",
    angle: "解释 AI 如何改变小生意的成本结构，同时反对过度浪漫化。",
    category: "商业解释",
    status: "radar",
    platforms: "抖音 / X / 小红书",
    sourcePlatform: "X",
    sourceName: "AI founder / creator 讨论",
    sourceUrl: "https://x.com/search?q=one-person%20AI%20company&f=top",
    whyNow: "一人公司成为 AI 商业高频叙事，但真实边界和风险经常被忽略。",
    evidence: "拆成获客、交付、客服、财务四项，说明哪些能自动、哪些不能。",
    shooting: "真人解释 + 四张成本卡片，不需要复杂素材。",
    contentFormat: "60 秒商业解释",
    risk: "不要承诺轻松赚钱，必须说明责任和现金流风险。",
    tags: "一人公司,AI商业,成本",
    scorePain: 22,
    scoreEvidence: 18,
    scorePersona: 18,
    scoreRepeatability: 14,
    scoreTimeliness: 10,
    scoreEase: 5,
    scoreTotal: 87,
    isPinned: false,
  },
  {
    id: "seed-dont-buy-gear",
    title: "做 AI 口播前，不要买设备，先建立这三个标准",
    hook: "大多数人缺的不是麦克风，而是不知道什么样的视频算完成。",
    angle: "用最低制作门槛建立起号标准：听得清、看得懂、有证据。",
    category: "方法系统",
    status: "selected",
    platforms: "抖音 / 小红书",
    sourcePlatform: "自主策划",
    sourceName: "女性 AI 口播对标结论",
    sourceUrl: "",
    whyNow: "适合作为账号冷启动的价值宣言，也能筛选同类目标用户。",
    evidence: "手机、领夹麦、固定机位与一条完整视频的实际对比。",
    shooting: "一机位完成；手持展示三件设备；插入一个作品结果。",
    contentFormat: "清单口播",
    risk: "不要做成反消费口号，要明确什么情况下设备才值得升级。",
    tags: "口播,设备,冷启动",
    scorePain: 21,
    scoreEvidence: 22,
    scorePersona: 18,
    scoreRepeatability: 13,
    scoreTimeliness: 7,
    scoreEase: 5,
    scoreTotal: 86,
    isPinned: false,
  },
  {
    id: "seed-ai-work-more",
    title: "为什么 AI 越强，人的工作反而可能越多？",
    hook: "AI 每替你省下一小时，团队可能立刻塞进来两小时的新任务。",
    angle: "效率工具如何抬高产出预期，而不是自动换来自由。",
    category: "商业解释",
    status: "radar",
    platforms: "抖音 / X / YouTube",
    sourcePlatform: "自主策划",
    sourceName: "AI 与劳动效率观察",
    sourceUrl: "",
    whyNow: "“AI 会不会替代工作”之外，工作密度上升是更贴近日常的矛盾。",
    evidence: "用内容生产前后每周任务量、审稿轮次和交付预期变化说明。",
    shooting: "真人口播 + 日历前后对比 + 一个橡皮筋比喻。",
    contentFormat: "观点解释",
    risk: "避免宏观空谈，必须回到一个具体职业场景。",
    tags: "工作密度,效率悖论,AI职场",
    scorePain: 24,
    scoreEvidence: 19,
    scorePersona: 19,
    scoreRepeatability: 13,
    scoreTimeliness: 9,
    scoreEase: 5,
    scoreTotal: 89,
    isPinned: false,
  },
];

export async function ensureTopicsSchema() {
  const db = env.DB;
  if (!db) throw new Error("D1 binding DB is unavailable");

  await db.batch([
    db.prepare(`
      CREATE TABLE IF NOT EXISTS topics (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        hook TEXT NOT NULL,
        angle TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'radar',
        platforms TEXT NOT NULL DEFAULT '全平台',
        source_platform TEXT NOT NULL DEFAULT '自主策划',
        source_name TEXT NOT NULL DEFAULT '私人选题系统',
        source_url TEXT NOT NULL DEFAULT '',
        why_now TEXT NOT NULL DEFAULT '',
        evidence TEXT NOT NULL DEFAULT '',
        shooting TEXT NOT NULL DEFAULT '',
        content_format TEXT NOT NULL DEFAULT '真人口播',
        risk TEXT NOT NULL DEFAULT '',
        tags TEXT NOT NULL DEFAULT '',
        score_pain INTEGER NOT NULL DEFAULT 0,
        score_evidence INTEGER NOT NULL DEFAULT 0,
        score_persona INTEGER NOT NULL DEFAULT 0,
        score_repeatability INTEGER NOT NULL DEFAULT 0,
        score_timeliness INTEGER NOT NULL DEFAULT 0,
        score_ease INTEGER NOT NULL DEFAULT 0,
        score_total INTEGER NOT NULL DEFAULT 0,
        is_pinned INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    `),
    db.prepare(
      "CREATE INDEX IF NOT EXISTS topics_status_score_idx ON topics(status, score_total DESC)",
    ),
    db.prepare(
      "CREATE INDEX IF NOT EXISTS topics_updated_idx ON topics(updated_at DESC)",
    ),
  ]);

  const count = await db
    .prepare("SELECT COUNT(*) AS count FROM topics")
    .first<{ count: number }>();

  if ((count?.count ?? 0) === 0) {
    const statements = seedTopics.map((topic) => {
      const createdAt = topic.createdAt ?? now;
      const updatedAt = topic.updatedAt ?? now;
      return db
        .prepare(`
          INSERT INTO topics (
            id, title, hook, angle, category, status, platforms,
            source_platform, source_name, source_url, why_now, evidence,
            shooting, content_format, risk, tags, score_pain, score_evidence,
            score_persona, score_repeatability, score_timeliness, score_ease,
            score_total, is_pinned, created_at, updated_at
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `)
        .bind(
          topic.id ?? crypto.randomUUID(),
          topic.title,
          topic.hook,
          topic.angle,
          topic.category,
          topic.status,
          topic.platforms,
          topic.sourcePlatform,
          topic.sourceName,
          topic.sourceUrl,
          topic.whyNow,
          topic.evidence,
          topic.shooting,
          topic.contentFormat,
          topic.risk,
          topic.tags,
          topic.scorePain,
          topic.scoreEvidence,
          topic.scorePersona,
          topic.scoreRepeatability,
          topic.scoreTimeliness,
          topic.scoreEase,
          topic.scoreTotal,
          topic.isPinned ? 1 : 0,
          createdAt,
          updatedAt,
        );
    });
    await db.batch(statements);
  }
}

function mapTopic(row: TopicRow): Topic {
  return {
    id: row.id,
    title: row.title,
    hook: row.hook,
    angle: row.angle,
    category: row.category,
    status: row.status,
    platforms: row.platforms,
    sourcePlatform: row.source_platform,
    sourceName: row.source_name,
    sourceUrl: row.source_url,
    whyNow: row.why_now,
    evidence: row.evidence,
    shooting: row.shooting,
    contentFormat: row.content_format,
    risk: row.risk,
    tags: row.tags,
    scorePain: row.score_pain,
    scoreEvidence: row.score_evidence,
    scorePersona: row.score_persona,
    scoreRepeatability: row.score_repeatability,
    scoreTimeliness: row.score_timeliness,
    scoreEase: row.score_ease,
    scoreTotal: row.score_total,
    isPinned: Boolean(row.is_pinned),
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

export async function listTopics(): Promise<Topic[]> {
  await ensureTopicsSchema();
  const result = await env.DB.prepare(
    "SELECT * FROM topics ORDER BY is_pinned DESC, score_total DESC, updated_at DESC",
  ).all<TopicRow>();
  return result.results.map(mapTopic);
}

export async function createTopics(inputs: TopicInput[]): Promise<Topic[]> {
  await ensureTopicsSchema();
  const db = env.DB;
  const created = inputs.map((input) => {
    const id = input.id ?? crypto.randomUUID();
    const createdAt = input.createdAt ?? new Date().toISOString();
    const updatedAt = input.updatedAt ?? createdAt;
    return { ...input, id, createdAt, updatedAt };
  });

  await db.batch(
    created.map((topic) =>
      db
        .prepare(`
          INSERT INTO topics (
            id, title, hook, angle, category, status, platforms,
            source_platform, source_name, source_url, why_now, evidence,
            shooting, content_format, risk, tags, score_pain, score_evidence,
            score_persona, score_repeatability, score_timeliness, score_ease,
            score_total, is_pinned, created_at, updated_at
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `)
        .bind(
          topic.id,
          topic.title,
          topic.hook,
          topic.angle,
          topic.category,
          topic.status,
          topic.platforms,
          topic.sourcePlatform,
          topic.sourceName,
          topic.sourceUrl,
          topic.whyNow,
          topic.evidence,
          topic.shooting,
          topic.contentFormat,
          topic.risk,
          topic.tags,
          topic.scorePain,
          topic.scoreEvidence,
          topic.scorePersona,
          topic.scoreRepeatability,
          topic.scoreTimeliness,
          topic.scoreEase,
          topic.scoreTotal,
          topic.isPinned ? 1 : 0,
          topic.createdAt,
          topic.updatedAt,
        ),
    ),
  );

  return created as Topic[];
}

const updatableColumns: Record<string, string> = {
  title: "title",
  hook: "hook",
  angle: "angle",
  category: "category",
  status: "status",
  platforms: "platforms",
  sourcePlatform: "source_platform",
  sourceName: "source_name",
  sourceUrl: "source_url",
  whyNow: "why_now",
  evidence: "evidence",
  shooting: "shooting",
  contentFormat: "content_format",
  risk: "risk",
  tags: "tags",
  scorePain: "score_pain",
  scoreEvidence: "score_evidence",
  scorePersona: "score_persona",
  scoreRepeatability: "score_repeatability",
  scoreTimeliness: "score_timeliness",
  scoreEase: "score_ease",
  scoreTotal: "score_total",
  isPinned: "is_pinned",
};

export async function updateTopic(
  id: string,
  updates: Partial<Topic>,
): Promise<Topic | null> {
  await ensureTopicsSchema();
  const entries = Object.entries(updates).filter(
    ([key]) => key in updatableColumns,
  );
  if (entries.length === 0) return null;

  const sets = entries.map(([key]) => `${updatableColumns[key]} = ?`);
  const values = entries.map(([key, value]) =>
    key === "isPinned" ? (value ? 1 : 0) : value,
  );
  const updatedAt = new Date().toISOString();

  await env.DB.prepare(
    `UPDATE topics SET ${sets.join(", ")}, updated_at = ? WHERE id = ?`,
  )
    .bind(...values, updatedAt, id)
    .run();

  const row = await env.DB.prepare("SELECT * FROM topics WHERE id = ?")
    .bind(id)
    .first<TopicRow>();
  return row ? mapTopic(row) : null;
}
