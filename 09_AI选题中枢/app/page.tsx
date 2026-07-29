import type { Metadata } from "next";
import TopicBoard from "./TopicBoard";

export const metadata: Metadata = {
  title: "选题罗盘｜私人 AI 内容中枢",
  description:
    "为女性 AI 真人 IP 打造的选题雷达、评分、筛选和制作决策系统。",
};

export default function Home() {
  return <TopicBoard />;
}
