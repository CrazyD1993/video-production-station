import {interpolate, useCurrentFrame} from 'remotion';

const fragments = [
  [-135, -70], [-96, 45], [-45, -110], [-20, 95], [40, -48], [78, 72], [125, -102], [138, 15]
];

export const WindowComparison = () => {
  const frame = useCurrentFrame();
  const crack = interpolate(frame, [12, 38], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const scatter = interpolate(frame, [92, 175], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const split = interpolate(frame, [245, 330], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const drawCrack = (x: number, y: number) => (
    <path d={`M${x} ${y} l-62 -64 l-24 67 l-58 -18 M${x} ${y} l55 -72 l31 75 l59 -28 M${x} ${y} l-18 83 l-74 32 M${x} ${y} l52 79 l70 26`} stroke="#EAF4FF" strokeWidth="7" strokeLinecap="round" opacity={crack} fill="none" />
  );
  return (
    <svg width="1080" height="1420" viewBox="0 0 1080 1420">
      <defs><filter id="glow"><feGaussianBlur stdDeviation="7" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
      {[250, 830].map((cx, index) => (
        <g key={cx}>
          <rect x={cx - 185} y="310" width="370" height="580" rx="16" fill="#15283B" stroke="#91B8D4" strokeWidth="16"/>
          <rect x={cx - 160} y="335" width="320" height="530" fill="#3D607B" opacity="0.92"/>
          {drawCrack(cx, 590)}
          {index === 1 && <g stroke="#E2B448" strokeWidth="18" opacity="0.96"><line x1={cx-148} y1="355" x2={cx+148} y2="845"/><line x1={cx+148} y1="355" x2={cx-148} y2="845"/></g>}
          <text x={cx} y="960" textAnchor="middle" fill="#DDEAF4" fontSize="34" fontWeight="700">{index === 0 ? '未贴胶带（示意）' : '贴米字胶带（示意）'}</text>
        </g>
      ))}
      {fragments.map(([dx, dy], i) => {
        const leftX = 250 + dx * scatter;
        const leftY = 590 + dy * scatter;
        const rightProgress = scatter * (i % 3 === 0 ? 0.55 : 0.22);
        const rightX = 830 + dx * rightProgress;
        const rightY = 590 + dy * rightProgress;
        return <g key={i}><rect x={leftX-12} y={leftY-8} width="24" height="16" rx="3" fill="#F4F8FF" opacity={scatter}/><rect x={rightX-12} y={rightY-8} width="24" height="16" rx="3" fill="#F4F8FF" opacity={scatter * 0.68}/></g>;
      })}
      {scatter > 0 && <g opacity={Math.min(1, scatter * 2)}><path d="M820 650 Q880 710 922 720" stroke="#E2B448" strokeWidth="5" strokeDasharray="12 12" fill="none"/><text x="830" y="1040" textAnchor="middle" fill="#F7D878" fontSize="31" fontWeight="700">可能辅助约束部分碎片</text></g>}
      {split > 0 && <g opacity={split} transform={`translate(${(1 - split) * 60}, 0)`}><rect x="670" y="1085" width="320" height="132" rx="14" fill="#263B4F" stroke="#E2B448" strokeWidth="3"/><text x="830" y="1140" textAnchor="middle" fill="#F7D878" fontSize="34" fontWeight="800">辅助约束</text><text x="830" y="1188" textAnchor="middle" fill="#DCE7F0" fontSize="28">不等于加固窗户</text></g>}
    </svg>
  );
};
