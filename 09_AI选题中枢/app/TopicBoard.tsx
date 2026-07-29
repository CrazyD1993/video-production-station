"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  STATUS_META,
  TOPIC_STATUSES,
  type Topic,
  type TopicInput,
  type TopicStatus,
} from "../lib/topic-types";

const categoryOptions = [
  "全部栏目",
  "真实项目",
  "商业解释",
  "工作流",
  "方法系统",
  "女性转型",
  "行业观察",
];

const platformOptions = ["全部平台", "抖音", "小红书", "YouTube", "X"];

const emptyForm: TopicInput = {
  title: "",
  hook: "",
  angle: "",
  category: "真实项目",
  status: "inbox",
  platforms: "全平台",
  sourcePlatform: "自主策划",
  sourceName: "手动收录",
  sourceUrl: "",
  whyNow: "",
  evidence: "",
  shooting: "",
  contentFormat: "真人口播",
  risk: "",
  tags: "",
  scorePain: 20,
  scoreEvidence: 20,
  scorePersona: 18,
  scoreRepeatability: 12,
  scoreTimeliness: 8,
  scoreEase: 4,
  scoreTotal: 82,
  isPinned: false,
};

function scoreTone(score: number) {
  if (score >= 90) return "score-excellent";
  if (score >= 80) return "score-good";
  return "score-watch";
}

