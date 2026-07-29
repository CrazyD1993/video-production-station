import { NextResponse } from "next/server";
import {
  createTopics,
  listTopics,
  updateTopic,
} from "../../../db/topics";
import type { TopicInput } from "../../../lib/topic-types";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const topics = await listTopics();
    return NextResponse.json({ topics });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "读取选题失败" },
      { status: 500 },
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as
      | TopicInput
      | { topics: TopicInput[] };
    const inputs = "topics" in body ? body.topics : [body];
    if (!inputs.length || inputs.some((topic) => !topic.title?.trim())) {
      return NextResponse.json({ error: "选题标题不能为空" }, { status: 400 });
    }
    const topics = await createTopics(inputs);
    return NextResponse.json({ topics }, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "新增选题失败" },
      { status: 500 },
    );
  }
}

export async function PATCH(request: Request) {
  try {
    const body = (await request.json()) as {
      id?: string;
      updates?: Record<string, unknown>;
    };
    if (!body.id || !body.updates) {
      return NextResponse.json({ error: "缺少选题或更新内容" }, { status: 400 });
    }
    const topic = await updateTopic(body.id, body.updates);
    if (!topic) {
      return NextResponse.json({ error: "没有可更新的字段" }, { status: 400 });
    }
    return NextResponse.json({ topic });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "更新选题失败" },
      { status: 500 },
    );
  }
}
