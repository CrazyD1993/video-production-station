import fs from 'node:fs';
import path from 'node:path';

const contractPath = path.resolve(process.argv[2] ?? '../shot-contract.json');
const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
const requiredFields = [
  'shot_id', 'start_time', 'duration_seconds', 'narration', 'shot_purpose',
  'subject_action', 'visual_change', 'evidence_type', 'subtitle', 'sound',
  'asset_path', 'asset_source', 'license_status', 'risk_tags',
  'production_method', 'fallback', 'current_status'
];
const allowedEvidenceTypes = new Set(['official_source', 'real_demo', 'illustrative_simulation']);
const errors = [];

if (!Array.isArray(contract.shots) || contract.shots.length === 0) {
  errors.push('合同中必须至少包含一个镜头。');
}

for (const shot of contract.shots ?? []) {
  for (const field of requiredFields) {
    const value = shot[field];
    if (value === undefined || value === null || value === '' || (Array.isArray(value) && value.length === 0)) {
      errors.push(`${shot.shot_id ?? 'unknown'} 缺少必填字段: ${field}`);
    }
  }
  if (!allowedEvidenceTypes.has(shot.evidence_type)) {
    errors.push(`${shot.shot_id} 的 evidence_type 不合法。`);
  }
  if (shot.evidence_type === 'illustrative_simulation' && !shot.illustrative_label) {
    errors.push(`${shot.shot_id} 是示意动画，必须提供 illustrative_label。`);
  }
  if (shot.evidence_type === 'illustrative_simulation' && !String(shot.illustrative_label).includes('结构示意')) {
    errors.push(`${shot.shot_id} 的示意标签必须明确包含“结构示意”。`);
  }
  if (!Array.isArray(shot.risk_tags) || shot.risk_tags.length === 0) {
    errors.push(`${shot.shot_id} 必须包含至少一个风险标签。`);
  }
}

if (errors.length) {
  console.error('镜头合同校验失败：');
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`镜头合同校验通过：${contract.shots.length} 个镜头可进入渲染。`);
