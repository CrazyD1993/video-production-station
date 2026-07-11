import {AbsoluteFill, Audio, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from 'remotion';

const Tape = ({rotate, delay}: {rotate: number; delay: number}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [delay, delay + 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'absolute', width: `${progress * 820}px`, height: 34, background: '#D8B04A', borderRadius: 18, left: 130, top: 760, transformOrigin: 'left center', transform: `rotate(${rotate}deg)`, boxShadow: '0 3px 10px rgba(0,0,0,0.35)'}} />;
};

const StructureOverlay = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [261, 275], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'absolute', inset: 0, opacity, pointerEvents: 'none'}}>
    <div style={{position: 'absolute', top: 106, left: 98, right: 98, padding: '15px 20px', borderRadius: 28, border: '2px solid #C8D8E5', background: 'rgba(12,30,45,0.88)', color: '#FFFFFF', textAlign: 'center', fontSize: 28, fontWeight: 700}}>结构示意，不代表实际玻璃强度或碎片效果</div>
    <svg width="1080" height="1920" viewBox="0 0 1080 1920"><path d="M540 700 l-130 -145 l-65 164 l-145 -55 M540 700 l135 -150 l58 160 l155 -62 M540 700 l-46 180 l-162 83 M540 700 l115 176 l175 80" stroke="#F2F7FF" strokeWidth="12" fill="none" strokeLinecap="round"/><path d="M350 500 L730 900 M730 500 L350 900" stroke="#E2B448" strokeWidth="24" opacity="0.9"/></svg>
  </div>;
};

export const PrototypeR2 = () => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [141, 155, 245, 261], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const introOpacity = interpolate(frame, [0, 245, 261], [1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const zoom = interpolate(frame, [0, 420], [1.12, 1.28]);
  return <AbsoluteFill style={{background: '#0A1520', fontFamily: 'Arial, PingFang SC, sans-serif', overflow: 'hidden'}}>
    <OffthreadVideo src={staticFile('rain-window-mixkit.mp4')} startFrom={5} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`, filter: 'brightness(0.56) saturate(0.78)'}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,16,26,0.32), rgba(5,16,26,0.1) 45%, rgba(5,16,26,0.82))'}} />
    <Tape rotate={34} delay={18}/><Tape rotate={-34} delay={43}/>
    <div style={{position: 'absolute', left: 68, right: 68, top: 110, opacity: introOpacity, color: '#FFFFFF', fontSize: 54, lineHeight: 1.18, fontWeight: 800, textShadow: '0 3px 16px rgba(0,0,0,0.7)'}}>台风一来，很多人<br/>第一件事就是贴胶带</div>
    <div style={{position: 'absolute', left: 64, right: 64, top: 760, textAlign: 'center', opacity: reveal, color: '#FFFFFF', fontSize: 76, fontWeight: 900, lineHeight: 1.05, textShadow: '0 5px 20px rgba(0,0,0,0.85)'}}>先别把它当<br/>护身符</div>
    <StructureOverlay />
    <div style={{position: 'absolute', left: 64, right: 64, bottom: 250, opacity: interpolate(frame, [261, 275], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), color: '#F6D773', fontSize: 58, lineHeight: 1.2, fontWeight: 900, textAlign: 'center', textShadow: '0 3px 18px rgba(0,0,0,0.8)'}}>胶带 ≠ 防台风玻璃</div>
    <div style={{position: 'absolute', left: 70, right: 70, bottom: 105, color: '#D0DFEA', fontSize: 27, textAlign: 'center'}}>台风防护请以当地气象和应急部门实时通知为准</div>
    <Audio src={staticFile('narration-r2-reference.wav')} volume={0.93}/>
  </AbsoluteFill>;
};