function formatTime(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-CN", {
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export default function TopicBoard() {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<TopicStatus | "all">("all");
  const [category, setCategory] = useState("全部栏目");
  const [platform, setPlatform] = useState("全部平台");
  const [sort, setSort] = useState<"score" | "updated">("score");
  const [detail, setDetail] = useState<Topic | null>(null);
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState<TopicInput>(emptyForm);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    void loadTopics();
  }, []);

  async function loadTopics() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/topics", { cache: "no-store" });
      const data = (await response.json()) as { topics?: Topic[]; error?: string };
      if (!response.ok) throw new Error(data.error ?? "读取题库失败");
      setTopics(data.topics ?? []);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "读取题库失败");
    } finally {
      setLoading(false);
    }
  }

  const counts = useMemo(
    () =>
      TOPIC_STATUSES.reduce(
        (result, key) => {
          result[key] = topics.filter((topic) => topic.status === key).length;
          return result;
        },
        {} as Record<TopicStatus, number>,
      ),
    [topics],
  );

  const filteredTopics = useMemo(() => {
    const query = search.trim().toLowerCase();
    return topics
      .filter((topic) => status === "all" || topic.status === status)
      .filter(
        (topic) => category === "全部栏目" || topic.category === category,
      )
      .filter(
        (topic) =>
          platform === "全部平台" || topic.platforms.includes(platform),
      )
      .filter(
        (topic) =>
          !query ||
          [
            topic.title,
            topic.hook,
            topic.angle,
            topic.tags,
            topic.sourceName,
          ]
            .join(" ")
            .toLowerCase()
            .includes(query),
      )
      .sort((a, b) =>
        sort === "score"
          ? b.scoreTotal - a.scoreTotal
          : new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
      );
  }, [topics, status, category, platform, search, sort]);

  const radar = topics
    .filter((topic) => topic.status === "radar")
    .sort((a, b) => b.scoreTotal - a.scoreTotal);
  const bestRadar = radar[0];
  const readyCount = topics.filter(
    (topic) => topic.status === "selected" || topic.status === "shortlist",
  ).length;
  const highScoreCount = topics.filter((topic) => topic.scoreTotal >= 90).length;

  async function patchTopic(id: string, updates: Partial<Topic>) {
    const previous = topics;
    setTopics((current) =>
      current.map((topic) =>
        topic.id === id ? { ...topic, ...updates } : topic,
      ),
    );
    try {
      const response = await fetch("/api/topics", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, updates }),
      });
      const data = (await response.json()) as { topic?: Topic; error?: string };
      if (!response.ok || !data.topic) {
        throw new Error(data.error ?? "更新失败");
      }
      setTopics((current) =>
        current.map((topic) => (topic.id === id ? data.topic! : topic)),
      );
      setDetail((current) =>
        current?.id === id ? data.topic ?? current : current,
      );
    } catch (reason) {
      setTopics(previous);
      setError(reason instanceof Error ? reason.message : "更新失败");
    }
  }

  async function submitTopic(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    const scoreTotal =
      form.scorePain +
      form.scoreEvidence +
      form.scorePersona +
      form.scoreRepeatability +
      form.scoreTimeliness +
      form.scoreEase;
    try {
      const response = await fetch("/api/topics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, scoreTotal }),
      });
      const data = (await response.json()) as {
        topics?: Topic[];
        error?: string;
      };
      if (!response.ok || !data.topics?.[0]) {
        throw new Error(data.error ?? "新增失败");
      }
      setTopics((current) => [data.topics![0], ...current]);
      setForm(emptyForm);
      setAdding(false);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "新增失败");
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="回到选题罗盘顶部">
          <span className="brand-mark">D</span>
          <span>
            <strong>选题罗盘</strong>
            <small>Dengqi&apos;s AI Content OS</small>
          </span>
        </a>
        <div className="topbar-actions">
          <span className="sync-state">
            <i />
            云端同步
          </span>
          <button className="button button-primary" onClick={() => setAdding(true)}>
            <span>＋</span> 收录选题
          </button>
        </div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <span className="eyebrow">私人内容编辑部 · 2026 / 07 / 30</span>
          <h1>
            不追每个热点，
            <br />
            只留下<span>值得你讲</span>的题。
          </h1>
          <p>
            为“真实项目实验者 × 商业翻译者 × 独立审片人”定位建立的私人选题系统。
            每一道题，都要经得起证据、人格与可执行性的检验。
          </p>
        </div>

        <article className="daily-card">
          <div className="daily-card-head">
            <span className="live-label"><i /> 今日主推</span>
            <span>{bestRadar ? `${bestRadar.scoreTotal} 分` : "等待更新"}</span>
          </div>
          {bestRadar ? (
            <>
              <h2>{bestRadar.title}</h2>
              <p>{bestRadar.hook}</p>
              <div className="daily-card-foot">
                <button onClick={() => setDetail(bestRadar)}>查看为什么值得拍</button>
                <button
                  className="round-action"
                  aria-label="加入重点观察"
                  onClick={() => void patchTopic(bestRadar.id, { status: "shortlist" })}
                >
                  ↗
                </button>
              </div>
            </>
          ) : (
            <p>每日雷达更新后，最高分选题会出现在这里。</p>
          )}
        </article>
      </section>

      <section className="metrics" aria-label="题库概览">
        <article>
          <span>题库总量</span>
          <strong>{topics.length}</strong>
          <small>持续积累，不追求虚假数量</small>
        </article>
        <article>
          <span>90 分以上</span>
          <strong>{highScoreCount}</strong>
          <small>证据与人设同时成立</small>
        </article>
        <article>
          <span>重点 / 待拍</span>
          <strong>{readyCount}</strong>
          <small>下一步可以进入脚本</small>
        </article>
        <article>
          <span>今日雷达</span>
          <strong>{counts.radar ?? 0}</strong>
          <small>系统新发现，等待裁决</small>
        </article>
      </section>

      <section className="workspace">
        <aside className="sidebar">
          <div className="sidebar-title">工作流</div>
          <button
            className={status === "all" ? "nav-item active" : "nav-item"}
            onClick={() => setStatus("all")}
          >
            <span><b>⌘</b> 全部选题</span>
            <em>{topics.length}</em>
          </button>
          {TOPIC_STATUSES.map((key) => (
            <button
              key={key}
              className={status === key ? "nav-item active" : "nav-item"}
              onClick={() => setStatus(key)}
            >
              <span><b>{key === "radar" ? "◉" : key === "selected" ? "✓" : "·"}</b> {STATUS_META[key].label}</span>
              <em>{counts[key] ?? 0}</em>
            </button>
          ))}
          <div className="sidebar-rule" />
          <div className="editorial-note">
            <span>编辑原则</span>
            <p>热点只是入口，真实证据和独立判断才是账号资产。</p>
          </div>
        </aside>

        <div className="board">
          <div className="board-head">
            <div>
              <span className="section-kicker">
                {status === "all" ? "MASTER LIBRARY" : STATUS_META[status].label}
              </span>
              <h2>{status === "all" ? "全部选题" : STATUS_META[status].description}</h2>
            </div>
            <div className="result-count">{filteredTopics.length} 个结果</div>
          </div>

          <div className="filters">
            <label className="searchbox">
              <span>⌕</span>
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="搜索标题、钩子、来源或标签"
                aria-label="搜索选题"
              />
            </label>
            <select value={category} onChange={(event) => setCategory(event.target.value)}>
              {categoryOptions.map((item) => <option key={item}>{item}</option>)}
            </select>
            <select value={platform} onChange={(event) => setPlatform(event.target.value)}>
              {platformOptions.map((item) => <option key={item}>{item}</option>)}
            </select>
            <select value={sort} onChange={(event) => setSort(event.target.value as "score" | "updated")}>
              <option value="score">按评分排序</option>
              <option value="updated">按更新时间</option>
            </select>
          </div>

          {error && (
            <div className="error-banner">
              <span>{error}</span>
              <button onClick={() => setError("")}>关闭</button>
            </div>
          )}

          {loading ? (
            <div className="loading-grid">
              {[1, 2, 3, 4, 5, 6].map((item) => <div key={item} />)}
            </div>
          ) : filteredTopics.length ? (
            <div className="topic-grid">
              {filteredTopics.map((topic) => (
                <article className="topic-card" key={topic.id}>
                  <div className="topic-card-top">
                    <div className="topic-tags">
                      <span className={`status-pill status-${topic.status}`}>
                        {STATUS_META[topic.status].short}
                      </span>
                      <span>{topic.category}</span>
                    </div>
                    <button
                      className={topic.isPinned ? "pin-button pinned" : "pin-button"}
                      onClick={() => void patchTopic(topic.id, { isPinned: !topic.isPinned })}
                      aria-label={topic.isPinned ? "取消置顶" : "置顶"}
                    >
                      {topic.isPinned ? "◆" : "◇"}
                    </button>
                  </div>
                  <button className="card-main" onClick={() => setDetail(topic)}>
                    <h3>{topic.title}</h3>
                    <p>{topic.hook}</p>
                  </button>
                  <div className="topic-meta">
                    <span>{topic.platforms}</span>
                    <span>{topic.contentFormat}</span>
                  </div>
                  <div className="topic-score-row">
                    <div className={`score-number ${scoreTone(topic.scoreTotal)}`}>
                      <strong>{topic.scoreTotal}</strong>
                      <span>/ 100</span>
                    </div>
                    <div className="score-track" aria-label={`选题评分 ${topic.scoreTotal}`}>
                      <i style={{ width: `${topic.scoreTotal}%` }} />
                    </div>
                  </div>
                  <div className="topic-card-bottom">
                    <span>更新于 {formatTime(topic.updatedAt)}</span>
                    <div className="quick-actions">
                      {topic.status !== "shortlist" && topic.status !== "selected" && (
                        <button onClick={() => void patchTopic(topic.id, { status: "shortlist" })}>
                          加入重点
                        </button>
                      )}
                      {topic.status === "shortlist" && (
                        <button onClick={() => void patchTopic(topic.id, { status: "selected" })}>
                          选它开拍
                        </button>
                      )}
                      {topic.status === "selected" && (
                        <button onClick={() => void patchTopic(topic.id, { status: "produced" })}>
                          标记完成
                        </button>
                      )}
                      <button className="more-button" onClick={() => setDetail(topic)} aria-label="查看详情">···</button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <span>⌕</span>
              <h3>没有符合条件的选题</h3>
              <p>换一个筛选条件，或者收录一条新的灵感。</p>
            </div>
          )}
        </div>
      </section>

      {detail && (
        <div className="overlay" role="presentation" onMouseDown={() => setDetail(null)}>
          <aside className="detail-panel" role="dialog" aria-modal="true" aria-label="选题详情" onMouseDown={(event) => event.stopPropagation()}>
            <div className="panel-head">
              <div>
                <span className={`status-pill status-${detail.status}`}>
                  {STATUS_META[detail.status].label}
                </span>
                <span className="panel-category">{detail.category}</span>
              </div>
              <button onClick={() => setDetail(null)} aria-label="关闭详情">×</button>
            </div>
            <div className="panel-title">
              <h2>{detail.title}</h2>
              <div className={`large-score ${scoreTone(detail.scoreTotal)}`}>
                <strong>{detail.scoreTotal}</strong>
                <span>综合分</span>
              </div>
            </div>
            <blockquote>{detail.hook}</blockquote>
            <DetailSection label="核心角度" value={detail.angle} />
            <DetailSection label="为什么现在值得拍" value={detail.whyNow} />
            <DetailSection label="你能拿出的证据" value={detail.evidence} />
            <DetailSection label="最低成本拍法" value={detail.shooting} />
            <DetailSection label="风险与边界" value={detail.risk} muted />

            <div className="score-breakdown">
              <h3>选题评分</h3>
              <ScoreItem label="用户痛感" value={detail.scorePain} max={25} />
              <ScoreItem label="一手证据" value={detail.scoreEvidence} max={25} />
              <ScoreItem label="人设增量" value={detail.scorePersona} max={20} />
              <ScoreItem label="可复用性" value={detail.scoreRepeatability} max={15} />
              <ScoreItem label="时效讨论" value={detail.scoreTimeliness} max={10} />
              <ScoreItem label="制作可行" value={detail.scoreEase} max={5} />
            </div>

            <div className="source-card">
              <span>{detail.sourcePlatform}</span>
              <strong>{detail.sourceName}</strong>
              {detail.sourceUrl ? (
                <a href={detail.sourceUrl} target="_blank" rel="noreferrer">打开原始来源 ↗</a>
              ) : (
                <small>来自自己的真实项目</small>
              )}
            </div>

            <div className="panel-actions">
              <select
                value={detail.status}
                onChange={(event) =>
                  void patchTopic(detail.id, { status: event.target.value as TopicStatus })
                }
                aria-label="修改选题状态"
              >
                {TOPIC_STATUSES.map((key) => (
                  <option key={key} value={key}>{STATUS_META[key].label}</option>
                ))}
              </select>
              <button
                className="button button-primary"
                onClick={() => void patchTopic(detail.id, { status: "selected" })}
              >
                选择这条，进入拍摄
              </button>
            </div>
          </aside>
        </div>
      )}

      {adding && (
        <div className="overlay" role="presentation" onMouseDown={() => setAdding(false)}>
          <form className="add-panel" onSubmit={submitTopic} onMouseDown={(event) => event.stopPropagation()}>
            <div className="panel-head">
              <div>
                <span className="section-kicker">QUICK CAPTURE</span>
                <h2>收录一个新选题</h2>
              </div>
              <button type="button" onClick={() => setAdding(false)} aria-label="关闭新增表单">×</button>
            </div>
            <label>
              <span>选题标题 *</span>
              <input required value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} placeholder="用一句话说清楚观众为什么想点开" />
            </label>
            <label>
              <span>开头钩子 *</span>
              <textarea required value={form.hook} onChange={(event) => setForm({ ...form, hook: event.target.value })} placeholder="视频开头第一句" />
            </label>
            <div className="form-row">
              <label>
                <span>栏目</span>
                <select value={form.category} onChange={(event) => setForm({ ...form, category: event.target.value })}>
                  {categoryOptions.slice(1).map((item) => <option key={item}>{item}</option>)}
                </select>
              </label>
              <label>
                <span>发布平台</span>
                <input value={form.platforms} onChange={(event) => setForm({ ...form, platforms: event.target.value })} />
              </label>
            </div>
            <label>
              <span>核心角度</span>
              <textarea value={form.angle} onChange={(event) => setForm({ ...form, angle: event.target.value })} placeholder="这条内容真正要证明什么？" />
            </label>
            <label>
              <span>为什么现在值得拍</span>
              <textarea value={form.whyNow} onChange={(event) => setForm({ ...form, whyNow: event.target.value })} />
            </label>
            <label>
              <span>一手证据</span>
              <textarea value={form.evidence} onChange={(event) => setForm({ ...form, evidence: event.target.value })} placeholder="录屏、数据、成片、失败版本或个人经历" />
            </label>
            <label>
              <span>来源链接</span>
              <input type="url" value={form.sourceUrl} onChange={(event) => setForm({ ...form, sourceUrl: event.target.value })} placeholder="https://" />
            </label>
            <div className="form-actions">
              <button type="button" className="button button-ghost" onClick={() => setAdding(false)}>取消</button>
              <button className="button button-primary" disabled={saving}>{saving ? "正在收录…" : "收录到候选池"}</button>
            </div>
          </form>
        </div>
      )}
    </main>
  );
}

function DetailSection({
  label,
  value,
  muted = false,
}: {
  label: string;
  value: string;
  muted?: boolean;
}) {
  return (
    <section className={muted ? "detail-section muted" : "detail-section"}>
      <span>{label}</span>
      <p>{value || "待补充"}</p>
    </section>
  );
}

function ScoreItem({
  label,
  value,
  max,
}: {
  label: string;
  value: number;
  max: number;
}) {
  return (
    <div className="score-item">
      <span>{label}</span>
      <div><i style={{ width: `${(value / max) * 100}%` }} /></div>
      <strong>{value}</strong>
    </div>
  );
}
