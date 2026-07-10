import {Composition} from 'remotion';
import {Prototype} from './Prototype';

export const Root = () => (
  <Composition
    id="Prototype"
    component={Prototype}
    durationInFrames={420}
    fps={30}
    width={1080}
    height={1920}
  />
);
