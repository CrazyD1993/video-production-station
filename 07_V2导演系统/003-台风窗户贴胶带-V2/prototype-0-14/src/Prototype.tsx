import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {WindowComparison} from './components/WindowComparison';

const captions = [
  {from: 0, to: 90, text: '贴胶带，保护的是窗？'},
  {from: 90, to: 240, text: '可能辅助约束部分碎片'},
  {from: 240, to: 420, text: '辅助约束 ≠ 加固窗户'}
];

export const Prototype = () => {
  const frame = useCurrentFrame();
  const active = captions.find((caption) => frame >= caption.from && frame < caption.to) ?? captions[2];
  return (
    <AbsoluteFill style={{backgroundColor: '#0B1723', fontFamily: 'Arial, PingFang SC, sans-serif'}}>
      <AbsoluteFill style={{background: 'linear-gradient(#183249 0%, #0B1723 72%)'}} />
      <div style={{position: 'absolute', top: 92, left: 120, right: 120, border: '2px solid #91B8D4', borderRadius: 999, backgroundColor: '#263B4F', color: '#FFFFFF', fontSize: 31, fontWeight: 700, textAlign: 'center', padding: '18px 24px', zIndex: 3}}>结构示意，不代表实际玻璃强度或碎片效果</div>
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 210}}><WindowComparison /></AbsoluteFill>
      <div style={{position: 'absolute', left: 64, right: 64, bottom: 245, color: '#FFFFFF', fontSize: 62, lineHeight: 1.26, fontWeight: 800, textAlign: 'center', letterSpacing: 0}}>{active.text}</div>
      <div style={{position: 'absolute', left: 90, right: 90, bottom: 120, color: '#BFD2E1', fontSize: 28, textAlign: 'center'}}>台风防护请以当地气象和应急部门实时通知为准</div>
      <Sequence from={0}><Audio src={staticFile('narration.wav')} volume={0.92}/></Sequence>
    </AbsoluteFill>
  );
};
